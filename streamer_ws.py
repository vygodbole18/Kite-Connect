# streamer_ws.py
import os
from dotenv import load_dotenv
from kiteconnect import KiteTicker, KiteConnect
from trigger import route_request  # reuses your existing routing to buy/sell

load_dotenv()
API_KEY = os.getenv("API_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

def _build_token_map(kite, symbols):
    """
    symbols: list like ["RELIANCE", "TCS", "HDFCBANK"]
    returns: dict { "RELIANCE": 738561, ... }
    """
    dump = kite.instruments("NSE")
    wanted = set(symbols)
    out = {}
    for ins in dump:
        if ins["segment"] == "NSE":
            tsym = ins["tradingsymbol"]
            if tsym in wanted:
                out[tsym] = ins["instrument_token"]
    missing = wanted - set(out.keys())
    if missing:
        raise ValueError(f"Tokens not found for: {', '.join(sorted(missing))}")
    return out

def start_stream(stocks):
    """
    stocks: list of dicts like your current user_input, one per stock:
      {
        "Stock_name": "NSE:RELIANCE",
        "Trigger": 2500,
        "Buy_Or_Sell": "BUY",   # or "SELL"
        "Option": "RELIANCE25NOV2500CE"
      }
    """
    # Build symbol -> config
    symbol_cfg = {}
    symbols = []
    for s in stocks:
        exch, sym = s["Stock_name"].split(":")
        symbols.append(sym)
        symbol_cfg[sym] = s

    kite = KiteConnect(api_key=API_KEY)
    kite.set_access_token(ACCESS_TOKEN)

    # Map tradingsymbol → instrument_token, and reverse
    sym_to_token = _build_token_map(kite, symbols)
    token_to_sym = {tok: sym for sym, tok in sym_to_token.items()}

    # Track previous price per symbol (for cross/ touch logic)
    EPS = 0.01
    prev_price = {sym: None for sym in symbols}

    kws = KiteTicker(API_KEY, ACCESS_TOKEN)

    def on_ticks(ws, ticks):
        for t in ticks:
            tok = t["instrument_token"]
            sym = token_to_sym.get(tok)
            if sym is None:
                continue

            # KiteTicker provides last_price / last_traded_price depending on mode
            curr = t.get("last_price") or t.get("last_traded_price")
            if curr is None:
                continue
            curr = float(curr)

            prev = prev_price[sym]
            prev_price[sym] = curr

            if prev is None:
                continue

            cfg = symbol_cfg[sym]
            trigger = float(cfg["Trigger"])

            crossed_up   = (prev < trigger <= curr)
            crossed_down = (prev > trigger >= curr)
            touched_now  = abs(curr - trigger) <= EPS

            if crossed_up or crossed_down or touched_now:
                print(f"[WS] {sym}: trigger {trigger} hit at {curr} → routing order for {cfg['Option']}")
                # IMPORTANT: In production, enqueue to a worker thread/process
                route_request(cfg)  # uses your existing buy/sell modules

                # optional: if one-shot per symbol, unsubscribe after firing
                # ws.unsubscribe([tok])

    def on_connect(ws, response):
        tokens = list(sym_to_token.values())
        ws.subscribe(tokens)
        ws.set_mode(ws.MODE_LTP, tokens)  # LTP is enough for trigger checks

    def on_close(ws, code, reason):
        print("WebSocket closed:", code, reason)

    def on_error(ws, code, reason):
        print("WebSocket error:", code, reason)

    kws.on_ticks = on_ticks
    kws.on_connect = on_connect
    kws.on_close = on_close
    kws.on_error = on_error

    # Blocking call — run in its own process/thread if you later need concurrency
    kws.connect(threaded=False)

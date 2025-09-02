from auth import get_kite
kite = get_kite()
import time
from trigger import route_request  # routes to buy/sell:contentReference[oaicite:0]{index=0}

def start_watching(user_input):
    instrument = user_input["Stock_name"]
    trigger = float(user_input["Trigger"])
    side = user_input["Buy_Or_Sell"].upper()  # "BUY" or "SELL"

    # 1 paisa tolerance to avoid float equality issues
    EPS = 0.01

    prev_ltp = None

    while True:
        ltp_data = kite.ltp([instrument])
        curr_ltp = float(ltp_data[instrument]["last_price"])
        print("Current LTP:", curr_ltp, "Trigger:", trigger)

        # Initialize baseline without firing on first read
        if prev_ltp is None:
            prev_ltp = curr_ltp
            time.sleep(15)
            continue

        # Fire when price TOUCHES or CROSSES the trigger in EITHER direction
        crossed_up = (prev_ltp < trigger <= curr_ltp)
        crossed_down = (prev_ltp > trigger >= curr_ltp)
        touched_now = abs(curr_ltp - trigger) <= EPS

        if crossed_up or crossed_down or touched_now:
            orderID = route_request(user_input)  # calls buy/sell per your choice:contentReference[oaicite:1]{index=1}
            # Monitor until terminal state (same as your original loop)
            while True:
                order_list = kite.order_history(orderID)
                latest_status = order_list[-1]["status"]
                if latest_status == "COMPLETE":
                    print("Order is successfully executed!")
                    return
                elif latest_status in ("CANCELLED", "REJECTED"):
                    print("Order failed or cancelled")
                    return
                else:
                    time.sleep(15)

        prev_ltp = curr_ltp
        time.sleep(15)

from auth import get_kite
kite = get_kite()

def place_sell_order(user_input):
    option_to_sell = user_input["Option"]

    ltp_data = kite.ltp([f"NFO:{option_to_sell}"])
    ltp_price = ltp_data[f"NFO:{option_to_sell}"]["last_price"]

    #Calculate +0.25% buffer to simulate MARKET order
    buffer = round(ltp_price * 0.0025, 2)
    raw_price = ltp_price + buffer

    #Round to nearest valid tick size (₹0.05)
    tick_size = 0.05
    final_price = round(round(raw_price / tick_size) * tick_size, 2)

    #Get correct lot size from instrument dump
    instruments = kite.instruments("NFO")
    instrument = next(i for i in instruments if i["tradingsymbol"] == option_to_sell and i["segment"] == "NFO-OPT")
    lot_size = instrument["lot_size"]

    print(f"Placing LIMIT SELL for {option_to_sell}")
    print(f"Final limit price: ₹{final_price}, Lot size: {lot_size}")

    orderID = kite.place_order(
        variety="regular",
        exchange="NFO",
        tradingsymbol=option_to_sell,
        transaction_type="SELL",
        quantity=lot_size,
        product="NRML",
        order_type="LIMIT",
        price=final_price
    )

    return orderID
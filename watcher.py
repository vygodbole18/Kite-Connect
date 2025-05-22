from auth import get_kite
kite = get_kite()
import time
from trigger import route_request




def start_watching(user_input):
    while True:
        instrument = user_input.get("Stock_name")
        ltp_data = kite.ltp([instrument])
        last_traded_price = float(ltp_data[user_input["Stock_name"]]["last_price"])
        ohlc_of_stock = kite.ohlc([instrument])
        print("LTP data:", ltp_data)
        print("Current LTP:", last_traded_price)
        print("Trigger:", user_input["Trigger"])
        high_of_stock = ohlc_of_stock[user_input["Stock_name"]]["ohlc"]["high"]
        low_of_stock = ohlc_of_stock[user_input["Stock_name"]]["ohlc"]["low"]
        print("OHLC High:", high_of_stock)
        print("OHLC Low:", low_of_stock)
        if (last_traded_price == user_input["Trigger"]) or (low_of_stock <=user_input["Trigger"] <= high_of_stock):
            orderID = route_request(user_input)
            while True:
                order_list = kite.order_history(orderID)
                latest_status = order_list[-1]["status"]
                if latest_status == "COMPLETE":
                    print("Order is successfully executed!")
                    return
                elif latest_status == "CANCELLED" or latest_status == "REJECTED":
                    print("Order failed or cancelled")
                    return
                else:
                    time.sleep(15)    
        else:
            time.sleep(15)





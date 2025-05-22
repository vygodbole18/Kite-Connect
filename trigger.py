from auth import get_kite
kite = get_kite()
from buy import place_buy_order
from sell import place_sell_order


def route_request(user_input):
    action = user_input["Buy_Or_Sell"]
    if (action == "BUY"):
        orderID = place_buy_order(user_input)
        return orderID
    else:
        orderID = place_sell_order(user_input)
        return orderID

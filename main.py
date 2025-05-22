from watcher import start_watching

stockSymbol = input("Please enter the name of the stock you want to track: ").strip().upper()
triggerPrice = float(input("Please enter the price at which you want to buy or sell: ").strip())
triggerAction = input("Do you want to buy or sell?: ").strip().upper()
optionSymbol = input("Please enter the symbol for the option you have: ").strip().upper()

add_to_string = "NSE:"
stockSymbol = add_to_string + stockSymbol

user_input = {
    "Stock_name" : stockSymbol , 
    "Trigger" : triggerPrice , 
    "Buy_Or_Sell" : triggerAction , 
    "Option" : optionSymbol , 
}

start_watching(user_input)


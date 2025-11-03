from streamer_ws import start_stream

stocks = []

print("How many stocks do you want to track?")
count = int(input("Enter number: ").strip())

for i in range(count):
    print(f"\n### Enter details for Stock #{i+1} ###")

    stockSymbol = input("Stock name (e.g. RELIANCE): ").strip().upper()
    triggerPrice = float(input("Trigger price: ").strip())
    triggerAction = input("Buy or Sell?: ").strip().upper()
    optionSymbol = input("Option symbol (e.g. RELIANCE25FEB2500CE): ").strip().upper()

    stockNameFull = "NSE:" + stockSymbol 
    user_input = {
        "Stock_name": stockNameFull,
        "Trigger": triggerPrice,
        "Buy_Or_Sell": triggerAction,
        "Option": optionSymbol
    }

    stocks.append(user_input)

print("\n Streaming live prices… waiting for triggers...\n")
start_stream(stocks)

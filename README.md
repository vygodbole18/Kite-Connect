#  Kite Options Bot (Zerodha)

A fully functional, trigger-based options trading bot built using the Zerodha Kite Connect API.  
This bot allows users to define a stock, a trigger price, and a target option to buy/sell when that price is reached.

---

## Features

- ✅ Buy or Sell options when a stock hits a defined trigger price  
- ✅ Automatically fetches the correct lot size  
- ✅ Places smart **LIMIT orders** simulating market orders (+/- 0.25% from LTP)  
- ✅ Tracks both **LTP and OHLC** for better trigger accuracy  
- ✅ Fully modular: split into `main`, `auth`, `watcher`, `trigger`, `buy`, and `sell`  

---

##  How It Works

1. User provides:
   - Stock to monitor (e.g., `RELIANCE`)
   - Trigger price (e.g., `1400`)
   - Action (`BUY` or `SELL`)
   - Option symbol (e.g., `RELIANCE25MAY1460CE`)
2. `watcher.py` continuously checks the stock's LTP and OHLC  
3. When the trigger is hit:
   - `buy.py` or `sell.py` is invoked
   - Order is placed using proper lot size and smart limit pricing
4. Order status is monitored until complete or failed

---

## ⚙️ Setup Instructions

1. Install dependencies:

```bash
pip install kiteconnect python-dotenv
```
2. **Create a `.env` file** (Do NOT commit this to Git)  
Inside your project folder, create a file named `.env` and add:
```
API_KEY=your_api_key
API_SECRET=your_api_secret
REQUEST_TOKEN=your_request_token
ACCESS_TOKEN=your_access_token
```

3. Generate your access token daily using
```
python generate_token.py
```
4. Run the bot
```
python main.py
```
## Safety Notes

- This project is for **educational purposes only**.  
- You are responsible for **all trades placed** using your API credentials.  
- Always test in paper/mock mode before using real funds.


## License

This project is licensed under MIT.

## Built with ❤️ for 🇮🇳
©️Vedant Godbole


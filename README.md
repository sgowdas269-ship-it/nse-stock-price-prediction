# NSE Stock Price Prediction Using Machine Learning

A beginner-friendly Flask app that downloads NSE historical prices, trains a Random Forest regression model, estimates the next trading day's close, and plots recent closing prices.

## Run on Windows
1. Open this folder in VS Code.
2. Open Terminal > New Terminal.
3. Run:

```powershell
py -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python app.py
```

If `py` is unavailable, use `python -m venv .venv`. Open http://127.0.0.1:5000 in your browser.

Symbols: TCS, INFY, RELIANCE, SBIN, ITC. The app appends `.NS` for Yahoo Finance's NSE ticker format.

## How it works
1. Browser sends the symbol to Flask.
2. `stock_model.py` downloads daily history through yfinance.
3. The five previous closing prices are used as model features.
4. Random Forest trains on the earlier 80% and is evaluated on the later 20% of observations.
5. The predicted next close and chart history are returned to the website.

## Limitations
This is an educational prototype, not an investment tool. yfinance data may be delayed, unavailable, or change. Historical test performance does not guarantee future accuracy. The model uses only past closing prices and may perform poorly. Not financial advice.

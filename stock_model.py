import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

def predict_stock(ticker):
    data = yf.download(ticker, period='5y', interval='1d', auto_adjust=True, progress=False)
    if data is None or data.empty:
        raise ValueError(f'No historical data found for {ticker}. Try TCS, INFY, or RELIANCE.')
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    if 'Close' not in data.columns:
        raise ValueError('The data source did not return closing prices.')
    close = pd.to_numeric(data['Close'], errors='coerce').dropna()
    if len(close) < 100:
        raise ValueError('Not enough historical data to train this model.')
    frame = pd.DataFrame({'Close': close})
    for lag in range(1, 6):
        frame[f'lag_{lag}'] = frame['Close'].shift(lag)
    frame['target'] = frame['Close'].shift(-1)
    frame = frame.dropna()
    cols = [f'lag_{lag}' for lag in range(1, 6)]
    X, y = frame[cols], frame['target']
    split = int(len(frame) * .8)
    X_train, X_test, y_train, y_test = X.iloc[:split], X.iloc[split:], y.iloc[:split], y.iloc[split:]
    model = RandomForestRegressor(n_estimators=150, random_state=42, min_samples_leaf=2, n_jobs=-1)
    model.fit(X_train, y_train)
    test_pred = model.predict(X_test)
    latest_features = pd.DataFrame([close.iloc[-5:][::-1].to_numpy()], columns=cols)
    predicted = float(model.predict(latest_features)[0])
    latest = float(close.iloc[-1])
    history = [{'date': d.strftime('%Y-%m-%d'), 'close': round(float(v), 2)} for d, v in close.tail(180).items()]
    return {'ticker':ticker, 'latest_date':close.index[-1].strftime('%Y-%m-%d'), 'latest_close':round(latest,2),
      'predicted_next_close':round(predicted,2), 'change_percent':round((predicted-latest)/latest*100,2),
      'mae':round(float(mean_absolute_error(y_test,test_pred)),2),
      'rmse':round(float(np.sqrt(mean_squared_error(y_test,test_pred))),2), 'test_rows':int(len(y_test)),
      'history':history, 'note':'Educational estimate only—not financial advice. Actual market prices may differ.'}

from flask import Flask, render_template, request, jsonify
from stock_model import predict_stock
app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/api/predict', methods=['POST'])
def predict():
    payload = request.get_json(silent=True) or {}
    symbol = str(payload.get('symbol', 'TCS')).strip().upper()
    if not symbol or len(symbol) > 20 or not symbol.replace('.', '').replace('-', '').isalnum():
        return jsonify({'error':'Enter a valid symbol, e.g. TCS or INFY.'}), 400
    ticker = symbol if symbol.endswith('.NS') else symbol + '.NS'
    try:
        return jsonify(predict_stock(ticker))
    except ValueError as e:
        return jsonify({'error':str(e)}), 400
    except Exception:
        app.logger.exception('Prediction failed')
        return jsonify({'error':'Could not fetch stock data. Check your internet connection and symbol, then try again.'}), 502
if __name__ == '__main__':
    app.run(debug=True)

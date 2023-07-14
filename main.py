from flask import Flask, jsonify, render_template
import yfinance as yf

app = Flask(__name__)

def calculate_profit_loss(purchase_price, current_price, quantity):
    return (current_price - purchase_price) * quantity

@app.route("/data")
def get_stock_info():
    tickers = ["AAPL", "TSLA"]
    purchase_info = {
        "AAPL": [190.78, 5],  # Bought 10 AAPL stocks at $150 each
        "TSLA": [278.69, 5],
    }

    data = yf.download(tickers=tickers, period="1d")
    total_profit_loss = 0.0

    stock_info = []
    for ticker in tickers:
        purchase_price, quantity = purchase_info[ticker]
        current_price = data['Close'][ticker].iloc[0]
        profit_loss = calculate_profit_loss(purchase_price, current_price, quantity)
        total_profit_loss += profit_loss

        stock_info.append({
            "ticker": ticker,
            "purchase_price": purchase_price,
            "quantity": quantity,
            "current_price": current_price,
            "profit_loss": profit_loss,
        })

    return jsonify({"stock_info": stock_info, "total_profit_loss": total_profit_loss})

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)

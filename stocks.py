import yfinance as yf
import tkinter as tk
from threading import Thread
import time


def calculate_profit_loss(purchase_price, current_price, quantity):
    return (current_price - purchase_price) * quantity


def get_stock_info(text_widget):
    tickers = ["AAPL", "TSLA"]
    purchase_info = {
        "AAPL": [190.78, 5],  # Bought 10 AAPL stocks at $150 each
        "TSLA": [278.69, 5],
    }

    prev_total_profit_loss = 0.0

    while True:  # Loop forever
        data = yf.download(tickers=tickers, period="1d")
        total_profit_loss = 0.0

        results = ""
        for ticker in tickers:
            purchase_price, quantity = purchase_info[ticker]
            current_price = data['Close'][ticker].iloc[0]
            profit_loss = calculate_profit_loss(purchase_price, current_price, quantity)
            total_profit_loss += profit_loss

            results += f"Ticker: {ticker}\n"
            results += f"Purchase price: ${purchase_price}\n"
            results += f"Quantity: {quantity}\n"
            results += f"Current price: ${current_price}\n"
            if profit_loss >= 0:
                results += f"Profit: ${profit_loss}\n"
            else:
                results += f"Loss: ${-profit_loss}\n"  # Negate to make the value positive
            results += "\n"

        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, results)

        total_profit_loss_str = ""
        if total_profit_loss >= 0:
            total_profit_loss_str += f"Total Profit: ${total_profit_loss}\n"
        else:
            total_profit_loss_str += f"Total Loss: ${-total_profit_loss}\n"  # Negate to make the value positive

        if total_profit_loss > prev_total_profit_loss:
            text_widget.insert(tk.END, total_profit_loss_str, 'green')
        elif total_profit_loss < prev_total_profit_loss:
            text_widget.insert(tk.END, total_profit_loss_str, 'red')
        else:  # total_profit_loss == prev_total_profit_loss
            text_widget.insert(tk.END, total_profit_loss_str)

        text_widget.tag_config('green', foreground='green')
        text_widget.tag_config('red', foreground='red')

        prev_total_profit_loss = total_profit_loss

        time.sleep(2)  # Delay for 60 seconds


root = tk.Tk()
text_widget = tk.Text(root)
text_widget.pack()

# Start the get_stock_info function in a separate thread
thread = Thread(target=get_stock_info, args=(text_widget,))
thread.start()

root.mainloop()

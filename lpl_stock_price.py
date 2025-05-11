import tkinter as tk
from tkinter import ttk
import yfinance as yf
import threading
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")  # Prevents backend conflicts in some environments

# Constants
STOCK_TICKER = "LALPATHLAB.NS"
REFRESH_INTERVAL = 10  # seconds

# Data buffer
price_history = []

# Fetch stock price
def fetch_stock_price():
    stock = yf.Ticker(STOCK_TICKER)
    data = stock.history(period="1d", interval="1m")
    if not data.empty:
        latest_price = data["Close"].iloc[-1]
        return latest_price
    else:
        return None

# Update UI elements
def update_price_and_graph():
    while running:
        try:
            price = fetch_stock_price()
            if price:
                price_history.append(price)
                price_var.set(f"Dr. Lal PathLabs Stock: ₹{price:.2f}")
                draw_graph()
        except Exception as e:
            price_var.set(f"Error: {e}")
        time.sleep(REFRESH_INTERVAL)

# Draw live graph
def draw_graph():
    ax.clear()
    ax.plot(price_history, color='lime', linewidth=2)
    ax.set_title("Live Price Chart", color='white')
    ax.set_facecolor('#1e1e1e')
    fig.patch.set_facecolor('#1e1e1e')
    ax.tick_params(colors='white')
    canvas.draw()

# Clean exit
def stop_script():
    global running
    running = False
    root.destroy()

# GUI setup
root = tk.Tk()
root.title("Dr. Lal PathLabs Stock Tracker")
root.geometry("500x400")
root.configure(bg="#1e1e1e")

# Display current price
price_var = tk.StringVar()
price_label = tk.Label(root, textvariable=price_var, font=("Helvetica", 16), bg="#1e1e1e", fg="#00ff00")
price_label.pack(pady=10)

# Close button
close_button = ttk.Button(root, text="Close", command=stop_script)
close_button.pack(pady=5)

# Matplotlib figure setup
fig, ax = plt.subplots(figsize=(5, 2.5), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill=tk.BOTH, expand=True)

# Start background thread
running = True
threading.Thread(target=update_price_and_graph, daemon=True).start()

root.mainloop()

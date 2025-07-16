# keep_alive.py

from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"  # This confirms the server is alive!

def run():
    app.run(host='0.0.0.0', port=8080)  # Ensures the Flask server is running on port 8080

def keep_alive():
    t = Thread(target=run)
    t.start()  # Starts the Flask server in a separate thread

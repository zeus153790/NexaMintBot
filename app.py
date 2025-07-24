import os
from flask import Flask
from threading import Thread
from main import main as run_bot

app = Flask(__name__)

@app.route('/')
def home():
    return "NexaMint Bot is running!"

def run_bot_in_thread():
    run_bot()

def keep_alive():
    bot_thread = Thread(target=run_bot_in_thread)
    bot_thread.daemon = True
    bot_thread.start()

# Start the bot when the app starts
keep_alive()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
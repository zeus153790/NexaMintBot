# helpers.py

import re
import datetime

from config import ORDER_PREFIX

# 🧠 Global counter for order IDs (you can enhance this with file or db later)
order_counter = 1

# ✅ Validate MLBB ID format: digits (digits)
def is_valid_mlbb_id(text):
    pattern = r"^\d+\s\(\d+\)$"
    return re.match(pattern, text) is not None

# 🔢 Generate unique order ID
def generate_order_id():
    global order_counter
    order_id = f"{ORDER_PREFIX}-{order_counter:04d}"
    order_counter += 1
    return order_id

# 🌐 Get language-specific message
def get_message(user_lang, messages):
    return messages.get(user_lang, messages["en"])

# 🕓 Get current readable time (optional use)
def current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ✅ Format diamond package nicely
def format_package(diamond):
    if isinstance(diamond, int):
        return f"{diamond} 💎"
    elif "weekly" in diamond:
        return "🔄 Weekly Pass"
    elif "+" in diamond:
        return f"🎁 {diamond} Bonus"
    return str(diamond)

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

# ✅ Validate if uploaded screenshot is likely from KBZPay or WavePay
def is_valid_screenshot(file):
    if file.mime_type not in ["image/jpeg", "image/png"]:
        return False

    filename = getattr(file, "file_name", "")
    keywords = ["kbz", "wave", "payment", "screenshot"]
    return any(keyword in filename.lower() for keyword in keywords)

# ⏱️ Estimated delivery time message
def get_estimated_time():
    return "⏳ Estimated Delivery: 5–10 minutes after payment confirmation"

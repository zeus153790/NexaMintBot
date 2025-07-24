import json
import os
from datetime import datetime
from config import USER_DATA_FILE, ORDERS_FILE, DIAMOND_PRICES, ORDER_STATUS

# Load data from JSON file
def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"users": {}, "orders": {}, "next_order_id": 1} if file_path == ORDERS_FILE else {}

# Save data to JSON file
def save_data(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Generate order ID
def generate_order_id():
    data = load_data(ORDERS_FILE)
    order_id = f"NXM-{str(data.get('next_order_id', 1)).zfill(4)}"
    data['next_order_id'] = data.get('next_order_id', 1) + 1
    save_data(data, ORDERS_FILE)
    return order_id

# Get user data
def get_user_data(user_id):
    data = load_data(USER_DATA_FILE)
    return data.get(str(user_id), {})

# Save user data
def save_user_data(user_id, user_data):
    data = load_data(USER_DATA_FILE)
    data[str(user_id)] = user_data
    save_data(data, USER_DATA_FILE)

# Save order
def save_order(order):
    data = load_data(ORDERS_FILE)
    order_id = order['order_id']
    data['orders'][order_id] = order
    save_data(data, ORDERS_FILE)

# Get user orders
def get_user_orders(user_id):
    data = load_data(ORDERS_FILE)
    orders = data.get('orders', {})
    return [order for order in orders.values() if order['user_id'] == user_id]

# Get pending orders
def get_pending_orders():
    data = load_data(ORDERS_FILE)
    orders = data.get('orders', {})
    return [order for order in orders.values() if order['status'] == ORDER_STATUS['pending']]

# Update order status
def update_order_status(order_id, status, reject_reason=None):
    data = load_data(ORDERS_FILE)
    if order_id in data['orders']:
        data['orders'][order_id]['status'] = status
        if reject_reason:
            data['orders'][order_id]['reject_reason'] = reject_reason
        save_data(data, ORDERS_FILE)
        return True
    return False

# Get order by ID
def get_order(order_id):
    data = load_data(ORDERS_FILE)
    return data['orders'].get(order_id)

# Format price
def format_price(price):
    return "{:,}".format(price)

# Validate MLBB format
def validate_mlbb(text):
    import re
    pattern = r'^\d+\s*\(\d+\)$'
    return bool(re.match(pattern, text))

# Get diamond price
def get_diamond_price(category, package):
    return DIAMOND_PRICES[category][package]

# Create keyboard
def create_keyboard(items, columns=2):
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    buttons = []
    row = []
    for item in items:
        row.append(InlineKeyboardButton(item, callback_data=item))
        if len(row) == columns:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    return InlineKeyboardMarkup(buttons)

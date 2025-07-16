import re
import time

# Simple in-memory storage (replace with DB in real use)
ORDERS = {}
USER_ORDERS = {}

def validate_mlbb_id(mlbb_id: str) -> bool:
    """
    Validate MLBB ID format, example: "12345678 (1234)"
    Numeric digits, space, zone in parentheses
    """
    pattern = r"^\d{6,8}\s\(\d{4}\)$"
    return bool(re.match(pattern, mlbb_id))

def generate_order_id() -> str:
    """
    Generate a unique order ID like NXM-0001, incrementing
    """
    count = len(ORDERS) + 1
    return f"NXM-{count:04d}"

def is_duplicate_order(user_id: int) -> bool:
    """
    Check if user has placed an order in last 5 minutes (300 seconds)
    """
    now = time.time()
    user_times = USER_ORDERS.get(user_id, [])
    # Filter out times older than 5 minutes
    USER_ORDERS[user_id] = [t for t in user_times if now - t < 300]
    return len(USER_ORDERS[user_id]) > 0

def save_order(user_id: int, data: dict):
    """
    Save order info
    """
    order_id = data["order_id"]
    ORDERS[order_id] = {
        "user_id": user_id,
        "mlbb_id": data["mlbb_id"],
        "amount": data["amount"],
        "price": data["price"],
        "screenshot": data["screenshot"],
        "status": "Pending",
        "timestamp": time.time()
    }
    USER_ORDERS.setdefault(user_id, []).append(time.time())

def get_order_status(user_id: int) -> str:
    """
    Return last order status for user or "No orders"
    """
    user_orders = [o for o in ORDERS.values() if o["user_id"] == user_id]
    if not user_orders:
        return "No orders found."
    last_order = max(user_orders, key=lambda x: x["timestamp"])
    return last_order["status"]

def get_last_orders(user_id: int, limit=5):
    """
    Return list of last orders summary strings for user
    """
    user_orders = [o for o in ORDERS.values() if o["user_id"] == user_id]
    user_orders.sort(key=lambda x: x["timestamp"], reverse=True)
    result = []
    for o in user_orders[:limit]:
        ts = time.strftime("%Y-%m-%d %H:%M", time.localtime(o["timestamp"]))
        line = f"Order {o.get('order_id','NXM-XXXX')} | {o['amount']} diamonds | Status: {o['status']} | Date: {ts}"
        result.append(line)
    return result

def update_order_status(order_id: str, status: str):
    """
    Update order status in ORDERS
    """
    if order_id in ORDERS:
        ORDERS[order_id]["status"] = status

def get_user_data(user_id: int):
    """
    Dummy placeholder for user data retrieval
    """
    return None

def allowed_image(message) -> bool:
    """
    Check if message has a valid KBZPay or WavePay screenshot.
    Here simplified: accept any photo message.
    """
    # You can add image filename or metadata checks here
    return True

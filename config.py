# Configuration constants
BOT_TOKEN ="8003394770:AAHFQhndIsh82ZEwIOzGMYvBSpZKjUi_QPI"
ADMIN_GROUP_ID = -1002530649712

# Diamond prices
DIAMOND_PRICES = {
    "regular": {
        "11": 1000, "22": 2000, "56": 4500, "86": 5300,
        "112": 8500, "172": 10600, "257": 15900, "343": 21200,
        "429": 26500, "514": 31800, "600": 37100, "706": 42400,
        "878": 53000, "1049": 63600, "1135": 69000, "1412": 84800,
        "1755": 106000, "2195": 127300, "3688": 212000, "5532": 318200,
        "9288": 530000,
    },
    "weekly": {
        "Weekly Pass": 6500
    },
    "bonus": {
        "50+50": 4500, "150+150": 10500, "250+250": 16500, "500+500": 33500
    }
}

# Order statuses
ORDER_STATUS = {
    "pending": "⏳ Pending",
    "paid": "✅ Paid",
    "completed": "🎉 Completed",
    "rejected": "❌ Rejected"
}

# File paths for data persistence
USER_DATA_FILE = "user_data.json"
ORDERS_FILE = "orders.json"

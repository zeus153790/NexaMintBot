# config.py

# === BOT SETTINGS ===
BOT_TOKEN = "8003394770:AAGfx308bowIsW7btWpBP1mn_o-ciXulPL0"

# === ADMIN SETTINGS ===
ADMIN_GROUP_ID = -1002530649712  # Telegram group where admin gets order alerts

# === PAYMENT NUMBERS ===
KBZ_PAY = "09978772558"
WAVE_PAY = "09978772558"

# === ORDER PREFIX ===
ORDER_PREFIX = "NXM"

# === PRICE DICTIONARY ===
# Format: diamond_amount: price_in_MMK
PRICES = {
    # 💎 Regular Diamonds
    11: 1000,
    22: 2000,
    56: 4500,
    86: 5300,
    112: 8500,
    172: 10600,
    257: 15900,
    343: 21200,
    429: 26500,
    514: 31800,
    600: 37100,
    706: 42400,
    878: 53000,
    1049: 63600,
    1135: 69000,
    1412: 84800,
    1755: 106000,
    2195: 127300,
    3688: 212000,
    5532: 318200,
    9288: 530000,

    # 🔄 Weekly Pass
    "weekly": 6500,

    # 🎁 First Recharge Bonus
    "50+50": 4500,
    "150+150": 10500,
    "250+250": 16500,
    "500+500": 33500
}

# === LANGUAGES ===
DEFAULT_LANGUAGE = "mm"  # Options: "mm" (Myanmar), "en" (English)

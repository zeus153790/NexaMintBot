from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, MessageHandler, ConversationHandler,
    ContextTypes, filters
)
from config import BOT_TOKEN, ADMIN_GROUP_ID, PRICES, KBZ_PAY, WAVE_PAY
from helpers import generate_order_id, is_valid_mlbb_id, is_valid_screenshot, get_estimated_time
from languages import TEXT
import os

# States for ConversationHandler
NAME, LANG, MLBB_ID, CATEGORY, DIAMOND, SCREENSHOT = range(6)

user_data = {}
order_history = {}

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id] = {}

    await update.message.reply_text(TEXT["ask_name"])
    return NAME

# Save name
async def save_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id]["name"] = update.message.text

    keyboard = [
        [InlineKeyboardButton("🇲🇲 မြန်မာ", callback_data="mm")],
        [InlineKeyboardButton("🇬🇧 English", callback_data="eng")]
    ]
    await update.message.reply_text(TEXT["choose_lang"], reply_markup=InlineKeyboardMarkup(keyboard))
    return LANG

# Set language
async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = query.data

    user_data[user_id]["lang"] = lang
    await query.message.reply_text(TEXT["ask_mlbb_id"][lang])
    return MLBB_ID

# Save MLBB ID + Zone
async def save_mlbb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    lang = user_data[user_id]["lang"]
    if not is_valid_mlbb_id(text):
        await update.message.reply_text(TEXT["invalid_id"][lang])
        return MLBB_ID

    user_data[user_id]["mlbb_id"] = text
    # Category menu
    keyboard = [
        [InlineKeyboardButton("💎 Regular", callback_data="regular")],
        [InlineKeyboardButton("🔄 Weekly Pass", callback_data="weekly")],
        [InlineKeyboardButton("🎁 First Recharge Bonus", callback_data="bonus")]
    ]
    await update.message.reply_text(TEXT["choose_category"][lang], reply_markup=InlineKeyboardMarkup(keyboard))
    return CATEGORY

# Category selected
async def select_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    category = query.data
    user_id = query.from_user.id
    user_data[user_id]["category"] = category
    lang = user_data[user_id]["lang"]

    # Create diamond options based on selected category
    buttons = []
    for amount, price in PRICES[category].items():
        buttons.append([InlineKeyboardButton(f"{amount} ➤ {price} Ks", callback_data=amount)])
    await query.message.reply_text(TEXT["choose_diamond"][lang], reply_markup=InlineKeyboardMarkup(buttons))
    return DIAMOND

# Diamond selected
async def select_diamond(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    diamond = query.data
    user_id = query.from_user.id
    lang = user_data[user_id]["lang"]
    user_data[user_id]["diamond"] = diamond

    # Ask for payment screenshot
    await query.message.reply_text(TEXT["ask_screenshot"][lang])
    return SCREENSHOT

# Screenshot received
async def receive_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = user_data[user_id]["lang"]
    photo = update.message.photo[-1]
    file_id = photo.file_id

    if not is_valid_screenshot(update.message):
        await update.message.reply_text(TEXT["invalid_screenshot"][lang])
        return SCREENSHOT

    # Generate order
    order_id = generate_order_id()
    user_data[user_id]["order_id"] = order_id
    order_history.setdefault(user_id, []).append(order_id)

    summary = TEXT["order_summary"][lang].format(
        name=user_data[user_id]["name"],
        mlbb=user_data[user_id]["mlbb_id"],
        diamond=user_data[user_id]["diamond"],
        category=user_data[user_id]["category"].capitalize(),
        payment="KBZPay / WavePay",
        time=get_estimated_time(),
        order_id=order_id
    )

    # Send to user
    await update.message.reply_text(summary)

    # Send to admin group
    buttons = [
        [
            InlineKeyboardButton("✅ Approve", callback_data=f"approve_{order_id}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject_{order_id}")
        ]
    ]
    admin_text = f"🔔 New Order from @{update.effective_user.username or 'NoUsername'}\n"
    admin_text += f"Order ID: {order_id}\n"
    admin_text += f"MLBB ID: {user_data[user_id]['mlbb_id']}\n"
    admin_text += f"Diamonds: {user_data[user_id]['diamond']}"

    await context.bot.send_photo(
        chat_id=ADMIN_GROUP_ID,
        photo=file_id,
        caption=admin_text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

    return ConversationHandler.END

# Approve order
async def handle_approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    order_id = query.data.split("_")[1]
    await query.edit_message_caption(caption=f"✅ Order {order_id} approved.")

# Reject order - ask reason
async def handle_reject(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    order_id = query.data.split("_")[1]
    context.user_data["reject_order"] = order_id
    await query.message.reply_text("📌 Order ကို ငြင်းပယ်ရန် အကြောင်းပြချက်ရေးပါ:")
    return "REJECT_REASON"

# Handle reject reason
async def handle_reject_reason(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reason = update.message.text
    order_id = context.user_data.get("reject_order")
    await update.message.reply_text(f"❌ Order {order_id} has been rejected with reason: {reason}")
    return ConversationHandler.END

# Start app
import asyncio

async def main():

    app = Application.builder().token(BOT_TOKEN).build()

    # ✅ Set webhook manually
    await app.bot.set_webhook("https://nexamint-bot.onrender.com/webhook")

    # All your handlers
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME:     [MessageHandler(filters.TEXT & ~filters.COMMAND, save_name)],
            LANG:     [CallbackQueryHandler(set_language)],
            MLBB_ID:  [MessageHandler(filters.TEXT & ~filters.COMMAND, save_mlbb)],
            CATEGORY: [CallbackQueryHandler(select_category)],
            DIAMOND:  [CallbackQueryHandler(select_diamond)],
            SCREENSHOT: [MessageHandler(filters.PHOTO, receive_screenshot)],
            "REJECT_REASON": [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_reject_reason)],
        },
        fallbacks=[]
    )
    
    app.add_handler(conv_handler)
    app.add_handler(CallbackQueryHandler(handle_approve, pattern=r"^approve_"))
    app.add_handler(CallbackQueryHandler(handle_reject, pattern=r"^reject_"))

    # ✅ Start webhook server
    await app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_path="/webhook"
    )

if __name__ == "__main__":
    asyncio.run(main())

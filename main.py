import logging
from telegram import (
    Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters,
    CallbackQueryHandler, ContextTypes, ConversationHandler
)
from config import BOT_TOKEN, ADMIN_GROUP_ID, KBZ_PAY, WAVE_PAY, PRICES
from helpers import (
    validate_mlbb_id, generate_order_id, is_duplicate_order,
    save_order, get_order_status, get_last_orders, get_user_data,
    update_order_status, allowed_image
)
from languages import TEXT
from keep_alive import keep_alive

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# States
LANGUAGE, NAME, MLBB_ID, DIAMOND_AMOUNT, PAYMENT_SCREENSHOT, CONFIRM_ORDER = range(6)

# Memory data
user_lang = {}
user_data = {}

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    keyboard = [
        [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
         InlineKeyboardButton("🇲🇲 မြန်မာ", callback_data="lang_mm")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🌐 Please choose your language:", reply_markup=reply_markup)
    return LANGUAGE

# Language selection handler
async def handle_language_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "lang_en":
        user_lang[user_id] = "en"
        await query.edit_message_text(TEXT["en"]["language_changed"])
    else:
        user_lang[user_id] = "mm"
        await query.edit_message_text(TEXT["mm"]["language_changed"])

    # Ask for MLBB ID after language is set
    await context.bot.send_message(
        chat_id=query.message.chat.id,
        text=TEXT[user_lang[user_id]]["ask_mlbb_id"]
    )
    return MLBB_ID

# MLBB ID collection
async def collect_mlbb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    mlbb_input = update.message.text

    if not validate_mlbb_id(mlbb_input):
        await update.message.reply_text(TEXT[user_lang[user_id]]["invalid_mlbb"])
        return MLBB_ID

    user_data[user_id] = {"mlbb_id": mlbb_input}

    # Show categories
    keyboard = [
        [InlineKeyboardButton("💎 Regular", callback_data="category_regular")],
        [InlineKeyboardButton("🔄 Weekly Pass", callback_data="category_weekly")],
        [InlineKeyboardButton("🎁 First Recharge", callback_data="category_bonus")]
    ]
    await update.message.reply_text(TEXT[user_lang[user_id]]["select_category"],
                                    reply_markup=InlineKeyboardMarkup(keyboard))
    return DIAMOND_AMOUNT

# Category selection handler
async def handle_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    category = query.data.replace("category_", "")

    user_data[user_id]["category"] = category

    buttons = []
    for amount, price in PRICES[category].items():
        buttons.append([InlineKeyboardButton(f"{amount} ➡️ {price} Ks",
                                             callback_data=f"amount_{amount}")])

    await query.edit_message_text(TEXT[user_lang[user_id]]["choose_diamond"],
                                  reply_markup=InlineKeyboardMarkup(buttons))
    return DIAMOND_AMOUNT

# Diamond amount selection handler
async def handle_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    amount = query.data.replace("amount_", "")
    user_data[user_id]["amount"] = amount
    user_data[user_id]["price"] = PRICES[user_data[user_id]["category"]][amount]

    msg = TEXT[user_lang[user_id]]["upload_screenshot"].format(
        kbz=KBZ_PAY, wave=WAVE_PAY
    )
    await query.edit_message_text(msg)
    return PAYMENT_SCREENSHOT

# Payment screenshot handler
async def handle_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not update.message.photo:
        await update.message.reply_text(TEXT[user_lang[user_id]]["invalid_screenshot"])
        return PAYMENT_SCREENSHOT

    file_id = update.message.photo[-1].file_id
    user_data[user_id]["screenshot"] = file_id

    # Summary
    mlbb = user_data[user_id]["mlbb_id"]
    amount = user_data[user_id]["amount"]
    price = user_data[user_id]["price"]

    summary = TEXT[user_lang[user_id]]["confirm_order"].format(
        mlbb=mlbb, amount=amount, price=price
    )

    keyboard = [
        [InlineKeyboardButton(TEXT[user_lang[user_id]]["confirm_btn"], callback_data="confirm")],
        [InlineKeyboardButton(TEXT[user_lang[user_id]]["cancel_btn"], callback_data="cancel")]
    ]
    await update.message.reply_text(summary, reply_markup=InlineKeyboardMarkup(keyboard))
    return CONFIRM_ORDER

# Confirm order handler
async def handle_order_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "cancel":
        await query.edit_message_text(TEXT[user_lang[user_id]]["order_cancelled"])
        return ConversationHandler.END

    # Check duplicate
    if is_duplicate_order(user_id):
        await query.edit_message_text(TEXT[user_lang[user_id]]["duplicate_order"])
        return ConversationHandler.END

    # Save order
    order_id = generate_order_id()
    user_data[user_id]["order_id"] = order_id
    save_order(user_id, user_data[user_id])

    # Send to admin group
    caption = f"🔔 New Order from @{query.from_user.username or query.from_user.first_name}\n\n"
    caption += f"🆔 Order ID: {order_id}\n🎮 MLBB ID: {user_data[user_id]['mlbb_id']}\n💎 Diamonds: {user_data[user_id]['amount']}\n💰 Price: {user_data[user_id]['price']} Ks\n\n⏳ Status: Pending"

    keyboard = [
        [InlineKeyboardButton("✅ Approve", callback_data=f"approve_{order_id}"),
         InlineKeyboardButton("❌ Reject", callback_data=f"reject_{order_id}")]
    ]

    await context.bot.send_photo(
        chat_id=ADMIN_GROUP_ID,
        photo=user_data[user_id]["screenshot"],
        caption=caption,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    await query.edit_message_text(TEXT[user_lang[user_id]]["order_success"].format(order_id=order_id))
    return ConversationHandler.END

# Admin approval handler
async def admin_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action, order_id = query.data.split("_", 1)
    if action == "approve":
        update_order_status(order_id, "Completed")
        await query.edit_message_caption(
            caption=query.message.caption + "\n✅ Status: Completed"
        )
    elif action == "reject":
        update_order_status(order_id, "Rejected")
        await query.edit_message_caption(
            caption=query.message.caption + "\n❌ Status: Rejected"
        )

# /checkorder command
async def check_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = user_lang.get(user_id, "en")
    result = get_order_status(user_id)
    await update.message.reply_text(TEXT[lang]["order_status"].format(status=result))

# /orders command
async def last_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = user_lang.get(user_id, "en")
    orders = get_last_orders(user_id)
    if not orders:
        await update.message.reply_text(TEXT[lang]["no_orders"])
    else:
        await update.message.reply_text("\n\n".join(orders))

# /help command
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = user_lang.get(user_id, "en")
    await update.message.reply_text(TEXT[lang]["help"])

def main():
    keep_alive()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANGUAGE: [CallbackQueryHandler(handle_language_selection, pattern="^lang_")],
            MLBB_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, collect_mlbb)],
            DIAMOND_AMOUNT: [CallbackQueryHandler(handle_category, pattern="^category_"),
                             CallbackQueryHandler(handle_amount, pattern="^amount_")],
            PAYMENT_SCREENSHOT: [MessageHandler(filters.PHOTO, handle_screenshot)],
            CONFIRM_ORDER: [CallbackQueryHandler(handle_order_confirmation, pattern="^(confirm|cancel)$")],
        },
        fallbacks=[],
        allow_reentry=True
    )

    app.add_handler(conv)
    app.add_handler(CommandHandler("checkorder", check_order))
    app.add_handler(CommandHandler("orders", last_orders))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CallbackQueryHandler(admin_action, pattern="^(approve|reject)_"))

    app.run_polling()

if __name__ == "__main__":
    main()

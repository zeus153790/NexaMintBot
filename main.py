# main.py
from keep_alive import keep_alive

keep_alive()

from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, InputMediaPhoto
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler,
    ContextTypes, filters, ConversationHandler
)
from config import BOT_TOKEN, ADMIN_GROUP_ID, DIAMOND_PRICES, KBZ_PAY_NUMBER, WAVE_PAY_NUMBER
from languages import texts
from helpers import (
    is_valid_mlbb_id, generate_order_id, get_message, format_package
)

# === TEMP DATA ===
user_data = {}         # Stores user name, language, MLBB ID, etc.
user_orders = {}       # Stores current order info per user
pending_orders = {}    # Track order status

# === STATES ===
NAME, LANG, MLBB_ID, CATEGORY, DIAMOND, SCREENSHOT = range(6)

# === /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id] = {"lang": "mm"}  # Default to MM
    await update.message.reply_text(texts["start"]["mm"])
    return NAME

# === Save Name ===
async def save_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    name = update.message.text
    user_data[user_id]["name"] = name

    keyboard = [
        [InlineKeyboardButton("🇲🇲 မြန်မာ", callback_data="lang_mm"),
         InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")]
    ]
    await update.message.reply_text(
        texts["language_choose"]["mm"],
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return LANG

# === Set Language ===
async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    lang = "mm" if "mm" in query.data else "en"
    user_data[user_id]["lang"] = lang

    msg = get_message(lang, texts["language_changed"])
    await query.edit_message_text(msg)
    msg2 = get_message(lang, texts["name_saved"])
    await context.bot.send_message(user_id, msg2)
    return MLBB_ID

# === Validate MLBB ID ===
async def save_mlbb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    lang = user_data[user_id]["lang"]

    if not is_valid_mlbb_id(text):
        msg = get_message(lang, texts["invalid_mlbb"])
        await update.message.reply_text(msg)
        return MLBB_ID

    user_data[user_id]["mlbb"] = text
    msg = get_message(lang, texts["mlbb_saved"])
    keyboard = [
        [InlineKeyboardButton("💎 Regular", callback_data="cat_regular")],
        [InlineKeyboardButton("🔄 Weekly Pass", callback_data="cat_weekly")],
        [InlineKeyboardButton("🎁 Bonus", callback_data="cat_bonus")]
    ]
    await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(keyboard))
    return CATEGORY

# === Handle Category Selection ===
async def select_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = user_data[user_id]["lang"]

    category = query.data.replace("cat_", "")
    user_data[user_id]["category"] = category

    # Show available diamonds
    options = []
    for k in DIAMOND_PRICES:
        if category == "regular" and isinstance(k, int):
            options.append([InlineKeyboardButton(f"{k} 💎 - {DIAMOND_PRICES[k]} Ks", callback_data=f"diamond_{k}")])
        elif category == "weekly" and k == "weekly":
            options.append([InlineKeyboardButton("🔄 Weekly Pass - 6500 Ks", callback_data="diamond_weekly")])
        elif category == "bonus" and "+" in str(k):
            options.append([InlineKeyboardButton(f"{k} 🎁 - {DIAMOND_PRICES[k]} Ks", callback_data=f"diamond_{k}")])

    msg = get_message(lang, texts["choose_diamond_amount"])
    await query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(options))
    return DIAMOND

# === Select Diamond Amount ===
async def select_diamond(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = user_data[user_id]["lang"]

    diamond = query.data.replace("diamond_", "")
    user_data[user_id]["diamond"] = diamond
    price = DIAMOND_PRICES.get(int(diamond)) if diamond.isdigit() else DIAMOND_PRICES.get(diamond)

    msg = get_message(lang, texts["show_price"]).format(price=price)
    await query.edit_message_text(msg)

    msg2 = get_message(lang, texts["upload_screenshot"])
    await context.bot.send_message(user_id, msg2)
    return SCREENSHOT

# === Receive Screenshot ===
async def receive_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = user_data[user_id]["lang"]
    username = update.effective_user.username or update.effective_user.first_name
    photo = update.message.photo[-1]

    # Generate Order
    order_id = generate_order_id()
    user_orders[user_id] = {
        "order_id": order_id,
        "status": "Pending",
        "screenshot": photo.file_id,
        "diamond": user_data[user_id]["diamond"]
    }

    msg = get_message(lang, texts["confirming_order"])
    await update.message.reply_text(msg)

    # Send to Admin Group
    diamond_label = format_package(user_data[user_id]["diamond"])
    mlbb_id = user_data[user_id].get("mlbb", "N/A")
    notify_msg = get_message(lang, texts["new_order_admin"]).format(
        username=f"@{username}",
        mlbb=mlbb_id,
        diamond=diamond_label,
        order_id=order_id
    )

    buttons = [
        [InlineKeyboardButton("✅ Approve", callback_data=f"approve_{order_id}"),
         InlineKeyboardButton("❌ Reject", callback_data=f"reject_{order_id}")]
    ]

    await context.bot.send_photo(
        chat_id=ADMIN_GROUP_ID,
        photo=photo.file_id,
        caption=notify_msg,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

    msg2 = get_message(lang, texts["order_sent"])
    await update.message.reply_text(msg2)
    pending_orders[order_id] = user_id
    return ConversationHandler.END

# === Handle Admin Approve/Reject ===
async def handle_admin_decision(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    order_id = data.split("_")[1]
    user_id = pending_orders.get(order_id)

    if "approve" in data:
        # Update user
        lang = user_data[user_id]["lang"]
        msg = get_message(lang, texts["order_approved"])
        await context.bot.send_message(user_id, msg)
        await query.edit_message_caption(query.message.caption + "\n✅ Approved")
    elif "reject" in data:
        await context.bot.send_message(
            chat_id=query.from_user.id,
            text=get_message("mm", texts["ask_rejection_reason"])  # Only admin language
        )
        context.user_data["reject_order_id"] = order_id
    return

# === Capture Rejection Reason ===
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "reject_order_id" in context.user_data:
        order_id = context.user_data.pop("reject_order_id")
        user_id = pending_orders.get(order_id)
        reason = update.message.text
        lang = user_data[user_id]["lang"]

        # Notify user
        msg = get_message(lang, texts["order_rejected"]).format(reason=reason)
        await context.bot.send_message(user_id, msg)

        # Update admin group message manually
        await update.message.reply_text(
            get_message(lang, texts["order_rejected_admin"]).format(order_id=order_id, reason=reason)
        )
    return

# === /checkorder ===
async def check_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = user_data.get(user_id, {}).get("lang", "mm")
    order = user_orders.get(user_id)

    if not order:
        msg = get_message(lang, texts["no_order_found"])
    else:
        msg = get_message(lang, texts["order_status"]).format(
            order_id=order["order_id"],
            diamond=format_package(order["diamond"]),
            status=order["status"]
        )
    await update.message.reply_text(msg)

# === /orders ===
async def list_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = user_data.get(user_id, {}).get("lang", "mm")
    order = user_orders.get(user_id)

    if not order:
        await update.message.reply_text(get_message(lang, texts["no_order_found"]))
    else:
        text = get_message(lang, texts["order_history_title"]) + "\n\n"
        text += f"🆔 {order['order_id']}\n💎 {format_package(order['diamond'])}\n📌 Status: {order['status']}"
        await update.message.reply_text(text)

# === /help ===
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = user_data.get(user_id, {}).get("lang", "mm")
    msg = get_message(lang, texts["help"])
    await update.message.reply_text(msg)

# === Admin Commands ===
async def pendingorders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not pending_orders:
        await update.message.reply_text("✅ No pending orders.")
        return
    await update.message.reply_text(texts["pendingorders_admin"]["mm"])
    for oid in pending_orders:
        await update.message.reply_text(f"🆔 {oid}")

async def complete_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text("⚠️ Usage: /completeorder NXM-0001")
        return
    order_id = args[0]
    user_id = pending_orders.pop(order_id, None)
    if user_id:
        user_orders[user_id]["status"] = "Completed"
        lang = user_data[user_id]["lang"]
        msg = get_message(lang, texts["order_approved"])
        await context.bot.send_message(user_id, msg)
        await update.message.reply_text(texts["order_completed_admin"]["mm"].format(order_id=order_id))

async def reject_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text("⚠️ Usage: /rejectorder NXM-0001")
        return
    order_id = args[0]
    user_id = pending_orders.pop(order_id, None)
    if user_id:
        await update.message.reply_text("📌 Now reply with the reason.")
        context.user_data["reject_order_id"] = order_id

# === Main Bot Setup ===
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_name)],
            LANG: [CallbackQueryHandler(set_language)],
            MLBB_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_mlbb)],
            CATEGORY: [CallbackQueryHandler(select_category)],
            DIAMOND: [CallbackQueryHandler(select_diamond)],
            SCREENSHOT: [MessageHandler(filters.PHOTO, receive_screenshot)]
        },
        fallbacks=[]
    )

    app.add_handler(conv_handler)
    app.add_handler(CallbackQueryHandler(handle_admin_decision))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(CommandHandler("checkorder", check_order))
    app.add_handler(CommandHandler("orders", list_orders))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("pendingorders", pendingorders))
    app.add_handler(CommandHandler("completeorder", complete_order))
    app.add_handler(CommandHandler("rejectorder", reject_order))

    app.run_polling()

import os

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080))
    )


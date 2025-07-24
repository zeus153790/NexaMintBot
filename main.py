import logging
import re
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ConversationHandler
)
from config import BOT_TOKEN, ADMIN_GROUP_ID, ORDER_STATUS, DIAMOND_PRICES
import languages
import helpers
from datetime import datetime

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
NAME, LANGUAGE, MAIN_MENU, MLBB_ID, CATEGORY, PACKAGE, PAYMENT, CONFIRM_ORDER = range(8)
ADMIN_REJECT_REASON = 9

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_data = helpers.get_user_data(user.id)

    if user_data:
        lang = user_data.get('language', 'en')
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=languages.LANGUAGES[lang]['main_menu'].format(user_data['name']),
            reply_markup=main_menu_keyboard(lang)
        )
        return MAIN_MENU
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=languages.LANGUAGES['en']['welcome'])
        
        return NAME

# Name handler
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text
    context.user_data['name'] = name

    keyboard = [
        [
            InlineKeyboardButton("🇲🇲 Myanmar", callback_data='my'),
            InlineKeyboardButton("🇬🇧 English", callback_data='en')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        languages.LANGUAGES['en']['lang_select'],
        reply_markup=reply_markup
    )
    return LANGUAGE

# Language handler
async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    language = query.data

    user = query.from_user
    user_data = {
        'id': user.id,
        'name': context.user_data['name'],
        'language': language,
        'username': user.username
    }
    helpers.save_user_data(user.id, user_data)

    await query.edit_message_text(
        text=languages.LANGUAGES[language]['main_menu'].format(user_data['name']),
        reply_markup=main_menu_keyboard(language)
    )
    return MAIN_MENU

# Main menu keyboard
def main_menu_keyboard(lang):
    keyboard = [
        [InlineKeyboardButton("💎 Order Diamonds", callback_data='order')],
        [InlineKeyboardButton("📦 Check Order", callback_data='check_order')],
        [InlineKeyboardButton("📜 My Orders", callback_data='my_orders')],
        [InlineKeyboardButton("❓ Help", callback_data='help')]
    ]
    return InlineKeyboardMarkup(keyboard)

# Start order process
async def start_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_data = helpers.get_user_data(query.from_user.id)
    lang = user_data['language']

    if 'mlbb_id' in user_data and user_data['mlbb_id']:
        keyboard = [
            [
                InlineKeyboardButton("✅ Use Saved", callback_data='use_saved'),
                InlineKeyboardButton("🆕 New ID", callback_data='new_id')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=f"Use saved MLBB ID: {user_data['mlbb_id']}?",
            reply_markup=reply_markup
        )
        return MLBB_ID  # Stay in the order flow
    else:
        await query.edit_message_text(languages.LANGUAGES[lang]['enter_mlbb'])
        return MLBB_ID

# Handle saved ID choice
async def handle_saved_id_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    choice = query.data
    user_id = query.from_user.id
    user_data = helpers.get_user_data(user_id)
    lang = user_data['language']

    if choice == 'use_saved':
        # Proceed to category selection
        keyboard = [
            [
                InlineKeyboardButton(
                    languages.LANGUAGES[lang]['category_regular'], 
                    callback_data='regular'
                ),
                InlineKeyboardButton(
                    languages.LANGUAGES[lang]['category_weekly'], 
                    callback_data='weekly'
                )
            ],
            [
                InlineKeyboardButton(
                    languages.LANGUAGES[lang]['category_bonus'], 
                    callback_data='bonus'
                )
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            languages.LANGUAGES[lang]['diamond_category'],
            reply_markup=reply_markup
        )
        return CATEGORY
    else:  # new_id
        await query.edit_message_text(languages.LANGUAGES[lang]['enter_mlbb'])
        return MLBB_ID

# MLBB ID handler
async def get_mlbb_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if this is a callback from the saved ID choice
    if update.callback_query:
        return await handle_saved_id_choice(update, context)

    # It's a text message with new ID
    text = update.message.text
    user_id = update.message.from_user.id
    user_data = helpers.get_user_data(user_id)
    lang = user_data['language']

    if not helpers.validate_mlbb(text):
        await update.message.reply_text(languages.LANGUAGES[lang]['invalid_mlbb'])
        return MLBB_ID

    # Save MLBB ID for future orders
    user_data['mlbb_id'] = text
    helpers.save_user_data(user_id, user_data)

    # Create category buttons with proper mapping
    keyboard = [
        [
            InlineKeyboardButton(
                languages.LANGUAGES[lang]['category_regular'], 
                callback_data='regular'
            ),
            InlineKeyboardButton(
                languages.LANGUAGES[lang]['category_weekly'], 
                callback_data='weekly'
            )
        ],
        [
            InlineKeyboardButton(
                languages.LANGUAGES[lang]['category_bonus'], 
                callback_data='bonus'
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        languages.LANGUAGES[lang]['diamond_category'],
        reply_markup=reply_markup
    )
    return CATEGORY

# Category handler
async def select_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    category = query.data

    if category not in DIAMOND_PRICES:
        user_data = helpers.get_user_data(query.from_user.id)
        lang = user_data['language']
        await query.edit_message_text(languages.LANGUAGES[lang]['invalid_category'])
        return CATEGORY

    context.user_data['category'] = category

    user_data = helpers.get_user_data(query.from_user.id)
    lang = user_data['language']

    # Get packages for selected category
    packages = list(DIAMOND_PRICES[category].keys())
    keyboard = helpers.create_keyboard(packages)

    await query.edit_message_text(
        text=languages.LANGUAGES[lang]['choose_package'],
        reply_markup=keyboard
    )
    return PACKAGE

# Package handler
async def select_package(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    package = query.data
    category = context.user_data['category']

    # Save package and calculate price
    context.user_data['package'] = package
    context.user_data['price'] = helpers.get_diamond_price(category, package)

    user_data = helpers.get_user_data(query.from_user.id)
    lang = user_data['language']

    await query.edit_message_text(
        text=languages.LANGUAGES[lang]['upload_payment']
    )
    return PAYMENT

# Payment screenshot handler
async def get_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # For simplicity, skipping validation per request
    context.user_data['payment_photo'] = update.message.photo[-1].file_id

    user_id = update.message.from_user.id
    user_data = helpers.get_user_data(user_id)
    lang = user_data['language']

    # Generate order summary
    order_id = helpers.generate_order_id()
    context.user_data['order_id'] = order_id

    order_summary = languages.LANGUAGES[lang]['order_confirm'].format(
        order_id,
        context.user_data['package'],
        helpers.format_price(context.user_data['price'])
    )

    keyboard = [
        [
            InlineKeyboardButton("✅ Confirm", callback_data='confirm_order'),
            InlineKeyboardButton("❌ Cancel", callback_data='cancel_order')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=context.user_data['payment_photo'],
        caption=order_summary,
        reply_markup=reply_markup
    )
    return CONFIRM_ORDER

# Order confirmation
async def confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    user_data = helpers.get_user_data(user_id)
    lang = user_data['language']

    # Save order
    order = {
        'order_id': context.user_data['order_id'],
        'user_id': user_id,
        'mlbb_id': user_data['mlbb_id'],
        'category': context.user_data['category'],
        'package': context.user_data['package'],
        'price': context.user_data['price'],
        'payment_photo': context.user_data['payment_photo'],
        'status': ORDER_STATUS['pending'],
        'date': datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    helpers.save_order(order)

    # Notify admin
    admin_text = languages.LANGUAGES['en']['admin_notification'].format(
        f"@{user_data['username']}" if user_data['username'] else user_data['name'],
        order['order_id'],
        order['mlbb_id'],
        order['package'],
        helpers.format_price(order['price'])
    )

    keyboard = [
        [
            InlineKeyboardButton("✅ Approve", callback_data=f"approve_{order['order_id']}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject_{order['order_id']}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_photo(
        chat_id=ADMIN_GROUP_ID,
        photo=order['payment_photo'],
        caption=admin_text,
        reply_markup=reply_markup
    )

    # Confirm to user
    await query.edit_message_caption(
        caption=languages.LANGUAGES[lang]['order_success']
    )
    return ConversationHandler.END

# Cancel order
async def cancel_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    user_data = helpers.get_user_data(user_id)
    lang = user_data['language']

    # Create cancel message based on language
    cancel_message = "🛑 Order cancelled!" if lang == 'en' else "🛑 အော်ဒါ ပယ်ဖျက်ပြီးပါပြီ!"

    await query.edit_message_caption(
        caption=cancel_message
    )
    return ConversationHandler.END

# Admin approve order
async def admin_approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    order_id = query.data.split('_')[1]

    helpers.update_order_status(order_id, ORDER_STATUS['paid'])

    order = helpers.get_order(order_id)
    user_data = helpers.get_user_data(order['user_id'])
    lang = user_data['language']

    # Notify user
    await context.bot.send_message(
        chat_id=order['user_id'],
        text=f"✅ Your order {order_id} has been approved! Diamonds will be delivered soon."
    )

    await query.edit_message_caption(
        caption=f"✅ Order {order_id} approved"
    )

# Admin reject order
async def admin_reject(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    order_id = query.data.split('_')[1]
    context.user_data['reject_order_id'] = order_id

    await query.edit_message_caption(
        caption=languages.LANGUAGES['en']['reject_reason']
    )
    return ADMIN_REJECT_REASON

# Admin reject reason handler
async def reject_reason(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reason = update.message.text
    order_id = context.user_data['reject_order_id']

    helpers.update_order_status(order_id, ORDER_STATUS['rejected'], reason)

    order = helpers.get_order(order_id)
    user_data = helpers.get_user_data(order['user_id'])
    lang = user_data['language']

    # Notify user
    await context.bot.send_message(
        chat_id=order['user_id'],
        text=languages.LANGUAGES[lang]['order_rejected'].format(order_id, reason)
    )

    await update.message.reply_text(
        text=languages.LANGUAGES['en']['order_rejected'].format(order_id, reason)
    )
    return ConversationHandler.END

# Check order command
async def check_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data = helpers.get_user_data(user_id)
    lang = user_data['language']

    orders = helpers.get_user_orders(user_id)
    if not orders:
        await update.message.reply_text(languages.LANGUAGES[lang]['no_orders'])
        return

    # Get latest order
    latest_order = sorted(orders, key=lambda x: x['date'], reverse=True)[0]

    response = languages.LANGUAGES[lang]['order_details'].format(
        latest_order['order_id'],
        latest_order['status'],
        latest_order['package'],
        helpers.format_price(latest_order['price']),
        latest_order['date']
    )

    await update.message.reply_text(response)

# My orders command
async def my_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data = helpers.get_user_data(user_id)
    lang = user_data['language']

    orders = helpers.get_user_orders(user_id)[-5:]  # Last 5 orders
    if not orders:
        await update.message.reply_text(languages.LANGUAGES[lang]['no_orders'])
        return

    response = "📦 Your Last Orders:\n\n"
    for order in orders:
        response += languages.LANGUAGES[lang]['order_details'].format(
            order['order_id'],
            order['status'],
            order['package'],
            helpers.format_price(order['price']),
            order['date']
        ) + "\n\n"

    await update.message.reply_text(response)

# Help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data = helpers.get_user_data(user_id)
    lang = user_data['language']

    # Add your username to help text
    help_text = languages.LANGUAGES[lang]['help_text'].replace(
        "@NexaMintSupport", 
        "@Terror_come"
    )

    await update.message.reply_text(
        help_text,
        disable_web_page_preview=True
    )

# Handle main menu callbacks
async def handle_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    user_data = helpers.get_user_data(user_id)
    lang = user_data['language']

    if query.data == 'check_order':
        await check_order_callback(update, context)
    elif query.data == 'my_orders':
        await my_orders_callback(update, context)
    elif query.data == 'help':
        await help_callback(update, context)
    return MAIN_MENU

# Check order callback
async def check_order_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    user_data = helpers.get_user_data(user_id)
    lang = user_data['language']

    orders = helpers.get_user_orders(user_id)
    if not orders:
        await query.edit_message_text(
            text=languages.LANGUAGES[lang]['no_orders'],
            reply_markup=main_menu_keyboard(lang)
        )
        return

    # Get latest order
    latest_order = sorted(orders, key=lambda x: x['date'], reverse=True)[0]

    response = languages.LANGUAGES[lang]['order_details'].format(
        latest_order['order_id'],
        latest_order['status'],
        latest_order['package'],
        helpers.format_price(latest_order['price']),
        latest_order['date']
    )

    await query.edit_message_text(
        text=response,
        reply_markup=main_menu_keyboard(lang)
    )

# My orders callback
async def my_orders_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    user_data = helpers.get_user_data(user_id)
    lang = user_data['language']

    orders = helpers.get_user_orders(user_id)[-5:]  # Last 5 orders
    if not orders:
        await query.edit_message_text(
            text=languages.LANGUAGES[lang]['no_orders'],
            reply_markup=main_menu_keyboard(lang)
        )
        return

    response = "📦 Your Last Orders:\n\n"
    for order in orders:
        response += languages.LANGUAGES[lang]['order_details'].format(
            order['order_id'],
            order['status'],
            order['package'],
            helpers.format_price(order['price']),
            order['date']
        ) + "\n\n"

    await query.edit_message_text(
        text=response,
        reply_markup=main_menu_keyboard(lang)
    )

# Help callback
async def help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    user_data = helpers.get_user_data(user_id)
    lang = user_data['language']

    # Add your username to help text
    help_text = languages.LANGUAGES[lang]['help_text'].replace(
        "@NexaMintSupport", 
        "@Terror_come"
    )

    await query.edit_message_text(
        text=help_text,
        reply_markup=main_menu_keyboard(lang),
        disable_web_page_preview=True
    )

# Admin pending orders
async def pending_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != ADMIN_GROUP_ID:
        return

    orders = helpers.get_pending_orders()
    if not orders:
        await update.message.reply_text("No pending orders")
        return

    response = languages.LANGUAGES['en']['pending_orders'] + "\n\n"
    for order in orders:
        response += f"Order ID: {order['order_id']}\n"
        response += f"User: {order['user_id']}\n"
        response += f"Diamonds: {order['package']}\n"
        response += f"Price: {helpers.format_price(order['price'])} MMK\n\n"

    await update.message.reply_text(response)

# Admin complete order
async def complete_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != ADMIN_GROUP_ID:
        return

    try:
        order_id = context.args[0]
        if helpers.update_order_status(order_id, ORDER_STATUS['completed']):
            order = helpers.get_order(order_id)
            user_data = helpers.get_user_data(order['user_id'])
            lang = user_data['language']

            # Notify user
            await context.bot.send_message(
                chat_id=order['user_id'],
                text=languages.LANGUAGES[lang]['order_completed'].format(order_id)
            )

            await update.message.reply_text(
                languages.LANGUAGES['en']['order_completed'].format(order_id)
            )
        else:
            await update.message.reply_text(
                languages.LANGUAGES['en']['order_not_found']
            )
    except IndexError:
        await update.message.reply_text("Usage: /completeorder NXM-0001")

# Main function
def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Conversation handler for customer flow
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            LANGUAGE: [CallbackQueryHandler(set_language)],
            MAIN_MENU: [
                CallbackQueryHandler(start_order, pattern='^order$'),
                CallbackQueryHandler(handle_main_menu, pattern='^(check_order|my_orders|help)$')
            ],
            MLBB_ID: [
                CallbackQueryHandler(get_mlbb_id, pattern='^use_saved|new_id$'),
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_mlbb_id)
            ],
            CATEGORY: [CallbackQueryHandler(select_category)],
            PACKAGE: [CallbackQueryHandler(select_package)],
            PAYMENT: [MessageHandler(filters.PHOTO, get_payment)],
            CONFIRM_ORDER: [
                CallbackQueryHandler(confirm_order, pattern='^confirm_order$'),
                CallbackQueryHandler(cancel_order, pattern='^cancel_order$')
            ]
        },
        fallbacks=[]
    )

    application.add_handler(conv_handler)

    # Admin handlers
    application.add_handler(CommandHandler('pendingorders', pending_orders))
    application.add_handler(CommandHandler('completeorder', complete_order))

    # Callback handlers
    application.add_handler(CallbackQueryHandler(admin_approve, pattern=r'^approve_'))
    application.add_handler(CallbackQueryHandler(admin_reject, pattern=r'^reject_'))

    # Command handlers
    application.add_handler(CommandHandler('checkorder', check_order))
    application.add_handler(CommandHandler('orders', my_orders))
    application.add_handler(CommandHandler('help', help_command))

    # Rejection reason handler
    rejection_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(admin_reject, pattern=r'^reject_')],
        states={
            ADMIN_REJECT_REASON: [MessageHandler(filters.TEXT & ~filters.COMMAND, reject_reason)]
        },
        fallbacks=[]
    )
    application.add_handler(rejection_handler)

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()

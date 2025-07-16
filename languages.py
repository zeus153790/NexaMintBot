# languages.py

TEXT = {
    "en": {
        "welcome":
        "👋 Welcome to NexaMint!\nPlease enter your name to get started:",
        "name_saved":
        "✅ Thanks, {name}! Use the menu below to start ordering.",
        "ask_mlbb_id": "📱 Enter your MLBB ID (e.g. 12345678 (1234)):",
        "choose_category": "📦 Choose a category:",
        "choose_diamond": "💎 Choose diamond amount:",
        "price_display":
        "💰 Price for {amount} diamonds is {price:,} MMK.\nUpload your KBZPay or WavePay screenshot to continue:",
        "invalid_id":
        "⚠️ Invalid MLBB ID or Zone. Please enter valid numbers.",
        "invalid_screenshot":
        "❌ Please send a valid payment screenshot (KBZPay or WavePay).",
        "order_confirmed":
        "📨 Your order has been submitted!\nOrder ID: {order_id}\nWe'll process it shortly.",
        "order_summary":
        "📝 Order Summary:\nOrder ID: {order_id}\nDiamonds: {diamonds}\nMLBB: {mlbb_id} ({zone})\nPrice: {price:,} MMK\n⏳ Delivery: {delivery_time}",
        "check_order": "🔍 Enter your Order ID (e.g., NXM-0001):",
        "order_status": "📦 Order Status:\nStatus: {status}",
        "no_order_found": "❌ No order found with that ID.",
        "order_history": "🕓 Your last 5 orders:\n\n{history}",
        "no_orders": "You haven't placed any orders yet.",
        "help":
        "📖 *FAQ*\n\n💰 *Payment*: Use KBZPay or WavePay only.\n⏳ *Delivery*: Usually 5–15 minutes after payment.\n👨‍💼 *Admin Contact*: @Terror_come\n\nNeed help? Just message us!",

        # 🔧 Required extra keys
        "language_changed": "✅ Language set to English!\n\n👨‍💼 *Admin Contact*: @Terror_come\nNeed help? Just message us!",
        "invalid_mlbb": "❌ Invalid MLBB ID. Use format: 12345678 (1234)",
        "select_category": "📦 Choose your diamond top-up category:",
        "choose_diamond": "💎 Choose the diamond amount:",
        "upload_screenshot":
        "📸 Upload your KBZPay or WavePay screenshot to proceed.\n\nKBZPay: {kbz}\nWavePay: {wave}",
        "confirm_order":
        "📝 Confirm your order:\nMLBB ID: {mlbb}\nDiamonds: {amount}\nPrice: {price:,} MMK",
        "confirm_btn": "✅ Confirm",
        "cancel_btn": "❌ Cancel",
        "order_cancelled": "❌ Your order has been cancelled.",
        "duplicate_order":
        "⚠️ You've already placed an order recently. Please wait a few minutes.",
        "order_success": "✅ Order placed successfully!\nOrder ID: {order_id}"
    },
    "mm": {
        "welcome": "👋 NexaMint မှကြိုဆိုပါတယ်။\nစတင်ရန်အတွက်နာမည်ထည့်ပေးပါ:",
        "name_saved":
        "✅ ကျေးဇူးတင်ပါတယ် {name}။ အောက်ကမီနူးကိုသုံးပြီးအော်ဒါမှာနိုင်ပါတယ်။",
        "ask_mlbb_id": "📱 သင့် MLBB ID ကိုထည့်ပါ (ဥပမာ - 12345678 (1234)):",
        "choose_category": "📦 ကဏ္ဍရွေးချယ်ပါ:",
        "choose_diamond": "💎 စျေးနှုန်းကြည့်မယ်:",
        "price_display":
        "💰 {amount} ရတနာအတွက်စျေးနှုန်းမှာ {price:,} ကျပ် ဖြစ်ပါတယ်။\nKBZPay သို့မဟုတ် WavePay ငွေပေးချေမှု screenshot တင်ပါ:",
        "invalid_id": "⚠️ မမှန်ကန်သော MLBB ID သို့မဟုတ် Zone ဖြစ်ပါတယ်။",
        "invalid_screenshot":
        "❌ KBZPay သို့မဟုတ် WavePay screenshot တင်ပေးပါ။",
        "order_confirmed":
        "📨 သင့်အော်ဒါတင်ပြီးပါပြီ!\nOrder ID: {order_id}\nမကြာမီလုပ်ဆောင်ပေးပါမည်။",
        "order_summary":
        "📝 အော်ဒါအကျဉ်းချုပ်:\nOrder ID: {order_id}\nရတနာ: {diamonds}\nMLBB: {mlbb_id} ({zone})\nစျေး: {price:,} ကျပ်\n⏳ ရနိုင်ချိန်: {delivery_time}",
        "check_order": "🔍 Order ID (ဥပမာ - NXM-0001) ရိုက်ထည့်ပါ:",
        "order_status": "📦 အော်ဒါအခြေအနေ:\nအခြေအနေ: {status}",
        "no_order_found": "❌ ဒီအော်ဒါID မရှိပါ။",
        "order_history": "🕓 နောက်ဆုံး ၅ ခုအော်ဒါများ:\n\n{history}",
        "no_orders": "သင်မှာပြီးတဲ့အော်ဒါမရှိသေးပါ။",
        "help":
        "📖 *အမေးများသောမေးခွန်းများ*\n\n💰 *ငွေပေးချေမှု*: KBZPay / WavePay သာလက်ခံပါသည်။\n⏳ *ပေးပို့ချိန်*: ငွေပေးချေပြီးနောက် 5–15 မိနစ်အတွင်း။\n👨‍💼 *Admin*: @Terror_come\n\nအကူအညီလိုပါက ဆက်သွယ်ပါ။",

        # 🔧 Required extra keys
        "language_changed": "✅ မြန်မာဘာသာသို့ပြောင်းပြီးပါပြီ!\n\n👨‍💼 *Admin*: @Terror_come\nအကူအညီလိုပါက ဆက်သွယ်ပါ။",
        "invalid_mlbb": "❌ မှန်ကန်သော MLBB ID မဟုတ်ပါ။ ဥပမာ - 12345678 (1234)",
        "select_category": "📦 Diamond ကဏ္ဍရွေးချယ်ပါ:",
        "choose_diamond": "💎 ရတနာအရေအတွက်ရွေးပါ:",
        "upload_screenshot":
        "📸 KBZPay သို့မဟုတ် WavePay screenshot တင်ပါ။\n\nKBZPay: {kbz}\nWavePay: {wave}",
        "confirm_order":
        "📝 အော်ဒါအတည်ပြုရန်:\nMLBB ID: {mlbb}\nရတနာ: {amount}\nစျေးနှုန်း: {price:,} ကျပ်",
        "confirm_btn": "✅ အတည်ပြုမည်",
        "cancel_btn": "❌ ပယ်ဖျက်မည်",
        "order_cancelled": "❌ အော်ဒါကိုပယ်ဖျက်လိုက်ပါပြီ။",
        "duplicate_order":
        "⚠️ မကြာသေးခင်က အော်ဒါတင်ပြီးသားဖြစ်ပါတယ်။ ခဏစောင့်ပါ။",
        "order_success": "✅ သင်၏အော်ဒါကိုလက်ခံရရှိပါပြီ!\nOrder ID: {order_id}"
    }
}

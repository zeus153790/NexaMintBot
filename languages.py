# languages.py

TEXT = {
    "start": {
        "mm": "👋 မင်္ဂလာပါ။ NexaMint မှကြိုဆိုပါတယ်။\n\nကျေးဇူးပြု၍ သင့်နာမည်ကို ဖြည့်ပါ👇",
        "en": "👋 Hello! Welcome to NexaMint.\n\nPlease enter your name to get started 👇"
    },
    "language_choose": {
        "mm": "🌐 ဘာသာစကားရွေးပါ",
        "en": "🌐 Please choose your language"
    },
    "language_changed": {
        "mm": "✅ ဘာသာစကားကို မြန်မာလို ပြောင်းလဲပြီးပါပြီ။",
        "en": "✅ Language changed to English successfully."
    },
    "name_saved": {
        "mm": "✅ သင့်နာမည်ကို သိမ်းပြီးပါပြီ။\nအော်ဒါတင်ရန် MLBB ID (Zone) ကို ဥပမာ 12345678 (1234) ပုံစံဖြင့် ဖြည့်ပါ👇",
        "en": "✅ Your name has been saved.\nNow enter your MLBB ID in the format like: 12345678 (1234) 👇"
    },
    "invalid_mlbb": {
        "mm": "📛 MLBB ID မမှန်ပါ။ ဥပမာ: 12345678 (1234)",
        "en": "📛 Invalid MLBB ID format. Example: 12345678 (1234)"
    },
    "mlbb_saved": {
        "mm": "✅ သင်၏ MLBB ID ကို သိမ်းဆည်းပြီးပါပြီ။\n\n💎 Diamond Category ကိုရွေးပါ👇",
        "en": "✅ Your MLBB ID has been saved.\n\nNow choose a diamond category 👇"
    },
    "choose_category": {
        "mm": "💎 Diamond Category ရွေးပါ",
        "en": "💎 Choose a Diamond Category"
    },
    "choose_diamond_amount": {
        "mm": "📦 လိုချင်တဲ့ Diamond အရေအတွက်ကို ရွေးပါ",
        "en": "📦 Select the amount of Diamonds you want"
    },
    "show_price": {
        "mm": "💰 ဈေးနှုန်း: {price} Ks\n\nKBZPay သို့မဟုတ် WavePay ဖြင့် ငွေပေးချေနိုင်ပါသည်။",
        "en": "💰 Price: {price} Ks\n\nYou can pay with KBZPay or WavePay."
    },
    "upload_screenshot": {
        "mm": "📤 ကျေးဇူးပြု၍ KBZPay သို့မဟုတ် WavePay Screenshot ကို upload လုပ်ပါ\n\nKBZPay - 09978772558 Min Zayar Khant\nWavePay - 09978772558 Shwe Yi Win",
        "en": "📤 Please upload the KBZPay or WavePay payment screenshot\n\nKBZPay - 09978772558 Min Zayar Khant\nWavePay - 09978772558 Shwe Yi Win"
    },
    "confirming_order": {
        "mm": "📝 အော်ဒါကို အတည်ပြုနေသည်...",
        "en": "📝 Confirming your order..."
    },
    "order_sent": {
        "mm": "✅ သင်၏အော်ဒါကို Admin ထံပို့ပြီးပါပြီ။\n📌 /checkorder ဖြင့် အော်ဒါအခြေအနေ စစ်နိုင်ပါတယ်။",
        "en": "✅ Your order has been sent to the Admin.\n📌 You can check the order status with /checkorder"
    },
    "order_status": {
        "mm": "📦 အော်ဒါအမှတ်: {order_id}\n💎 Diamond: {diamond}\n📌 အခြေအနေ: {status}",
        "en": "📦 Order ID: {order_id}\n💎 Diamonds: {diamond}\n📌 Status: {status}"
    },
    "no_order_found": {
        "mm": "❌ သင့်အတွက် အော်ဒါများ မတွေ့ပါ။",
        "en": "❌ No orders found for you."
    },
    "order_history_title": {
        "mm": "📜 သင့်အော်ဒါမှတ်တမ်း (နောက်ဆုံး 5 ခု)",
        "en": "📜 Your Last 5 Orders"
    },
    "help": {
        "mm": "📌 NexaMint ၀န်ဆောင်မှု\n\n💳 ငွေပေးချေမှု:\nKBZPay / WavePay ➤ 09978772558\n\n🚚 ပေးပို့ချိန်:\nငွေသွင်းပြီး 5-15 မိနစ်အတွင်းပေးပို့သည်။\n\n📞 Admin ကိုဆက်သွယ်ရန်: @Terror_come",
        "en": "📌 NexaMint Services\n\n💳 Payment:\nKBZPay / WavePay ➤ 09978772558\n\n🚚 Delivery Time:\nWithin 5–15 minutes after payment.\n\n📞 Contact Admin: @Terror_come"
    },
    "already_registered": {
        "mm": "✅ သင်သည်ပြီးသား မှတ်ပုံတင်ပြီးဖြစ်သည်။",
        "en": "✅ You're already registered."
    },
    "reorder_prompt": {
        "mm": "🔁 ပြန်လည်မှာယူလိုပါသလား။ မိမိ၏အရင်မှတ်ထားသော MLBB ID: {mlbb}\n\n✅ Yes / ❌ No",
        "en": "🔁 Do you want to reorder using your saved MLBB ID: {mlbb}?\n\n✅ Yes / ❌ No"
    },
    "order_approved": {
        "mm": "✅ သင့်အော်ဒါကို Admin မှ အတည်ပြုပြီးပါပြီ။",
        "en": "✅ Your order has been approved by Admin."
    },
    "order_rejected": {
        "mm": "❌ သင့်အော်ဒါကို ငြင်းပယ်ခဲ့ပါသည်။\n📌 အကြောင်းပြချက်: {reason}",
        "en": "❌ Your order was rejected.\n📌 Reason: {reason}"
    },
    "pendingorders_admin": {
        "mm": "📋 လက်ရှိ Pending အော်ဒါများ:",
        "en": "📋 Current Pending Orders:"
    },
    "order_completed_admin": {
        "mm": "✅ Order {order_id} ကို 'Completed' အဖြစ်သတ်မှတ်ပြီးပါပြီ။",
        "en": "✅ Order {order_id} has been marked as 'Completed'."
    },
    "order_rejected_admin": {
        "mm": "❌ Order {order_id} ကို ငြင်းပယ်ပြီးပါပြီ။\n📌 အကြောင်းပြချက်: {reason}",
        "en": "❌ Order {order_id} has been rejected.\n📌 Reason: {reason}"
    },
    "new_order_admin": {
        "mm": "🆕 New Order\n👤 User: {username}\n🆔 MLBB ID: {mlbb}\n💎 Diamonds: {diamond}\n📦 Order ID: {order_id}",
        "en": "🆕 New Order\n👤 User: {username}\n🆔 MLBB ID: {mlbb}\n💎 Diamonds: {diamond}\n📦 Order ID: {order_id}"
    },
    "ask_rejection_reason": {
        "mm": "📌 Order ကို ငြင်းပယ်ရန် အကြောင်းပြချက်ရေးပါ:",
        "en": "📌 Please enter the reason for rejecting the order:"
    },
}

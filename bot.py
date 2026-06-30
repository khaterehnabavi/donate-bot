from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ===========================
# تنظیمات
# ===========================

TOKEN="8750388737:AAHacqniDfKI8OncEdEkcFQqN-zBxoeymZw"
 
YOUTUBE = "https://www.youtube.com/@KhaterehCafe"

CARD = """
❤️ حمایت مالی

💳 شماره کارت:

6219861909232216

👤 به نام:
خاطره نبوی

از حمایت شما صمیمانه سپاسگزارم ❤️
"""

USDT = """
💵 USDT (TRC20)

آدرس کیف پول:

Txxxxxxxxxxxxxxxxxxxxxxxx
"""

# آیدی عددی تلگرام خودت
ADMIN_ID = 123456789


# ===========================
# شروع
# ===========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("❤️ دونیت ریالی", callback_data="rial")],
        [InlineKeyboardButton("💵 USDT", callback_data="crypto")],
        [InlineKeyboardButton("▶️ کانال یوتیوب", url=YOUTUBE)],
    ]

    await update.message.reply_text(
        "☕ به کافه خاطره خوش آمدید\n\n"
        "اگر از ویدیوها خوشت اومده، میتونی از کانال حمایت کنی ❤️",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ===========================
# دکمه ها
# ===========================

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "rial":

        keyboard = [
            [InlineKeyboardButton("✅ پرداخت کردم", callback_data="paid")],
            [InlineKeyboardButton("❌ پرداخت نشد", callback_data="cancel")]
        ]

        await query.edit_message_text(
            CARD,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "crypto":

        await query.edit_message_text(USDT)

    elif query.data == "cancel":

        await query.edit_message_text(
            "❌ پرداخت لغو شد."
        )

    elif query.data == "paid":

        user = query.from_user

        text = f"""
💰 یک کاربر اعلام کرده پرداخت انجام داده است.

👤 نام:
{user.full_name}

🆔 آیدی:
@{user.username}

ID:
{user.id}
"""

        # ارسال پیام برای ادمین
        try:
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=text
            )
        except:
            pass

        await query.edit_message_text(
            "❤️ ممنون از حمایت شما.\n\n"
            "پیام شما برای مدیر ارسال شد.\n"
            "در صورت واریز، از شما سپاسگزاریم 🌹"
        )


# ===========================
# اجرا
# ===========================

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))

print("Bot Started...")

app.run_polling()

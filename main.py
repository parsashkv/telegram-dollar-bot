from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler


from datetime import datetime
import asyncio

from sources.tgju import get_price as get_tgju_price
from sources.alanchand import get_price as get_alanchand_price
from sources.bitpin import get_price as get_bitpin_price
from statistics import median
from sources.exiraz import get_price as get_exiraz_price

import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

CURRENCIES = {
    "usd": {
        "name": "دلار",
        "sources": [
            {"name": "TGJU", "getter": get_tgju_price},
            {"name": "AlanChand", "getter": get_alanchand_price},
            {"name": "Bitpin", "getter": get_bitpin_price},
        ]
    },

    "eur": {
        "name": "یورو",
        "sources": [
            {"name": "TGJU", "getter": get_tgju_price},
            {"name": "AlanChand", "getter": get_alanchand_price},
            {"name": "Bitpin", "getter": get_bitpin_price},
        ]
    },

    "gbp": {
        "name": "پوند",
        "sources": [
            {"name": "TGJU", "getter": get_tgju_price},
            {"name": "AlanChand", "getter": get_alanchand_price},
            {"name": "Bitpin", "getter": get_bitpin_price},
        ]
    },

    "aed": {
        "name": "درهم",
        "sources": [
            {"name": "TGJU", "getter": get_tgju_price},
            {"name": "AlanChand", "getter": get_alanchand_price},
            {"name": "Bitpin", "getter": get_bitpin_price},
        ]
    },
    "bahar": {
        "name": "سکه بهار آزادی",
        "sources": [
            {"name": "ExirAz", "getter": get_exiraz_price},
        ]
    },

    "half": {
        "name": "نیم سکه",
        "sources": [
            {"name": "ExirAz", "getter": get_exiraz_price},
        ]
    },

    "quarter": {
        "name": "ربع سکه",
        "sources": [
            {"name": "ExirAz", "getter": get_exiraz_price},
        ]
    },

    "gram_coin": {
        "name": "سکه گرمی",
        "sources": [
            {"name": "ExirAz", "getter": get_exiraz_price},
        ]
    }
}



def get_price_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("💵 دلار", callback_data="usd"),
            InlineKeyboardButton("💶 یورو", callback_data="eur"),
        ],
        [
            InlineKeyboardButton("💷 پوند", callback_data="gbp"),
            InlineKeyboardButton("🇦🇪 درهم", callback_data="aed"),
        ],
        [
            InlineKeyboardButton("🌕 بهار آزادی", callback_data="bahar"),
            InlineKeyboardButton("🌕 نیم سکه", callback_data="half"),
        ],
        [
            InlineKeyboardButton("🌕 ربع سکه", callback_data="quarter"),
            InlineKeyboardButton("🌕 سکه گرمی", callback_data="gram_coin"),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = """
💰 Telegram Price Check

قیمت ارزها و سکه‌ها را از منابع مختلف دریافت می‌کنم.

👇 قیمت مورد نظر خود را انتخاب کنید:
"""

    await update.message.reply_text(
        message,
        reply_markup=get_price_keyboard()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()

    currency = query.data

    context.args = [currency]

    await price(update, context)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = """
📌 راهنمای ربات

💵 ارزها:
/price usd    دلار
/price eur    یورو
/price gbp    پوند
/price aed    درهم

🌕 سکه‌ها:
/price bahar       سکه بهار آزادی
/price half        نیم سکه
/price quarter     ربع سکه
/price gram_coin   سکه گرمی

مثال:
 /price usd
 /price bahar
"""

    await update.message.reply_text(message)



async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "لطفاً ارز مورد نظر را وارد کنید.\nمثال: /price usd"
        )
        return

    currency = context.args[0].lower()

    if currency not in CURRENCIES:
        await update.message.reply_text("این ارز پشتیبانی نمی‌شود.")
        return

    sources = CURRENCIES[currency]["sources"]
    currency_name = CURRENCIES[currency]["name"]

    async def get_price_with_time(getter, currency):
        try:
            price = await asyncio.to_thread(getter, currency)
            received_at = datetime.now().strftime("%H:%M:%S")
            return price, received_at
        except Exception as e:
            print(f"ERROR: {e}")
            received_at = datetime.now().strftime("%H:%M:%S")
            return None, received_at
    tasks = [
        get_price_with_time(source["getter"], currency)
        for source in sources
    ]
    results = await asyncio.gather(*tasks)

    prices = [
        price for price, received_at in results
        if price is not None
    ]

    message = f"💵 قیمت {currency_name} آزاد:\n\n"

    for source, (price, received_at) in zip(sources, results):
        source_name = source["name"]
        if price is not None:
            message += f"{source_name}: {price:,} تومان\n"
            message += f"🕐 دریافت: {received_at}\n\n"
        else:
            message += f"{source_name}: ❌ دریافت نشد\n\n"

    if len(prices) >= 2:
        difference = max(prices) - min(prices)
        message += f"📊 اختلاف منابع: {difference:,} تومان"

    if prices:
        median_price = median(prices)
        message += f"\n📌 میانه قیمت‌ها: {median_price:,.0f} تومان"



    if update.message:
        await update.message.reply_text(message)
    else:
        await update.callback_query.message.reply_text(message)




def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("price", price))
    app.add_handler(CallbackQueryHandler(button_handler))

    mode = os.getenv("BOT_MODE", "polling")

    print(f"Bot is running in {mode} mode...")

    if mode == "webhook":
        port = int(os.getenv("PORT", "8080"))
        render_url = os.getenv("RENDER_URL")

        app.run_webhook(
            listen="0.0.0.0",
            port=port,
            url_path=BOT_TOKEN,
            webhook_url=f"{render_url}/{BOT_TOKEN}",
        )

    else:
        app.run_polling()


if __name__ == "__main__":
    main()
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


from datetime import datetime
import asyncio

from config import BOT_TOKEN
from sources.tgju import get_price as get_tgju_price
from sources.alanchand import get_price as get_alanchand_price
from sources.bitpin import get_price as get_bitpin_price
from statistics import median

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
    }
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = """
💵 Telegram Dollar Check

قیمت دلار آزاد را از چند منبع دریافت می‌کنم.

برای دریافت قیمت:
 /price

برای راهنما:
 /help
"""

    await update.message.reply_text(message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = """
📌 راهنمای ربات

/price
دریافت قیمت دلار از چند منبع

/help
نمایش این راهنما
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
        except Exception:
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



    await update.message.reply_text(message)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("price", price))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


from datetime import datetime
import asyncio

from config import BOT_TOKEN
from sources.tgju import get_dollar_price as get_tgju_price
from sources.alanchand import get_dollar_price as get_alanchand_price
from sources.bitpin import get_dollar_price as get_bitpin_price

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
    async def get_price_with_time(getter):
        price = await asyncio.to_thread(getter)
        received_at = datetime.now().strftime("%H:%M:%S")
        return price, received_at

    (
        (tgju_price, tgju_time),
        (alanchand_price, alanchand_time),
        (bitpin_price, bitpin_time)
    ) = await asyncio.gather(
        get_price_with_time(get_tgju_price),
        get_price_with_time(get_alanchand_price),
        get_price_with_time(get_bitpin_price)
    )

    prices = [
        price for price in [tgju_price, alanchand_price, bitpin_price]
        if price is not None
    ]

    message = "💵 قیمت دلار آزاد:\n\n"

    if tgju_price:
        message += f"TGJU: {tgju_price:,} تومان\n"
        message += f"🕐 دریافت: {tgju_time}\n\n"
    else:
        message += "TGJU: ❌ دریافت نشد\n\n"

    if alanchand_price:
        message += f"AlanChand: {alanchand_price:,} تومان\n"
        message += f"🕐 دریافت: {alanchand_time}\n\n"
    else:
        message += "AlanChand: ❌ دریافت نشد\n\n"

    if bitpin_price:
        message += f"Bitpin: {bitpin_price:,} تومان\n"
        message += f"🕐 دریافت: {bitpin_time}\n"
    else:
        message += "Bitpin: ❌ دریافت نشد\n"

    if len(prices) >= 2:
        difference = max(prices) - min(prices)
        message += f"\n📊 اختلاف منابع: {difference:,} تومان"

    if len(prices) == 3:
        sorted_prices = sorted(prices)
        median = sorted_prices[1]
        message += f"\n📌 میانه قیمت‌ها: {median:,} تومان"

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
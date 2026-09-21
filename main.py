import requests
from bs4 import BeautifulSoup
import re

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "8676375002:AAGgvh2MwvDUQDZkpW8IYo29onsFILGs1ik"


def get_dollar_price():
    url = "https://www.tgju.org/profile/price_dollar_rl"

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    text = soup.get_text(" ", strip=True)

    index = text.find("نرخ فعلی")

    if index == -1:
        return None

    result = text[index:index + 100]

    match = re.search(r"نرخ فعلی::\s*([\d,]+)", result)

    if match:
        price_rial = int(match.group(1).replace(",", ""))
        price_toman = price_rial // 10
        return price_toman

    return None


async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dollar_price = get_dollar_price()

    if dollar_price:
        await update.message.reply_text(
            f"💵 قیمت دلار آزاد:\n{dollar_price:,} تومان"
        )
    else:
        await update.message.reply_text(
            "❌ نتونستم قیمت دلار رو دریافت کنم."
        )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("price", price))

    print("Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
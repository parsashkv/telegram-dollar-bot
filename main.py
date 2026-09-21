from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from config import BOT_TOKEN
from sources.tgju import get_dollar_price


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
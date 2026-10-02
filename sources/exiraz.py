import requests
from bs4 import BeautifulSoup

URL = "https://exiraz.com/coin-price"


def get_price(coin):
    response = requests.get(URL, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    coin_names = {
        "bahar": "سکه بهار آزادی",
        "half": "نیم سکه",
        "quarter": "ربع سکه",
        "gram_coin": "سکه گرمی",
    }

    name = coin_names[coin]

    element = soup.find(
        "h3",
        string=lambda text: text and text.strip() == name
    )

    if element is None:
        return None

    price = element.find_next_sibling("div").get_text(strip=True)

    price = price.translate(str.maketrans(
        "۰۱۲۳۴۵۶۷۸۹٬",
        "0123456789,"
    ))

    return int(price.replace(",", ""))
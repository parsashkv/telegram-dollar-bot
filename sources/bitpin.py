import requests
from bs4 import BeautifulSoup
import re

CURRENCY_URLS = {
    "usd": "https://bitpin.ir/academy/live/currency/",
    "eur": "https://bitpin.ir/academy/live/currency/eur/",
    "gbp": "https://bitpin.ir/academy/live/currency/gbp/",
    "aed": "https://bitpin.ir/academy/live/currency/aed/",
}

CURRENCY_NAMES = {
    "usd": "دلار (نرخ بازار)",
    "eur": "یورو (نرخ بازار)",
    "gbp": "پوند (نرخ بازار)",
    "aed": "درهم امارات (نرخ بازار)",
}


def get_price(currency):
    url = CURRENCY_URLS.get(currency)

    if not url:
        return None

    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(" ", strip=True)

        currency_name = CURRENCY_NAMES.get(currency)

        if not currency_name:
            return None

        index = text.find(currency_name)

        if index == -1:
            return None

        result = text[index:index + 150]

        match = re.search(
            rf"{re.escape(currency_name)}.*?([\d,،]+)\s*تومان",
            result
        )

        if match:
            price = match.group(1).replace(",", "").replace("،", "")
            return int(price)

        return None

    except requests.RequestException:
        return None
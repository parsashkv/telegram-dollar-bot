import requests
from bs4 import BeautifulSoup
import re


CURRENCY_NAMES = {
    "usd": "دلار آمریکا",
    "eur": "یورو",
    "gbp": "پوند انگلیس",
    "aed": "درهم",
}


def get_price(currency):
    url = f"https://alanchand.com/currencies-price/{currency}"


    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(" ", strip=True)

        currency_name = CURRENCY_NAMES.get(currency)

        if not currency_name:
            return None

        index = text.find(f"قیمت فروش {currency_name}")


        if index == -1:
            return None

        result = text[index:index + 100]

        match = re.search(
            rf"قیمت فروش {currency_name}\s*([\d,،]+)",
            result
        )

        if match:
            price = match.group(1).replace(",", "").replace("،", "")
            return int(price)

        return None

    except requests.RequestException:
        return None



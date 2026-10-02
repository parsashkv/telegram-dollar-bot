import requests
from bs4 import BeautifulSoup
import re

CURRENCY_URLS = {
    "usd": "https://www.tgju.org/profile/price_dollar_rl",
    "eur": "https://www.tgju.org/profile/price_eur",
    "gbp": "https://www.tgju.org/profile/price_gbp",
    "aed": "https://www.tgju.org/profile/price_aed",
}


GOLD_URLS = {
    "emami": "https://www.tgju.org/profile/sekee",
    "bahar": "https://www.tgju.org/profile/sekeb",
    "half": "https://www.tgju.org/profile/nim",
    "quarter": "https://www.tgju.org/profile/rob",
    "gram_coin": "https://www.tgju.org/profile/gerami",
    "gold_18": "https://www.tgju.org/profile/geram18",
}


def get_gold_price(product):
    url = GOLD_URLS.get(product)

    if not url:
        return None

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(" ", strip=True)

        index = text.find("نرخ فعلی")

        if index == -1:
            return None

        result = text[index:index + 100]

        match = re.search(r"نرخ فعلی::\s*([\d,]+)", result)

        if match:
            price_rial = int(match.group(1).replace(",", ""))
            return price_rial // 10

        return None

    except requests.RequestException:
        return None


def get_price(currency):
    url = CURRENCY_URLS.get(currency)
    if not url:
        return None


    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(" ", strip=True)

        index = text.find("نرخ فعلی")

        if index == -1:
            return None

        result = text[index:index + 100]

        match = re.search(r"نرخ فعلی::\s*([\d,]+)", result)

        if match:
            price_rial = int(match.group(1).replace(",", ""))
            return price_rial // 10

        return None

    except requests.RequestException:
        return None


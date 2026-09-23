import requests
from bs4 import BeautifulSoup
import re


def get_dollar_price():
    url = "https://alanchand.com/currencies-price/usd"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(" ", strip=True)

        index = text.find("قیمت فروش دلار آمریکا")

        if index == -1:
            return None

        result = text[index:index + 100]

        match = re.search(r"قیمت فروش دلار آمریکا\s*([\d,،]+)", result)

        if match:
            price = match.group(1).replace(",", "").replace("،", "")
            return int(price)

        return None

    except requests.RequestException:
        return None
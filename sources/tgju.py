import requests
from bs4 import BeautifulSoup
import re


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
import requests
from bs4 import BeautifulSoup
import re


def get_dollar_price():
    url = "https://bitpin.ir/academy/live/currency/"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(" ", strip=True)

        index = text.find("دلار (نرخ بازار)")

        if index == -1:
            return None

        result = text[index:index + 150]

        match = re.search(
            r"دلار \(نرخ بازار\).*?([\d,،]+)\s*تومان",
            result
        )

        if match:
            price = match.group(1).replace(",", "").replace("،", "")
            return int(price)

        return None

    except requests.RequestException:
        return None
import requests
from bs4 import BeautifulSoup
import re

url = "https://www.tgju.org/profile/price_dollar_rl"

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

text = soup.get_text(" ", strip=True)

index = text.find("نرخ فعلی")

if index != -1:
    result = text[index:index + 100]

    match = re.search(r"نرخ فعلی::\s*([\d,]+)", result)

    if match:
        price = match.group(1)
        print("Dollar price:", price)
    else:
        print("Price not found")
else:
    print("نرخ فعلی پیدا نشد")
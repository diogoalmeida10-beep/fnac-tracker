import os
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time

BOT_TOKEN = os.getenv(
8257351230:AAH-ZFugrpnmIJPGlmFQ174tRVHIFqKQbNK)
CHAT_ID = os.getenv(622090807
)

if not BOT_TOKEN or not CHAT_ID:
    raise ValueError("BOT_TOKEN and CHAT_ID must be set in environment variables!")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)




import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time

# --------------------------
# TELEGRAM SETTINGS
# --------------------------
BOT_TOKEN = 8257351230:AAH-ZFugrpnmIJPGlmFQ174tRVHIFqKQbNK
CHAT_ID = 622090807

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

# --------------------------
# SCRAPER SETTINGS
# --------------------------

CATEGORIES = {
    "VINYL": "https://www.fnac.pt/Musica-Vinil-Vinil/s18264?PageIndex={}",
    "CD": "https://www.fnac.pt/Musica-CD-CDs/s495?PageIndex={}"
}

headers = {
    "User-Agent": UserAgent().chrome,
    "Accept-Language": "pt-PT,pt;q=0.9,en;q=0.8"
}

def price_to_float(text):
    return float(text.replace("€", "").replace(".", "").replace(",", ".").strip())

def check_category(name, url_template):
    page = 1
    deals_found = 0

    while True:
        url = url_template.format(page)
        print(f"Checking {name} page {page}...")

        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")

        items = soup.select(".Article-item")
        if not items:
            break

        for p in items:
            title_el = p.select_one(".Article-title")
            price_el = p.select_one(".f-priceBox-price")
            old_price_el = p.select_one(".f-priceBox-price--old")

            if not title_el or not price_el:
                continue

            title = title_el.text.strip()
            link = "https://www.fnac.pt" + title_el["href"]

            current_price = price_to_float(price_el.text)

            if old_price_el:
                old_price = price_to_float(old_price_el.text)
            else:
                old_price = current_price

            if old_price == 0:
                continue

            discount = (old_price - current_price) / old_price * 100

            if discount >= 80:
                deals_found += 1
                message = (
                    f"🔥 *80%+ DISCOUNT FOUND!*\n\n"
                    f"📀 {title}\n"
                    f"💶 Now: {current_price}€\n"
                    f"💸 Was: {old_price}€\n"
                    f"📉 Discount: {discount:.1f}%\n\n"
                    f"🔗 {link}"
                )
                send_telegram(message)

        page += 1
        time.sleep(1)  # be polite

    print(f"{name}: found {deals_found} deals")

# --------------------------
# MAIN LOOP
# --------------------------

for name, url_template in CATEGORIES.items():
    check_category(name, url_template)

print("Done.")

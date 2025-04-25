from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

def scrape_flight_deals():
    deals = []
    airlines = [
        {"name": "Example Airlines", "url": "https://example.com/special-offers"},
    ]
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    for airline in airlines:
        try:
            response = requests.get(airline["url"], headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            deal_elements = soup.find_all("div", class_="deal")
            for deal in deal_elements:
                title = deal.find("h3").text.strip() if deal.find("h3") else "No Title"
                price = deal.find("span", class_="price").text.strip() if deal.find("span", class_="price") else "N/A"
                link = deal.find("a")["href"] if deal.find("a") else airline["url"]
                deals.append({
                    "airline": airline["name"],
                    "title": title,
                    "price": price,
                    "link": link,
                    "date": datetime.now().strftime("%Y-%m-%d")
                })
        except Exception as e:
            print(f"Error scraping {airline['name']}: {e}")
    deals.append({
        "airline": "Example Airlines",
        "title": "Taipei to Tokyo Round Trip",
        "price": "$250",
        "link": "https://example.com/deal1",
        "date": datetime.now().strftime("%Y-%m-%d")
    })
    return deals

@app.route("/")
def index():
    deals = scrape_flight_deals()
    return render_template("index.html", deals=deals)

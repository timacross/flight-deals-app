from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

def scrape_flight_deals():
    deals = []
    
    airlines = [
        {"name": "VietJet Air", "url": "https://www.vietjetair.com/"},
        {"name": "Cebu Pacific", "url": "https://www.cebupacificair.com/"},
        {"name": "AirAsia", "url": "https://www.airasia.com/zh/tw"},
        {"name": "Thai Lion Air", "url": "https://www.lionairthai.com/tw/tw/"},
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    for airline in airlines:
        try:
            response = requests.get(airline["url"], headers=headers, timeout=10)
            response.raise_for_status()  # 若發生錯誤會引發例外
            soup = BeautifulSoup(response.text, "html.parser")

            # *** 真實爬蟲需根據每家航空公司網站結構來改 ***
            # 這裡使用假資料模擬特價資訊
            deals.append({
                "airline": airline["name"],
                "title": "從台北出發的限時優惠票",
                "price": "$99 起",
                "link": airline["url"],
                "date": datetime.now().strftime("%Y-%m-%d")
            })
        except Exception as e:
            print(f"Error scraping {airline['name']}: {e}")
    
    return deals

@app.route("/")
def index():
    deals = scrape_flight_deals()
    return render_template("index.html", deals=deals)

if __name__ == "__main__":
    app.run(debug=True)

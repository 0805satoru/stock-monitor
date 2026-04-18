import requests
from bs4 import BeautifulSoup
import os

# GitHubのSecretsからURLを読み込む
DISCORD_URL = os.environ.get("DISCORD_WEBHOOK_URL")
# ストップ高銘柄の一覧ページ
URL = "https://kabutan.jp/warning/?mode=3_1"

def check_market():
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
    try:
        response = requests.get(URL, headers=headers)
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 銘柄名を取得
        stocks = soup.find_all("td", class_="stock_name")
        
        if not stocks:
            print("現在、ストップ高銘柄はありません。")
            return

        # 銘柄が見つかったらDiscordへ通知
        for s in stocks:
            name = s.text.strip()
            data = {"content": f"🚀 **ストップ高検知**\n銘柄名: {name}"}
            requests.post(DISCORD_URL, json=data)
            print(f"通知完了: {name}")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_market()

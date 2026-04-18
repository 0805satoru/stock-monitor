import requests
from bs4 import BeautifulSoup
import os

# GitHubの「秘密の鍵」からDiscordのURLを読み込む設定
DISCORD_URL = os.environ.get("DISCORD_WEBHOOK_URL")
# ストップ高銘柄の一覧ページ
URL = "https://kabutan.jp/warning/?mode=3_1"

def send_notifications(name):
    """Discordに通知を送る"""
    data = {"content": f"🚀 **ストップ高検知**\n銘柄名: {name}"}
    try:
        requests.post(DISCORD_URL, json=data)
    except Exception as e:
        print(f"送信エラー: {e}")

def check_market():
    """株探をチェックする"""
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(URL, headers=headers)
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 銘柄名が書かれている場所（tdタグのstock_nameクラス）を探す
        stocks = soup.find_all("td", class_="stock_name")
        
        if not stocks:
            print("現在、ストップ高銘柄はありません。")
            return

        for s in stocks:
            name = s.text.strip()
            print(f"検知: {name}")
            send_notifications(name)
                
    except Exception as e:
        print(f"エラー発生: {e}")

if __name__ == "__main__":
    check_market()

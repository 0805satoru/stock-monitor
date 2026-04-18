import requests
from bs4 import BeautifulSoup
import os

# GitHubのSecretsから読み込む設定
DISCORD_URL = os.environ.get("DISCORD_WEBHOOK_URL")
# ストップ高銘柄の一覧ページ（東証・大証・地方市場すべて）
URL = "https://kabutan.jp/warning/?mode=3_1"

def check_market():
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
    try:
        response = requests.get(URL, headers=headers)
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 銘柄名が書かれている場所（tdタグのstock_nameクラス）を取得
        stocks = soup.find_all("td", class_="stock_name")
        
        # 【テスト用】起動を確認するための通知（不要になったら消してください）
        requests.post(DISCORD_URL, json={"content": "✅ システム稼イド中：株探をチェックしました。"})

        if not stocks:
            print("現在、ストップ高銘柄はありません。")
            return

        # ページに載っている全銘柄をDiscordへ通知
        for s in stocks:
            name = s.text.strip()
            data = {"content": f"🚀 **ストップ高検知**\n銘柄名: {name}"}
            requests.post(DISCORD_URL, json=data)
            print(f"通知完了: {name}")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_market()

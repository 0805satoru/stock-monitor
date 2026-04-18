import requests
from bs4 import BeautifulSoup
import os

# GitHubの「秘密の鍵」からDiscordのURLを読み込む設定
DISCORD_URL = os.environ.get("DISCORD_WEBHOOK_URL")
# ストップ高銘柄の一覧ページ
URL = "https://kabutan.jp/warning/?mode=3_1"

def check_market():
    # サイトに「人間がアクセスしています」と伝えるための設定
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(URL, headers=headers)
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 銘柄名が書かれている場所を特定
        stocks = soup.find_all("td", class_="stock_name")
        
        if not stocks:
            print("現在、ストップ高銘柄はありません。")
            return

        # ページに載っている銘柄を一つずつ取り出して通知
        for s in stocks:
            name = s.text.strip()
            data = {"content": f"🚀 **ストップ高検知**\n銘柄名: {name}"}
            requests.post(DISCORD_URL, json=data)
            print(f"通知完了: {name}")
                
    except Exception as e:
        print(f"エラーが発生しました: {e}")

＃if __name__ == "__main__":
    ＃check_market()

if __name__ == "__main__":
    # テスト用：強制的にメッセージを送る
    data = {"content": "✅ GitHubからのテスト通知です！正常に連携されています。"}
    requests.post(DISCORD_URL, json=data)
    # 本来のチェックも動かす
    check_market()

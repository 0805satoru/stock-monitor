import requests
from bs4 import BeautifulSoup
import os
import time

DISCORD_URL = os.environ.get("DISCORD_WEBHOOK_URL")
# ターゲットを「みんかぶ」のストップ高一覧に変更
URL = "https://minkabu.jp/news/search?category=s_high"

def check_market():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(URL, headers=headers, timeout=15)
        response.encoding = "utf-8"
        
        soup = BeautifulSoup(response.text, "html.parser")
        print(f"--- 取得したページのタイトル: {soup.title.string if soup.title else '不明'} ---")

        # みんかぶのニュース見出し（h2 または div 内のリンク）を探す
        # 構造：div.news_list_item > a > h2
        articles = soup.select(".news_list_item")
        
        found_any = False
        for item in articles[:10]:  # 最新10件を確認
            title_tag = item.select_one(".news_list_item_title")
            if title_tag and "ストップ高" in title_tag.text:
                title_text = title_tag.text.strip()
                
                # Discordに送信
                requests.post(DISCORD_URL, json={"content": f"🚀 **ストップ高検知 (みんかぶ)**\n{title_text}"})
                print(f"通知成功: {title_text}")
                found_any = True
                time.sleep(0.5)

        if not found_any:
            print("ストップ高のニュースは見つかりませんでした。")
                
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    check_market()

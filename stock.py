import requests
from bs4 import BeautifulSoup
import os
import time

DISCORD_URL = os.environ.get("DISCORD_WEBHOOK_URL")
URL = "https://kabutan.jp/news/?category=5"

def check_market():
    # ヘッダーをより本物のブラウザ（Chrome）に近づける
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
        "Referer": "https://kabutan.jp/"
    }
    
    try:
        # 連続アクセスで弾かれないよう、少し待つ（おまじない）
        time.sleep(1)
        response = requests.get(URL, headers=headers, timeout=10)
        response.encoding = "utf-8"
        
        # ログ確認用（タイトルが 'ニュース - 株探' になっていれば成功）
        soup = BeautifulSoup(response.text, "html.parser")
        print(f"--- 取得したページのタイトル: {soup.title.string if soup.title else '不明'} ---")

        # ニュースの各行（tr）を取得
        articles = soup.select(".news_list_table tbody tr")
        
        found_any = False
        # 10分おきに動くので、最新の10件程度だけチェックすれば十分
        for row in articles[:10]:
            title_tag = row.select_one(".news_list_title a")
            if title_tag and "ストップ高" in title_tag.text:
                title_text = title_tag.text.strip()
                
                # Discordに送信
                requests.post(DISCORD_URL, json={"content": f"🚀 **ストップ高検知**\n{title_text}"})
                print(f"通知成功: {title_text}")
                found_any = True
                # Discordの連投制限（レートリミット）を避けるため少し待つ
                time.sleep(0.5)

        if not found_any:
            print("ストップ高に関する新しいニュースは見つかりませんでした。")
                
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    check_market()

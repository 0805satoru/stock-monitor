import requests
from bs4 import BeautifulSoup
import os

# GitHubのSecretsからURLを読み込む
DISCORD_URL = os.environ.get("DISCORD_WEBHOOK_URL")
# より確実に情報が取れる「ニュース形式」のストップ高一覧ページに変更
URL = "https://kabutan.jp/news/?category=5"

def check_market():
    # 相手のサーバーに拒否されないための「名刺」代わりの設定
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
    
    try:
        response = requests.get(URL, headers=headers)
        response.encoding = response.apparent_encoding
        
        # --- 【デバッグ】ここから：HTMLの冒頭をログに出す ---
        print("--- 取得データ確認用 (最初の300文字) ---")
        print(response.text[:300])
        print("---------------------------------------")
        # --- ここまで ---

        soup = BeautifulSoup(response.text, "html.parser")
        
        # ニュース一覧のテーブルから銘柄を含むリンクを探す
        # 株探のニュースページ構造に合わせた抽出
        articles = soup.select(".news_list_table tr")
        
        found_any = False
        for row in articles:
            title_tag = row.select_one(".news_list_title a")
            if title_tag and "ストップ高" in title_tag.text:
                name = title_tag.text.strip()
                # 時間も取得（あれば）
                time_tag = row.select_one(".news_list_time time")
                time_str = time_tag.text if time_tag else "本日"
                
                # Discord送信
                data = {"content": f"🚀 **ストップ高検知**\n【{time_str}】\n{name}"}
                requests.post(DISCORD_URL, json=data)
                
                print(f"通知完了: {name}")
                found_any = True

        if not found_any:
            print("解析しましたが、ストップ高銘柄の記事は見つかりませんでした。")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_market()

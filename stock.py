import requests
import os

# 秘密の鍵がちゃんと動いているか確認
url = os.environ.get("DISCORD_WEBHOOK_URL")

def test_send():
    if url is None:
        print("❌ エラー: DiscordのURLが設定されていません（Secretsを確認してください）")
        return
    
    data = {"content": "📢 GitHub Actionsからのテスト通知です！これが届けば成功です。"}
    response = requests.post(url, json=data)
    
    if response.status_code == 204:
        print("✅ Discordへの送信に成功しました！")
    else:
        print(f"❌ 送信失敗。エラーコード: {response.status_code}")

if __name__ == "__main__":
    test_send()

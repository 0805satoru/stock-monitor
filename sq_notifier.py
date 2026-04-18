import datetime
import requests
import os
import jpholiday

DISCORD_URL = os.environ.get("SQ_WEBHOOK_URL")

def get_sq_date(year, month):
    """祝日を考慮したその月のSQ日（第2金曜日）を計算"""
    first_day = datetime.date(year, month, 1)
    days_to_first_friday = (4 - first_day.weekday() + 7) % 7
    sq_date = first_day + datetime.timedelta(days=days_to_first_friday + 7)
    
    # 祝日または土日なら前営業日にずらす
    while jpholiday.is_holiday(sq_date) or sq_date.weekday() >= 5:
        sq_date -= datetime.timedelta(days=1)
    return sq_date

def check_sq():
    today = datetime.date.today()
    for m_offset in [0, 1]:
        target_month = today.month + m_offset
        target_year = today.year
        if target_month > 12:
            target_month -= 12
            target_year += 1
        
        sq_target = get_sq_date(target_year, target_month)
        diff = (sq_target - today).days
        
        if diff == 14:
            send_discord(f"🗓 **SQリマインダー (2週間前)**\n{target_month}月のSQ日は **{sq_target}** です。")
        elif diff == 7:
            send_discord(f"⚠️ **SQリマインダー (1週間前)**\n{target_month}月のSQ日は **{sq_target}** です。")

def send_discord(message):
    if DISCORD_URL:
        requests.post(DISCORD_URL, json={"content": message})

if __name__ == "__main__":
    check_sq()

if __name__ == "__main__":
    # ★テスト用にこの1行を追加して保存（Commit）する
    send_discord("🧪 SQ通知チャンネルのテスト送信です！")
    
    check_sq()

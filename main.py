import requests
import time
import hmac
import hashlib
import base64
import json
import os
import telegram

# تنظیمات بات تلگرام
TELEGRAM_TOKEN = "7269363995:AAEC5qbA6i57ytdctFxKTkhXzdTf6uuPAm0"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"  # اینو بعداً ست می‌کنیم

# اطلاعات API صرافی LBank
API_KEY = "9ddf15b3-583e-45d4-84ea-9064012d06ab"
API_SECRET = "78334F69DCFD1A61562E2491E968EEA9"

# توکن‌ها یا جفت ارزهایی که می‌خوای بررسی کنی
SYMBOLS = ["BTC_USDT", "ETH_USDT", "PEPE_USDT", "DOGE_USDT", "BONK_USDT"]

def send_telegram_alert(message):
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

def get_signature(params):
    sign_str = ""
    for key in sorted(params.keys()):
        sign_str += key + str(params[key])
    sign_str += API_SECRET
    return hashlib.sha256(sign_str.encode()).hexdigest()

def check_whale_activity():
    url = "https://api.lbkex.com/v2/futures/openOrders.do"
    for symbol in SYMBOLS:
        params = {
            "api_key": API_KEY,
            "symbol": symbol,
            "timestamp": int(time.time() * 1000)
        }
        sign = get_signature(params)
        params["sign"] = sign
        try:
            response = requests.post(url, data=params)
            data = response.json()
            if "data" in data and data["data"]:
                big_orders = [order for order in data["data"] if float(order["amount"]) > 100000]
                for order in big_orders:
                    msg = f"🚨 نهنگ شناسایی شد!\nجفت ارز: {symbol}\nمقدار: {order['amount']}\nقیمت: {order['price']}\nنوع: {order['type']}"
                    send_telegram_alert(msg)
        except Exception as e:
            print(f"خطا در بررسی {symbol}: {e}")

if __name__ == "__main__":
    while True:
        check_whale_activity()
        time.sleep(60)

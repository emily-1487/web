import json
import requests
import os
import sys

# json_str = json.dumps(data)
# json_data = json.loads(json_str)
##########################定義常數###############################
API_KEY = "bbd176313163ca6836b79a06217f3b6f"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
UNITS = "metric"
LANG = "zh_tw"
ICON_BASE_URL = "https://openweathermap.org/img/wn/"
##########################主程式#################################
os.chdir(sys.path[0])
city_name = input("請輸入城市名稱：")
send_url = f"{BASE_URL}appid={API_KEY}&q={city_name}&units={UNITS}&lang={LANG}"
print(f"發送的URL：{send_url}")
response = requests.get(send_url)
info = response.json()
if "weather" in info and "main" in info:
    current_temperture = info["main"]["temp"]
    weather_description = info["weather"][0]["description"]
    icon_code = info["weather"][0]["icon"]
    print(f"城市：{city_name}")
    print(f"溫度：{current_temperture}℃")
    print(f"描述：{weather_description}")
    icon_url = f"{ICON_BASE_URL}{icon_code}@2x.png"
    print(f"下載天氣圖標:{icon_url}")
    icon_response = requests.get(icon_url)
    if icon_response.status_code == 200:
        with open(f"{icon_code}.png", "wb") as icon_file:
            icon_file.write(icon_response.content)
        print(f"天氣圖標已下載到{icon_code}.png")
    else:
        print("無法下載天氣")
else:
    print("找不到該程式或無法獲取天氣資訊")

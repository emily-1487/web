import requests

###########################定義常數###########################
API_KEY = "892da2f13edf3c7f382637760e72d224"  # API Key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"  # API URL
UNITS = "metric"  # 單位 (公制)
LANG = "zh_tw"  # 語言 (繁體中文)
##########################主程式###############################
city_name = "london"
send_url = f"{BASE_URL}q={city_name}&appid={API_KEY}&units={UNITS}&lang={LANG}"
print(f"發送的URL：{send_url}")
response = requests.get(send_url)
response.raise_for_status()
info = response.json()
if "city" in info:
    for forecast in info["list"]:
        dt_txt = forecast["dt_txt"]
        temp = forecast["main"]["temp"]
        weather_description = forecast["weather"][0]["description"]
        print(f"{dt_txt}-溫度:{temp}度,天氣狀況:{weather_description}")
else:
    print("找不到該程式或無法獲取天氣資訊")

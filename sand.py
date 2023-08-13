from rbdata import RbData

# import requests
# api_url="https://functions.yandexcloud.net/d4el6366460kn19a2ao8"
# resp=requests.get(api_url,json={'videoName':"ЦСКА"})
# print(resp.text)

v=RbData("https://functions.yandexcloud.net/d4el6366460kn19a2ao8").get_videos("ЮФЛ2")
print(list(v))
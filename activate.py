import sys
import requests

import telebot

if len(sys.argv)<3:
    print('usage python -m activate [-help] TOKEN URL')
else:
    token=sys.argv[1]
    url=sys.argv[2]

resp=requests.get(f'https://api.telegram.org/bot{token}/setWebhook?url={url}')
if resp.status_code==200:
    print("Success!!!")
print(resp.json()['description'])

#bot.set_webhook(url)
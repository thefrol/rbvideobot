from bot import bot
from telebot.types import Update
import traceback

def handler(event,context):
    #pprint(event)
    request_body_dict = event['body']
    update = Update.de_json(request_body_dict)
    try:
        bot.process_new_updates([update])
    except Exception as e:
        print('error {e}')
        print('Ой, со мной что-то не так 🤮')
        print(traceback.format_exc())
    
    

    return {
        'body':'',
        'status_code':200
        }
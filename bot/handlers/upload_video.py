from rbdata.native_api import NativeRbData
import rbdata
import yadisk
from pprint import pprint
import os
from ..bot import bot
from telebot.types import Message



def upload_video(resource:yadisk.Resource, messaging_func) -> rbdata.Video:
    """
        url: URL of video to upload
        messaging_func: a function to response to bot"""
    n=NativeRbData(os.getenv("RBDATA_EMAIL"),os.getenv("RBDATA_PASSWORD"))


    if not resource.is_file:
        print(f'not a file, its a {resource.type}')
        if messaging_func:
            messaging_func("🥴 По ссылке не файл")
        return None
    if resource.media_type != 'video':
        print(f'not a video!!! its a {resource.media_type}')
        if messaging_func:
            messaging_func("🥴 По ссылке не видео")
        return None

    return n.upload_video_from_url(video_url=resource.file, filename=resource.name)

def is_yandex_disk_link(message):
    return 'yadi.sk' in message.text or 'disk.yandex.ru' in message.text

@bot.message_handler(func=is_yandex_disk_link)
def on_disk_link(message:Message):
    bot.reply_to(message, "🤔Кажется, что-то с Яндекс.Диска. Попробую загрузить в видео. ")
    def responder(text:str):
        nonlocal message
        """a function that allows to respond to this message in this handler"""
        bot.reply_to(message=message,text=text)
    url=message.text
    r=yadisk.Resource(url)
    video=upload_video(resource=r,messaging_func=responder)
    if video is None:
        bot.reply_to(message=message,text='Не удалось загрузить файл 😓')
        return
    bot.send_photo(chat_id=message.chat.id,photo=r.preview,caption=f'❤️‍🔥Загружено видео:\n{video.name}\n`{video.url}` ',parse_mode='MARKDOWN')
    
        

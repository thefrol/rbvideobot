from rbdata.native_api import NativeRbData
import rbdata
import yadisk
from pprint import pprint
import os
from ..bot import bot
from telebot.types import Message
import re

#Helper Functions

def upload_video_from_yadisk(resource:yadisk.Resource, messaging_func=None) -> rbdata.Video:
    """Загружает в Хранилище ресурс яндекс диска
        resource: yadisk.Resource ресурс яндекс диска
        messaging_func: функция, которая будет отправлять сообщения которые напишет эта функция
        
    В случае ошибки вернет None, в случае успеха rbdata.Video"""
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

def upload_random_video(url, messaging_func=None):
    """Загружает видео по ссылке в Хранилище
        url: ссылка на видео
        messaging_func: функция принимающая сообщения от этой функции и, например, отправляющая их в бот
    возвращает rbdata.Video если все удалось, или None если возникла ошибка"""
    n=NativeRbData(os.getenv("RBDATA_EMAIL"),os.getenv("RBDATA_PASSWORD"))
    return n.upload_video_from_url(video_url=url, filename=f"Upload from @rbvideobot: {url}") #TODO bot name in os.getenv and after settings.bot_name


# Conditions for handlers

def is_yandex_disk_link(message):
    """returns True if message has yandex link in its text
    This is a condition function for handlers"""
    return 'yadi.sk' in message.text or 'disk.yandex.ru' in message.text

def is_link(message):
    """returns True if message has any url in its text
    This is a condition function for handlers"""
    m=re.match(pattern=r"(http|https|ftp)://.*",string=message.text)
    return m is not None

def not_(func):
    """inverts a condition func
    usage: not(is_yandex_link)"""
    return lambda message: not func(message)

def and_(*funcs): #TODO TESTS!
    """mixes two and more conditions functions into one
    usage: and_(is_link,not_(is_yandex_link))"""
    def callee(message: Message):
        nonlocal funcs
        return all((f(message) for f in funcs))
    return callee


# Handlers

@bot.message_handler(func=is_yandex_disk_link)
def on_disk_link(message:Message):
    bot.reply_to(message, "🤔Кажется, что-то с Яндекс.Диска. Попробую загрузить в видео. ")
    def responder(text:str):
        nonlocal message
        """a function that allows to respond to this message in this handler"""
        bot.reply_to(message=message,text=text)
    url=message.text
    r=yadisk.Resource(url)
    video=upload_video_from_yadisk(resource=r,messaging_func=responder)
    if video is None:
        bot.reply_to(message=message,text='Не удалось загрузить файл 😓')
        return
    bot.send_photo(chat_id=message.chat.id,photo=r.best_preview,caption=f'❤️‍🔥Загружено видео:\n{video.name}\n`{video.url}` ',parse_mode='MARKDOWN')
    
@bot.message_handler(func=and_(is_link, not_(is_yandex_disk_link)))
def on_link(message:Message):
    """Ловит сообщения со ссылками, и пытается загрузить их в Хранилище"""
    bot.reply_to(message, "🤔 Какая-то ссылка. Попробую её загрузить в видео. ")
    url=message.text
    video=upload_random_video(url=url)
    if video is None:
        bot.reply_to(message=message,text='Не удалось загрузить файл 😓')
        return
    bot.send_message(chat_id=message.chat.id,text=f'❤️‍🔥Загружено видео:\n{video.name}\n`{video.url}` ',parse_mode='MARKDOWN')   
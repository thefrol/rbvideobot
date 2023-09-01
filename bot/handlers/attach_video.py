from rbdata.native_api import NativeRbData
import rbdata
import os
from telebot.types import Message
import re

from ..bot import bot
import settings
from .conditionals import is_a_reply, is_numeric, reply_to_message, from_bot,has_link_to_storage, and_

# Handlers

def extract_video_id(text, messaging_callback):

        m=list(re.finditer(pattern=settings.STORAGE_URL_REGEXP,string=text))
        if m is None or not m:
            messaging_callback("Не могу найти ссылку, чтобы прикрепить матч, это какая-то ошибка 😖")
            return
        elif len(m)>1:
            messaging_callback("Слишком много ссылок в сообщении 🤔")
            return

        video_id=m[0].group("video_id")
        return video_id


# Handlers

@bot.message_handler(func=replies_to(from_bot,has_link_to_storage, is_numeric))
def append_match_id(message:Message):
    """Привязывает видео к матчу, если ссылка на матч только одна и получино сообщение из цифр, оно отправлено в ответ на сообщение со ссылкой на видео"""
    message_with_video=message.reply_to_message
    video_id=extract_video_id(message_with_video.text,messaging_callback=lambda text: bot.reply_to(message,text=text))
    match_id=message.text
    #TODO проверка, а существует ли такое видео вообще!

    n=NativeRbData(os.getenv("RBDATA_EMAIL"),os.getenv("RBDATA_PASSWORD"))
    if(n.attach_match(match_id=match_id, video_id=video_id)):
        bot.send_message(chat_id=message.chat.id,text="🙌")
        bot.send_message(chat_id=message.chat.id,text=f"Привязал `видео {video_id}` к `матчу {match_id}`",parse_mode="MARKDOWN") #TODO писать имя видео и матча! или ссылки хотябы            
    else:
        bot.send_message(chat_id=message.chat.id,text="😢")
        bot.send_message(chat_id=message.chat.id,text=f"Я не смог привязать `видео {video_id}` к `матчу {match_id}`",parse_mode="MARKDOWN") 

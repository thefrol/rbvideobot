from rbdata.native_api import NativeRbData
import rbdata
import os
from telebot.types import Message
import re

from ..bot import bot
import settings
from .conditionals import is_a_reply, is_numeric, replies_to, from_bot,has_link_to_storage, and_

SEPARATORS=':='
#TODO переименовать бы в update_video или типа того

# Helpers

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

def extract_parameter(text:str)-> (str,str,bool):
    """Достает параметр из cообщения типа `id=2`
    возвращает: parameter_name str, parameter_value str, success bool
    вернет ("id","2", True) или 
    None, None, False — в случае ошибки в последнем параметре(success) передается False"""
    pattern=rf'(?P<name>\w+)[{SEPARATORS}](?P<value>.*)'
    m=re.search(pattern=pattern,string=text)
    if m is None:
        return None,None,False
    return m.group("name"),m.group("value"), True

def append_match_id(match_id,video_id, messaging_callback):
    n=NativeRbData(os.getenv("RBDATA_EMAIL"),os.getenv("RBDATA_PASSWORD"))
    if(n.attach_match(match_id=match_id, video_id=video_id)):
        messaging_callback(text="🙌")
        messaging_callback(text=f"Привязал `видео {video_id}` к `матчу {match_id}`",parse_mode="MARKDOWN") #TODO писать имя видео и матча! или ссылки хотябы            
    else:
        messaging_callback(text="😢")
        messaging_callback(text=f"Я не смог привязать `видео {video_id}` к `матчу {match_id}`",parse_mode="MARKDOWN") 


# Conditionals

def is_parameter_setting(message:Message):
    """определяет если текст сообщения используется для натройки параметров, то есть имеет вид
    `name=Видео` или `matchid: 123`"""

    return any((sep in message.text for sep in SEPARATORS))
     

# Handlers

@bot.message_handler(func=and_(is_numeric,replies_to(from_bot,has_link_to_storage)))
def on_numeric_reply_to_links(message:Message):
    """Привязывает видео к матчу, если ссылка на матч только одна и получино сообщение из цифр, оно отправлено в ответ на сообщение со ссылкой на видео"""
    reply_to_callback=lambda text,**kwargs: bot.reply_to(message,text=text,**kwargs) #интересно какой-то свой обработчик разве что, который будет не мессадж возвращать а вот такое, объект контекст
    write_to_chat_callback=lambda text,**kwargs: bot.send_message(chat_id=message.chat.id,text=text,**kwargs)
    message_with_video=message.reply_to_message

    video_id=extract_video_id(message_with_video.text,messaging_callback=reply_to_callback)
    match_id=message.text
    #TODO проверка, а существует ли такое видео вообще!
    append_match_id(match_id=match_id, video_id=video_id,messaging_callback=write_to_chat_callback)

# связь параметров и функций, которые они вызывают
func_map={
    ("matchId","match","matchid","match_id"): lambda video_id, value, messaging_callback: append_match_id(video_id=video_id, match_id=value,messaging_callback=messaging_callback),
    ("name","videoName","video_name"): lambda video_id, value, messaging_callback: messaging_callback("Not Implemented")
}

@bot.message_handler(
    func=and_(is_parameter_setting, replies_to(from_bot,has_link_to_storage)))
def on_parametric_message_in_reply_to_link(message:Message):
    reply_to_callback=lambda text,**kwargs: bot.reply_to(message,text=text,**kwargs)
    write_to_chat_callback=lambda text,**kwargs: bot.send_message(chat_id=message.chat.id,text=text,**kwargs)
    message_with_video=message.reply_to_message
    video_id=extract_video_id(message_with_video.text,messaging_callback=reply_to_callback)

    param_name, param_value, success=extract_parameter(message.text)
    if not success:
        bot.send_message(chat_id=message.chat.id,text="🤔 Кажется, это что-то с параметром, но у меня не получается понять что... Сдаюсь")
        return

    #calling a function for specified parameter name
    for params in func_map:
        if param_name in params:
            func_map[params](video_id=video_id,value=param_value,messaging_callback=write_to_chat_callback)
            return

    bot.send_message(chat_id=message.chat.id,text=f"Я ещё пока не умею пользоваться {param_name}")
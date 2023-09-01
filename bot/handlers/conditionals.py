# Тут содержатся всякие полезные условия для обработки сообщений, который используются,
# чтобы определить где какой хендлер для сообщения использовать
# состоит из агреггаторов таких условий, а так же из простых условий
#
# агрегаторы принимают на вход другие условия: 
# and_(is_reply, is_link) - значит и ссылка, и ответ на сообщение
# то есть агрегаторы собирают условия из нескольких других
import re

from telebot.types import Message

def is_yandex_disk_link(message:Message):
    """returns True if message has yandex link in its text
    This is a condition function for handlers"""
    return 'yadi.sk' in message.text or 'disk.yandex.ru' in message.text

def is_link(message:Message):
    """returns True if message has any url in its text
    This is a condition function for handlers"""
    m=re.match(pattern=r"(http|https|ftp)://.*",string=message.text)
    return m is not None

# Aggregators

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
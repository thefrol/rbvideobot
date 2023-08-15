# This example show how to write an inline mode telegram bot use pyTelegramBotAPI.
import logging
import sys
import time
import os
from itertools import starmap

import telebot
from telebot import types

from rbdata import RbData,Video

API_TOKEN = os.getenv('TOKEN')


bot = telebot.TeleBot(API_TOKEN)
telebot.logger.setLevel(logging.DEBUG)

def combine_fist_videos(videos:list[Video],count=3):
    message='\n'.join(f"{video.name} \n {video.url}"  for video in videos[:count])
    return types.InlineQueryResultArticle(
        id=id(message),
        title= 'Три свежайших',
        description='\n'.join([video.name for video in videos]),
        input_message_content=types.InputTextMessageContent(message))


def create_video_article(id:int,video:Video):
    message=f"{video.name} \n {video.url}"
    return types.InlineQueryResultArticle(
        id=str(video.id),
        title= video.name,
        url=video.url,
        description=video.name,
        input_message_content=types.InputTextMessageContent(message))


@bot.inline_handler(lambda query: len(query.query) >=0)
def query_text(inline_query):
    try:
        videos=RbData().get_videos(inline_query.query)
        if videos==None or len(videos)==0:
            bot.answer_inline_query(inline_query.id,results=[]) #maybe block unnecesary
            return
        responses=list(starmap(create_video_article,enumerate(videos)))
        first_videos=combine_fist_videos(videos,3)
        bot.answer_inline_query(inline_query.id, [first_videos,*responses])
    except ValueError as e:
        print(f'inline_handler error {e}')

# @bot.inline_handler(lambda query: len(query.query) == 0)
# def default_query(inline_query):
#     try:
#         r = types.InlineQueryResultArticle('1', 'default', types.InputTextMessageContent('default'))
#         bot.answer_inline_query(inline_query.id, [r])
#     except Exception as e:
#         print(e)


def main_loop():
    bot.infinity_polling(long_polling_timeout=3)
    while 1:
        time.sleep(3)


if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print('\nExiting by user request.\n')
        sys.exit(0)
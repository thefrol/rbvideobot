from itertools import starmap

from telebot import types

from rbdata import RbData,Video
from bot.bot import bot

# importing other handlers
from .upload_video import on_disk_link,on_link

# basic handlers

def create_video_article(id:int,video:Video):
    message=f"{video.name} \n {video.url}"
    return types.InlineQueryResultArticle(
        id=str(video.id),
        title= video.name,
        url=video.url,
        #description=video.name,
        input_message_content=types.InputTextMessageContent(message))


@bot.inline_handler(lambda query: len(query.query) >=0)
def query_text(inline_query):
    try:
        videos=RbData().get_videos(inline_query.query)
        if videos==None or len(videos)==0:
            print("INLINE HANDLER: received no videos")
            bot.answer_inline_query(inline_query.id,results=[]) #maybe block unnecesary
            return
        responses=list(starmap(create_video_article,enumerate(videos)))
        bot.answer_inline_query(inline_query.id, [*responses])
    except ValueError as e:
        print(f'inline_handler error {e}')
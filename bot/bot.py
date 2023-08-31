import logging
import os

import telebot


API_TOKEN = os.getenv('TOKEN')

bot = telebot.TeleBot(API_TOKEN)
telebot.logger.setLevel(logging.WARNING)
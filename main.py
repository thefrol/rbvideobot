# This example show how to write an inline mode telegram bot use pyTelegramBotAPI.
import logging
import sys
import time
import os
from itertools import starmap

import telebot
from telebot import types

from rbdata import RbData,Video
from bot import bot


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
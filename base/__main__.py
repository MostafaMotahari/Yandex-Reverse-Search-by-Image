"""This file has functions for get and search an image in google
and returning the resault.
"""

# Imports
from datetime import date
import re
import configparser
import logging
import time

from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
)

from handlers import *
#from session import engine
#from base_class import Base


# Parsing bot configartion fot reading bot token
config = configparser.ConfigParser()
config.read("base/config.ini")
TOKEN = config['ptb']['bot_token']
updater = Updater(token=TOKEN, use_context=True, workers=24)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


# Dispatchers
dispatcher = updater.dispatcher

start_command_handler = CommandHandler("start", start, run_async=True)
search_photo_handler = MessageHandler(Filters.photo, search_image, run_async=True)
bot_statistics_handler = MessageHandler(Filters.user(1398458529) & Filters.regex("^آمار ربات$"), bot_statistics, run_async=True)
user_statistics_handler = MessageHandler(Filters.user(1398458529) & Filters.regex("^آمار کاربر$"), user_statistics, run_async=True)
public_message_handler = MessageHandler(Filters.user(1398458529) & Filters.regex("^پیام همگانی$"), public_message, run_async=True)

dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(search_photo_handler)
dispatcher.add_handler(bot_statistics_handler)
dispatcher.add_handler(user_statistics_handler)
dispatcher.add_handler(public_message_handler)


# Running bot
if __name__ == "__main__":
    #Base.metadata.create_all(bind=engine)
    updater.start_polling()

import configparser
import re
import requests
import bs4
from time import sleep
from html import escape

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

import session
from db_methods import get_users_list


# Parsing bot configartion fot reading bot token
config = configparser.ConfigParser()
config.read("base/config.ini")
TOKEN = config['ptb']['bot_token']


#Function that gives a page html content
def google_search(file_path, message):
    
    img_url = file_path
    msg = message.reply_text("🔎 *در حال زدن...*", parse_mode="Markdown")
    
    # Get search page
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14', 
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-language': 'en-US,en;q=0.9'}

    while True:
        response = requests.get("https://yandex.com/images/search?rpt=imageview&url=" + img_url, headers=headers)

        # Check for 429
        if response.status_code != 429:
            break

    # Parse all needed information
    b = bs4.BeautifulSoup(response.text, "html.parser")

    # Try parse suggestion
    try:
        find_sug = b.select('.CbirSites-Item')
        titles = []
        counter = 0

        for title in find_sug:
            titles.append(title.text[7:60].split("\n")[0])

            counter += 1

            if counter == 10:
                break

        suggestion = "\n\n".join(titles)

    except Exception as e:
        print(e, "No suggestion")
        suggestion = False

    # Send
    txt = ''
    if suggestion:
        txt = '<b>Main suggestion: \n\n%s</b>\n\n' % escape(suggestion)


    inline_keyboard = []
    inline_keyboard.append([
        InlineKeyboardButton(text="🌐 Search page", url="https://www.google.com/searchbyimage?image_url=" + img_url)
    ])
    msg.edit_text(text=txt, parse_mode='html', reply_markup=InlineKeyboardMarkup(inline_keyboard), disable_web_page_preview=True)


# Creating a local database for temporary requests
def create_local_database():
    db = session.get_db().__next__()

    for user_id in get_users_list(db):
        session.TEMP_DATA.append(user_id)

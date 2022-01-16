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
    open("test.html", "w").write(response.text)
    # Try parse suggestion
    try:
        find_sug = b.select('.CbirSites-Item')
        print(find_sug)
        suggestion = find_sug[0].text
    except Exception as e:
        print(e, "No suggestion")
        suggestion = False

    # Try parse similar
    try:
        find_similar = b.select(".e2BEnf")
        similar = 'https://www.google.com' + str(find_similar[0].a['href'])
    except Exception as e:
        print(e, "No similar")
        similar = False

    # Try parse sites
    try:
        find_sites = b.find_all('div', {'class': 'yuRUbf'})
        sites = [(si.a['href'], si.h3.text) for si in find_sites]
    except Exception as e:
        print(e, "No sites")
        sites = False

    # Send
    txt = ''
    if suggestion:
        txt = '<b>Main suggestion: %s</b>\n\n' % escape(suggestion)

    txt += '<b>Search results:</b>\n\n'
    if sites:
        txt += '\n\n'.join([f'<a href="{escape(site[0])}">{escape(site[1])}</a>' for site in sites])

    inline_keyboard = []
    if similar:
        inline_keyboard.append([
            InlineKeyboardButton(text="🔗 Link to similar images", url=similar)
        ])

    inline_keyboard.append([
        InlineKeyboardButton(text="🌐 Search page", url="https://www.google.com/searchbyimage?image_url=" + img_url)
    ])
    msg.edit_text(text=txt, parse_mode='html', reply_markup=InlineKeyboardMarkup(inline_keyboard), disable_web_page_preview=True)

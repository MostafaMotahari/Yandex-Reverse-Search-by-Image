# Imports
import re

from telegram import Update
from telegram.ext import CallbackContext

from plugins import google_search
from session import get_db, TEMP_DATA
from db_methods import (
    get_users_list,
    sign_up,
    increase_search,
    get_user
)
from models import UserModel
import messages

# Handlers

# Check user verfing
def verify_user(update: Update, user_id: int):
    global TEMP_DATA
    if user_id not in TEMP_DATA:
        update.message.reply_text(
            messages.signup_failed
        )
        return False

    return True


# Start Message
def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    
    if verify_user(update, user_id):
        update.message.reply_text(
            messages.start_msg
        )

# Searching Image
def search_image(update: Update, context: CallbackContext):

    db = get_db().__next__()
    user_id = update.message.from_user.id
    
    if not verify_user(update, user_id):
        return 0        

    google_search(
        update.message.photo[0].get_file().file_path,
        update.message
    )

    increase_search(db, user_id)


# Get bot statistics
def bot_statistics(update: Update, context: CallbackContext):
    # Get users count
    db = get_db().__next__()
    users_list = get_users_list(db)
    users_count = len(users_list)

    # Get total searches count
    # Get banned user count
    searches_count = 0
    banned_count = 0
    for user_id in users_list:
        user: UserModel = get_user(db, user_id)
        searches_count += user.total_searches
        if user.is_banned:
            banned_count += 1

    update.message.reply_text(
        messages.statistics_msg.format(
            str(users_count),
            str(searches_count),
            str(banned_count)
        )
    )


# def ban_user(update: Update, context: CallbackContext):
#     pass

# Get user statistics
def user_statistics(update: Update, context: CallbackContext):
    db = get_db().__next__()
    user_id = update.message.reply_to_message.forward_from.id
    user = get_user(db, user_id)

    if user:
        update.message.reply_text(
            messages.user_statistics_msg.format(
                str(user.total_searches),
                str(user.is_banned)
            )
        )
        return 1

    update.message.reply_text("این کاربر در ربات وجود ندارد!")



# Public message
def public_message(update: Update, context: CallbackContext):
    db = get_db().__next__()
    users_list = get_users_list(db)

    for user_id in users_list:
        try:
            context.bot.send_message(
                user_id,
                update.message.reply_to_message.text
            )
        
        except Exception as e:
            print(e)
            continue

    update.message.reply_text(
        "پیام همگانی با موفقیت ارسال شد!"
    )

# Signup a user by admin
def signup_by_admin(update: Update, context: CallbackContext):
    db = get_db().__next__()

    target_user_id = int(
        re.findall("Id: (.*)", update.message.text)[0]
    )
    sign_up(db, target_user_id)

    update.message.reply_text(
        "کابر مورد نظر با موفقیت ثبت نام شد!✅"
    )

import os
import re
from telegram_bot.api import api
import telebot
import ccxt
from logger import Logger
from pathlib import Path
# the file structure is
# telegram_bot
# -src
#   - telebot.py
# - api.py
# - recv_list.txt
# Only the contents of src and the recv_list.txt file are included for obvious reasons. To use your own api create a file names api.py in the same
# directory as src and make it have a function that returns the api key

bot = telebot.TeleBot(token=api())
logger = Logger()
# print(ccxt.exchanges)
@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, f"Welcome to our telegram bot {message.from_user.first_name}!")
    bot.send_message(message.chat.id, f"Your message id is: {message.chat.id}")
    # First check if the user has a valid code, if so add the users message id to a list which is used to send signals
    # If the code is valid add the user to telegram_bot/recv_list.txt
    with open("../recv_list.txt", "a+") as f:
        path = Path("../logs/bot.log")
        f.seek(0)
        ids = [line.strip() for line in f]

        if str(message.chat.id) not in ids:
            logger.logit("[START]", message.chat.id, message.from_user.first_name, reason="User started receiving signals", path_to_log=path)
            f.write(f"{message.chat.id}\n")
        else:
            # user is already part of the receiving list
            logger.logit("[INFO]", message.chat.id, message.from_user.first_name, reason="User tried to start Bot but its already started", path_to_log=path)

@bot.message_handler(commands=['help'])
def help(message):
    path = Path("../logs/bot.log")
    bot.send_message(message.chat.id, "I'm useless")
    logger.logit(typ="[INFO]", chat_id=message.chat.id, from_user=message.from_user.first_name, reason="User requested help from the bot", path_to_log=path)


@bot.message_handler(commands=['contact'])
def contact(message):
    print("Showing Contact Information to", message.from_user.first_name)
    user = message.from_user.first_name
    bot.send_message(message.chat.id, f"Your Username is: {user}")

@bot.message_handler(commands=['privacy'])
def privacy(message):
    print("Showing Privacy Information to", message.from_user.first_name)
    messages = []
    user_first_name = message.from_user.first_name
    user_last_name = message.from_user.last_name
    user_username = message.from_user.username

    msg = f"Username: {user_username}\nFirst Name: {user_first_name}\nLast Name: {user_last_name}\n Chat ID: {message.chat.id}"

    bot.send_message(
        message.chat.id,
        msg
    )

@bot.message_handler(commands=['contact'])
def contact(message):
    print("Showing Contact Information to", message.from_user.first_name)
    user = message.from_user.first_name
    bot.send_message(message.chat.id, f"Your Username is: {user}") # This is meant to include your busines' contact information, or it should exist at all

@bot.message_handler(commands=['mail'])
def add_to_email_list(message):
    bot.send_message(message.chat.id, 'Enter your email if you want to receive email notifications for signals.')
    bot.register_next_step_handler(message, process_email)

def process_email(message):
    EMAIL_PATTERN = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    #-------------------------------------------
    # use email_validator module instead
    # from email_validator import validate_email
    # email = "abcd8@gmail.com"
    # res = validate_email(email) # throws error if it fails so try/catch it
    # print("Valid Email")
    # _________________DO THIS___________________

    if re.match(EMAIL_PATTERN, message.text):
        path = Path("../logs/bot.log")
        email = message.text
        bot.send_message(message.chat.id, f"Sending a confirmation email to: {email}")
        bot.send_message(message.chat.id, f"This Function is still under construction, you will not receive an email.")
        # Save to database here

        # after that log the event
        logger.logit("[INFO]", message.chat.id, message.from_user.first_name, reason=f"The user registered under the email: {email}", path_to_log=path)
    else:
        bot.reply_to(message, "Please enter a valid email address.")

@bot.message_handler()
def reply_func(message):
    bot.reply_to(message, text="This is a reply")

if __name__ == '__main__':
    bot.polling()



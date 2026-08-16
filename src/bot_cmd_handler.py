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
# Only the contents of src are included for obvious reasons. To use your own api create a file names api.py in the same
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
            # log.log_new_start(message.chat.id, message.from_user.first_name, path)
            logger.logit("[START]", message.chat.id, message.from_user.first_name, reason="User started receiving signals", path_to_log=path)
            f.write(f"{message.chat.id}\n")
        else:
            # user is already part of the signaling list
            # log.log_bad_start(message.chat.id, message.from_user.first_name, path)
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
    msg1 = f"You can find our privacy statement under xxx.xx/privacy.html \nThe statement contains information regarding the storage of user data \n In order to comply with local and state authority we have also included a short summary of the processes that are carried out on personal data."
    msg2 = f"Telegram user IDs, Usernames"
    msg3 = f"Telegram user IDs, Usernames, first and last names saved to the account and the email the user registers t"
    msg4 = f"Data Retention Policy: \n"
    msg5 = f"All your privacy related information is shown below. \nPlease note that this information is always being processed and sent to the bot by Telegram when users interact with it. \n As such we have no way to restrict this information. We do however minimize it to only use what is strictly required. For our data retention policy, please look to our privacy statement or the summary above."
    msg6 = f"Username: {user_username}\nFirst Name: {user_first_name}\nLast Name: {user_last_name}\n Chat ID: {message.chat.id}"

    messages.append(msg1)
    messages.append(msg2)
    messages.append(msg3) # I know I know this sucks ill load it from a different file soon just hold up
    messages.append(msg4)
    messages.append(msg5)
    messages.append(msg6)
    for msg in messages:
        bot.send_message(
            message.chat.id,
            msg
        )


@bot.message_handler(commands=['contact'])
def contact(message):
    print("Showing Contact Information to", message.from_user.first_name)
    user = message.from_user.first_name
    bot.send_message(message.chat.id, f"Your Username is: {user}")
@bot.message_handler(commands=['mail'])
def add_to_email_list(message):
    bot.send_message(message.chat.id, 'Enter your email if you want to receive email notifications for signals.')
    bot.register_next_step_handler(message, process_email)


def process_email(message):
    EMAIL_PATTERN = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    if re.match(EMAIL_PATTERN, message.text):
        path = Path("../logs/bot.log")
        email = message.text
        bot.send_message(message.chat.id, f"Sending a confirmation email to: {email}")
        bot.send_message(message.chat.id, f"This Function is still under construction, you will not receive an email.")
        # Save to your database here

        # after that log the event
        logger.logit("[INFO]", message.chat.id, message.from_user.first_name, reason=f"The user registered under the email: {email}", path_to_log=path)
    else:
        bot.reply_to(message, "Please enter a valid email address.")
@bot.message_handler()
def reply_func(message):
    bot.reply_to(message, text="This is a reply")

if __name__ == '__main__':
    bot.polling()



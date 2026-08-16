import bot_cmd_handler
import re
from telegram_bot.api import api
import telebot
import time

bot = telebot.TeleBot(token=api())
# the bot constantly sends messages to
def send_signal():
    # load the list of signal receiver message ids
    #
    while True:
        recv_list = open("../recv_list.txt", "r")
        for message_id in recv_list:
            bot.send_message(int(message_id), f"This will come every 10 seconds ")
        time.sleep(10)
        return
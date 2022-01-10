import os
import re
import platform

import telebot

import config

bot = telebot.TeleBot(config.token)

regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)



def validate(url):
    return (re.match(regex, url) is not None)


def dir_exist(path):
        if os.path.exists(path):
                if bool(os.listdir(path)):
                        return True
                else:
                        return False
        else:
                return False

def error_message_answer_bot(message, error_num):

        if error_num == 2:
                bot.send_message(message.chat.id, f'Скорее всего введен не верный URL, элементы не найдены на странице')


def slash_valid_end (message):

        if message.text.endswith('/'):
                message.text=message.text[0:-1]
                slash_valid_end(message)


        return message

def slash_valid_begin(message):
        if message.text[0] != '/':
                message.text= '/' + message.text

        return message


if platform.uname().system in ('Linux', 'Darwin'):
    slash = '/'
else:
    slash = '\\'
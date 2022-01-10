'''Чукча не писатель'''
import os
import platform

import telebot
from telebot import types
from models import MainTestPicture
import config
import services
import utils

bot = telebot.TeleBot(config.token)
slash = services.slash


# ответ на команду start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     f"Этот бот предназначен для сравнивания одних и тех же блоков на страницах сайта, но на разных стендах или в разное время (до и после релиза, сборки, обновления.)\n\n"
                     f"Вопросы и предложения @pirog\n\n"
                     f"/help - сраница помощи\n\n"
                     f"Стенд — это ссылка на сайт (http://vprok.ru), стенд (http://fo.dev02.services.lab.x5.ru), стейдж (vpr-app01.im.perekrestok.ru). В общем любой апп где есть FO.\n\n"
                     f"Ссылка – часть ссылки после домена (стенда). Например, карточка товара, страница доставки.\n\n"
                     f"Для теста станиц новый покупатель, header/footer, в меню вводить ссылку необязательно, достаточно указать стенд.\n\n"
                     f"Во время теста страницы доставки принудительно убирается карта и рекламный баннер, для статичности страницы\n\n"
                     f"Порядок работы:\n\n"
                     f"0.	/config\n"
                     f"1.	Ввести Стенд\n"
                     f"2.	Ввести ссылку (если необходимо)\n"
                     f"3.	Выбрать необходимый шаблон\n"
                     f"4.	Изменить стенд, или дождаться релиза, пересобрать проект\n"
                     f"5.	Выбрать необходимый тест\n\n"

                     f"Шаблон * - бот создаст шаблон, с которым в последствии будет сравниваться тест.\n\n"
                     f"Тест * - загрузка блоков указанной страницы и сравнение их со сделанным ранее шаблоном. Если тест прошел без ошибок и различия в блоках не найдены, выдается сообщение: Тест прошел без ошибок.\n\n"
                     f" Если есть различия, то выдается сообщение: Тест провален с прикрепленным изображением склеенным из трех изображений: Шаблон + Тест + Результат.\n"
                     f" На изображении результата красным выделены, те места в которых есть различия.\n\n")


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id,
                     f"Для теста станиц новый покупатель, header/footer, в меню вводить ссылку необязательно, достаточно указать стенд.\n\n"
                     f"Во время теста страницы доставки принудительно убирается карта и рекламный баннер, для статичности страницы\n\n"
                     f"Порядок работы:\n\n"
                     f"0.	/config\n"
                     f"1.	Ввести Стенд\n"
                     f"2.	Ввести ссылку (если необходимо)\n"
                     f"3.	Выбрать необходимый шаблон\n"
                     f"4.	Изменить стенд, или дождаться релиза, пересобрать проект\n"
                     f"5.	Выбрать необходимый тест\n\n\n"
                     f"/start – справка\n\n"
                     f"/config – просмотр конфигурации и выбор необходимого теста.\n\n"
                     f"/help - сраница помощи\n\n"
                     )


@bot.message_handler(commands=["config"])
def config(message):
    # Смотрим есть ли сохраненый ранее конфиг у пользователей

    user_dict = utils.get_user_dict(message.chat.id)
    # Если нет создаем пустой список
    if user_dict == None:
        user_dict = [None, None]
        utils.set_user_dict(message.chat.id, user_dict)

    # Создаем кнопки и записываем их в переменную
    markup = types.InlineKeyboardMarkup(row_width=2)
    bt1 = types.InlineKeyboardButton('Стенд', callback_data="Stend")
    bt2 = types.InlineKeyboardButton('Ссылка', callback_data="Link")
    bt3 = types.InlineKeyboardButton('Шаблон New-Customer', callback_data="template_new_customer")
    bt4 = types.InlineKeyboardButton('Тест New-Customer', callback_data="test_template_new_customer")
    bt5 = types.InlineKeyboardButton('Шаблон Delivery', callback_data="template_delivery")
    bt6 = types.InlineKeyboardButton('Тест Delivery', callback_data="test_template_delivery")
    bt7 = types.InlineKeyboardButton('Шаблон Карточки товара', callback_data="template_product")
    bt8 = types.InlineKeyboardButton('Тест Карточки товара', callback_data="test_template_product")
    bt9 = types.InlineKeyboardButton('Шаблон Header/Footer', callback_data="template_headfoot")
    bt10 = types.InlineKeyboardButton('Тест Header/Footer', callback_data="test_template_headfoot")
    bt11 = types.InlineKeyboardButton('Шаблон Главная', callback_data="template_home")
    bt12 = types.InlineKeyboardButton('Тест Главная', callback_data="test_template_home")
    bt13 = types.InlineKeyboardButton('Шаблон Меню', callback_data="template_menu")
    bt14 = types.InlineKeyboardButton('Тест Меню', callback_data="test_template_menu")

    markup.add(bt1, bt2, bt3, bt4, bt5, bt6, bt7, bt8, bt9, bt10, bt13, bt14)

    # Пишем что конфиг пользователя пуст если он пуст или выводим сохраненный конфиг
    try:

        if (user_dict[0] or user_dict[1]) is None:
            bot.send_message(message.chat.id, 'Конфиг пуст', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, str(user_dict[0]) + str(user_dict[1]) +
                             f"\n\n"
                             f"/start – справка\n\n"
                             f"/help - сраница помощи\n\n"
                             f"/config – просмотр конфигурации и выбор необходимого теста.\n\n"
                             ,
                             reply_markup=markup)
    except KeyError:
        bot.send_message(message.chat.id, 'Конфиг пуст',
                         reply_markup=markup)


'''Реакция на нажатие кнопок в зависимости от того какая callback_data 
 происходит соответсвующий вызов функции'''


@bot.callback_query_handler(func=lambda c: True)
def callback(c):
    if c.data == 'Stend':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        bot.answer_callback_query(c.id, text='Введите адрес стенда')
        bt1 = types.KeyboardButton('Отмена')
        markup.add(bt1)
        msg = bot.send_message(c.message.chat.id, f'Введите адрес стенда',
                               reply_markup=markup)
        bot.register_next_step_handler(msg, add_stend)
    if c.data == 'Link':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        bot.answer_callback_query(c.id, text='Введите ссылку...')
        bt1 = types.KeyboardButton('Отмена')
        markup.add(bt1)
        msg = bot.send_message(c.message.chat.id, f'Введите ссылку на продукт',
                               reply_markup=markup)
        bot.register_next_step_handler(msg, add_link)
    if c.data == 'template_new_customer':
        bot.answer_callback_query(c.id, text='Получаешм шаблон')
        bot.send_message(c.message.chat.id,
                         'Получаешм шаблон страницы новый покупатель')
        get_template_new_customer(c.message)
    if c.data == 'test_template_new_customer':
        bot.answer_callback_query(c.id, text='Начало теста')
        bot.send_message(c.message.chat.id,
                         'Начало теста страницы новый покупатель')
        test_picture_new_customer(c.message)
    if c.data == 'template_delivery':
        bot.answer_callback_query(c.id, text='Получаешм шаблон')
        bot.send_message(c.message.chat.id,
                         'Получаешм шаблон страницы доставки')
        get_template_delivery(c.message)
    if c.data == 'test_template_delivery':
        bot.answer_callback_query(c.id, text='Начало теста')

        bot.send_message(c.message.chat.id,
                         'Начало теста страницы доставки')
        test_picture_delivery(c.message)
    if c.data == 'template_product':
        bot.answer_callback_query(c.id, text='Получаешм шаблон')

        bot.send_message(c.message.chat.id,
                         'Получаешм шаблон карточки товара')
        get_template_product(c.message)
    if c.data == 'test_template_product':
        bot.answer_callback_query(c.id, text='Начало теста')

        bot.send_message(c.message.chat.id,
                         'Начало теста карточки товара')
        test_template_product(c.message)
    if c.data == 'template_headfoot':
        bot.answer_callback_query(c.id, text='Получаешм шаблон')

        bot.send_message(c.message.chat.id,
                         'Получаешм шаблон Хедера и Футера')
        get_template_headfoot(c.message)
    if c.data == 'test_template_headfoot':
        bot.answer_callback_query(c.id, text='Начало теста')

        bot.send_message(c.message.chat.id,
                         'Начало теста Хедера и Футера')
        test_template_headfoot(c.message)
    if c.data == 'template_home':
        bot.answer_callback_query(c.id, text='Получаешм шаблон')

        bot.send_message(c.message.chat.id,
                         'Получаешм шаблон главной станицы')
        get_template_home(c.message)
    if c.data == 'test_template_home':
        bot.answer_callback_query(c.id, text='Начало теста')

        bot.send_message(c.message.chat.id,
                         'Начало теста главной станицы')
        test_template_home(c.message)
    if c.data == 'template_menu':
        bot.answer_callback_query(c.id, text='Получаешм шаблон')

        bot.send_message(c.message.chat.id,
                         'Получаешм шаблон Меню')
        get_template_menu(c.message)
    if c.data == 'test_template_menu':
        bot.answer_callback_query(c.id, text='Начало теста')

        bot.send_message(c.message.chat.id,
                         'Начало теста Меню')
        test_template_menu(c.message)


# Добавление ссылки на стенд в конфиг и его сохранение
def add_stend(message):
    chat_id = message.chat.id

    markup = types.ReplyKeyboardRemove(selective=False)
    if message.text != 'Отмена':
        try:
            user_dict = utils.get_user_dict(chat_id)

            if user_dict == None:
                user_dict = [None, None]
            message = services.slash_valid_end(message)

            user_dict[0] = message.text
            utils.set_user_dict(chat_id, user_dict)
        except KeyError:
            None
        bot.send_message(chat_id, f'Стенд  {message.text} добавлен в  /config', reply_markup=markup)
    else:
        bot.send_message(chat_id, 'Стенд не обновлен', reply_markup=markup)


# ДОбавление ссылки и ее сохрание в конфиг
def add_link(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardRemove(selective=False)
    if message.text != 'Отмена':
        try:
            user_dict = utils.get_user_dict(chat_id)
            if user_dict == None:
                user_dict = [None, None]
            message = services.slash_valid_begin(message)
            user_dict[1] = message.text
            utils.set_user_dict(chat_id, user_dict)
        except KeyError:
            None
        bot.send_message(chat_id, f'Ссылка   {message.text} добавлена в /config', reply_markup=markup)
    else:
        bot.send_message(chat_id, 'Ссылка не обновлена', reply_markup=markup)


# Получение шаблона страницы новый покупатель
def get_template_new_customer(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardRemove(selective=False)
    # Читаем конфиг
    user_dict = utils.get_user_dict(chat_id)
    # Проверяем валидность url
    url = str(user_dict[0]) + '/new-customer'
    if services.validate(url):
        # Вызов функции получения и сохранения шаблона

        crash_list = MainTestPicture().get_new_cutomer_template(message, url)
        if crash_list:
            if crash_list[0] == 'Error':
                services.error_message_answer_bot(message, 2)
        else:
            bot.send_message(chat_id, f'Шаблон готов', reply_markup=markup)


    else:
        bot.send_message(chat_id, f'Не верный URl', reply_markup=markup)


# Получение шаблона страницы товара
def get_template_product(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardRemove(selective=False)
    # Читаем конфиг

    user_dict = utils.get_user_dict(chat_id)
    # Проверяем валидность url

    url = str(user_dict[0]) + str(user_dict[1])
    if services.validate(url):
        # Вызов функции получения и сохранения шаблона

        crash_list = MainTestPicture().get_product_template(message, url)
        if crash_list:
            if crash_list[0] == 'Error':
                services.error_message_answer_bot(message, 2)
        else:
            bot.send_message(chat_id, f'Шаблон готов', reply_markup=markup)
    else:
        bot.send_message(chat_id, f'Не верный URl', reply_markup=markup)


# Получение шаблона хедера и футера
def get_template_headfoot(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardRemove(selective=False)
    # Читаем конфиг

    user_dict = utils.get_user_dict(chat_id)
    # Проверяем валидность url

    url = str(user_dict[0]) + '/'
    if services.validate(url):
        # Вызов функции получения и сохранения шаблона
        crash_list = MainTestPicture().get_headfoot_template(message, url)
        if crash_list:
            if crash_list[0] == 'Error':
                services.error_message_answer_bot(message, 2)
        else:
            bot.send_message(chat_id, f'Шаблон готов', reply_markup=markup)

    else:
        bot.send_message(chat_id, f'Не верный URl', reply_markup=markup)


# Получение шаблона меню каталога
def get_template_menu(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardRemove(selective=False)
    # Читаем конфиг

    user_dict = utils.get_user_dict(chat_id)
    # Проверяем валидность url

    url = str(user_dict[0]) + '/'
    if services.validate(url):
        # Вызов функции получения и сохранения шаблона
        crash_list = MainTestPicture().get_menu_template(message, url)
        if crash_list:
            if crash_list[0] == 'Error':
                services.error_message_answer_bot(message, 2)
        else:
            bot.send_message(chat_id, f'Шаблон готов', reply_markup=markup)

    else:
        bot.send_message(chat_id, f'Не верный URl', reply_markup=markup)


# Получение шаблона главной страницы
def get_template_home(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardRemove(selective=False)
    # Читаем конфиг

    user_dict = utils.get_user_dict(chat_id)
    # Проверяем валидность url

    url = str(user_dict[0]) + '/'
    if services.validate(url):
        # Вызов функции получения и сохранения шаблона
        crash_list = MainTestPicture().get_home_template(message, url)
        if crash_list:
            if crash_list[0] == 'Error':
                services.error_message_answer_bot(message, 2)
        else:
            bot.send_message(chat_id, f'Шаблон готов', reply_markup=markup)

    else:
        bot.send_message(chat_id, f'Не верный URl', reply_markup=markup)


# Получение шаблона страницы доставки
def get_template_delivery(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardRemove(selective=False)
    # Читаем конфиг

    user_dict = utils.get_user_dict(chat_id)
    # Проверяем валидность url

    url = str(user_dict[0]) + str(user_dict[1])
    if services.validate(url):
        # Вызов функции получения и сохранения шаблона
        crash_list = MainTestPicture().get_delivery_template(message, url)

        if crash_list:
            if crash_list[0] == 'Error':
                services.error_message_answer_bot(message, 2)
        else:
            bot.send_message(chat_id, f'Шаблон готов', reply_markup=markup)

    else:
        bot.send_message(chat_id, f'Не верный URl', reply_markup=markup)


# Тест шаблона страницы доставки

def test_picture_new_customer(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardRemove(selective=False)
    # Одинаковые действия разница только в ОС
    if services.dir_exist(
            os.getcwd() + slash + 'images' + slash + str(chat_id) + slash + 'new-customer' + slash + 'template'):
        user_dict = utils.get_user_dict(chat_id)
        url = str(user_dict[0]) + '/new-customer'
        if services.validate(url):

            crash_list = MainTestPicture().test_picture_new_customer(message, url)
            if crash_list:
                if crash_list[0] == 'Error':
                    services.error_message_answer_bot(message, 2)
                else:
                    path = os.getcwd() + slash + 'images' + slash + str(
                        message.chat.id) + slash + 'new-customer' + slash + 'result' + slash
                    for pic in crash_list:
                        image = open(path + pic, 'rb')
                        bot.send_document(chat_id, image)

                        bot.send_message(chat_id, f'Тест провален: ' + str(pic), reply_markup=markup)

            else:
                bot.send_message(chat_id, f'Тест прошел без ошибок', reply_markup=markup)

        else:
            bot.send_message(chat_id, f'Не верный URl', reply_markup=markup)
    else:
        bot.send_message(chat_id, f'Сначала сделайте шаблон станицы новый покупатель', reply_markup=markup)


def test_template_product(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardRemove(selective=False)
    # Проверка есть ли папка шаблона

    if services.dir_exist(
            os.getcwd() + slash + 'images' + slash + str(chat_id) + slash + 'product' + slash + 'template'):
        # Читаем конфиг

        user_dict = utils.get_user_dict(chat_id)
        # Проверяем валидность url

        url = str(user_dict[0]) + str(user_dict[1])
        if services.validate(url):
            '''Вызов функции получения тестового изображения для сравнения его с шаблоном, в результате crash_list 
                                             с именами файлов из папки rezult которые отдаем пользователю в чат. Если crash_list пуст 
                                             возвращаем сообщение что тест пройден'''
            crash_list = MainTestPicture().test_picture_product(message, url)
            if crash_list:
                if crash_list[0] == 'Error':
                    services.error_message_answer_bot(message, 2)
                else:
                    path = os.getcwd() + slash + 'images' + slash + str(
                        message.chat.id) + slash + 'product' + slash + 'result' + slash
                    for pic in crash_list:
                        image = open(path + pic, 'rb')
                        bot.send_document(chat_id, image)

                        bot.send_message(chat_id, f'Тест провален: ' + str(pic), reply_markup=markup)

            else:
                bot.send_message(chat_id, f'Тест прошел без ошибок', reply_markup=markup)
        else:
            bot.send_message(chat_id, f'Не верный URl', reply_markup=markup)
    else:
        bot.send_message(chat_id, f'Сначала сделайте шаблон карточки товара', reply_markup=markup)


def test_template_headfoot(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardRemove(selective=False)
    # Проверка есть ли папка шаблона

    if services.dir_exist(
            os.getcwd() + slash + 'images' + slash + str(chat_id) + slash + 'headfoot' + slash + 'template'):
        # Читаем конфиг

        user_dict = utils.get_user_dict(chat_id)
        # Проверяем валидность url

        url = str(user_dict[0]) + '/'
        if services.validate(url):
            '''Вызов функции получения тестового изображения для сравнения его с шаблоном, в результате crash_list 
                                             с именами файлов из папки rezult которые отдаем пользователю в чат. Если crash_list пуст 
                                             возвращаем сообщение что тест пройден'''
            crash_list = MainTestPicture().test_picture_headfoot(message, url)
            if crash_list:
                if crash_list[0] == 'Error':
                    services.error_message_answer_bot(message, 2)
                else:
                    path = os.getcwd() + slash + 'images' + slash + str(
                        message.chat.id) + slash + 'headfoot' + slash + 'result' + slash
                    for pic in crash_list:
                        image = open(path + pic, 'rb')
                        bot.send_document(chat_id, image)

                        bot.send_message(chat_id, f'Тест провален: ' + str(pic), reply_markup=markup)

            else:
                bot.send_message(chat_id, f'Тест прошел без ошибок', reply_markup=markup)
        else:
            bot.send_message(chat_id, f'Не верный URl', reply_markup=markup)
    else:
        bot.send_message(chat_id, f'Сначала сделайте шаблон Хедера\\Футера', reply_markup=markup)


def test_template_menu(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardRemove(selective=False)
    # Проверка есть ли папка шаблона

    if services.dir_exist(os.getcwd() + slash + 'images' + slash + str(chat_id) + slash + 'menu' + slash + 'template'):
        # Читаем конфиг

        user_dict = utils.get_user_dict(chat_id)
        # Проверяем валидность url

        url = str(user_dict[0]) + '/'
        if services.validate(url):
            '''Вызов функции получения тестового изображения для сравнения его с шаблоном, в результате crash_list 
                                             с именами файлов из папки rezult которые отдаем пользователю в чат. Если crash_list пуст 
                                             возвращаем сообщение что тест пройден'''
            crash_list = MainTestPicture().test_picture_menu(message, url)
            if crash_list:
                if crash_list[0] == 'Error':
                    services.error_message_answer_bot(message, 2)
                else:

                    path = os.getcwd() + slash + 'images' + slash + str(
                        message.chat.id) + slash + 'menu' + slash + 'result' + slash
                    for pic in crash_list:
                        image = open(path + pic, 'rb')
                        bot.send_document(chat_id, image)

                        bot.send_message(chat_id, f'Тест провален: ' + str(pic), reply_markup=markup)

            else:
                bot.send_message(chat_id, f'Тест прошел без ошибок', reply_markup=markup)
    else:
        bot.send_message(chat_id, f'Сначала сделайте шаблон Главной', reply_markup=markup)


def test_template_home(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardRemove(selective=False)

    # Проверка есть ли папка шаблона

    if services.dir_exist(os.getcwd() + slash + 'images' + slash + str(chat_id) + slash + 'home' + slash + 'template'):
        # Читаем конфиг

        user_dict = utils.get_user_dict(chat_id)
        # Проверяем валидность url

        url = str(user_dict[0]) + '/'
        if services.validate(url):
            '''Вызов функции получения тестового изображения для сравнения его с шаблоном, в результате crash_list 
                                             с именами файлов из папки rezult которые отдаем пользователю в чат. Если crash_list пуст 
                                             возвращаем сообщение что тест пройден'''
            crash_list = MainTestPicture().test_picture_home(message, url)
            if crash_list:
                if crash_list[0] == 'Error':
                    services.error_message_answer_bot(message, 2)
                else:

                    path = os.getcwd() + slash + 'images' + slash + str(
                        message.chat.id) + slash + 'home' + slash + 'result' + slash
                    for pic in crash_list:
                        image = open(path + pic, 'rb')
                        bot.send_document(chat_id, image)

                        bot.send_message(chat_id, f'Тест провален: ' + str(pic), reply_markup=markup)

            else:
                bot.send_message(chat_id, f'Тест прошел без ошибок', reply_markup=markup)
    else:
        bot.send_message(chat_id, f'Сначала сделайте шаблон Главной', reply_markup=markup)


def test_picture_delivery(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardRemove(selective=False)

    # Проверка есть ли папка шаблона

    if services.dir_exist(
            os.getcwd() + slash + 'images' + slash + str(chat_id) + slash + 'delivery' + slash + 'template'):
        # Читаем конфиг

        user_dict = utils.get_user_dict(chat_id)
        # Проверяем валидность url

        url = str(user_dict[0]) + str(user_dict[1])
        if services.validate(url):
            '''Вызов функции получения тестового изображения для сравнения его с шаблоном, в результате crash_list 
                                             с именами файлов из папки rezult которые отдаем пользователю в чат. Если crash_list пуст 
                                             возвращаем сообщение что тест пройден'''
            crash_list = MainTestPicture().test_picture_delivery(message, url)
            if crash_list:
                if crash_list[0] == 'Error':
                    services.error_message_answer_bot(message, 2)
                else:

                    path = os.getcwd() + slash + 'images' + slash + str(
                        message.chat.id) + slash + 'delivery' + slash + 'result' + slash
                    for pic in crash_list:
                        image = open(path + pic, 'rb')
                        bot.send_document(chat_id, image)

                        bot.send_message(chat_id, f'Тест провален: ' + str(pic), reply_markup=markup)

            else:
                bot.send_message(chat_id, f'Тест прошел без ошибок', reply_markup=markup)

        else:
            bot.send_message(chat_id, f'Не верный URl', reply_markup=markup)
    else:
        bot.send_message(chat_id, f'Сначала сделайте шаблон станицы доставки', reply_markup=markup)


if __name__ == '__main__':
    bot.remove_webhook()

    bot.polling(none_stop=True)

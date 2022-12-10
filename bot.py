import telebot
from telebot import types
from Globals import TOKEN, CHOICES1, CHOICES2, LANGUAGES, HELPTEXT
from Shifr import shifr
import codecs
import os


def cryptbot():
    value1 = ''
    value2 = ''
    language = ''
    flag_key = bool(False)
    key = ''
    bot = telebot.TeleBot(TOKEN)

    def languages(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton(LANGUAGES[0])
        button2 = types.KeyboardButton(LANGUAGES[1])
        button3 = types.KeyboardButton("Назад1")
        button4 = types.KeyboardButton('Помощь')
        markup.add(button1, button2, button3, button4)
        bot.send_message(message.chat.id, text="Выбирайте язык", reply_markup=markup)

    def regim(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton(CHOICES1[0])
        button2 = types.KeyboardButton(CHOICES1[1])
        button3 = types.KeyboardButton(CHOICES1[2])
        button4 = types.KeyboardButton("Назад2")
        button5 = types.KeyboardButton('Помощь')
        markup.add(button1, button2, button3, button4, button5)
        bot.send_message(message.chat.id, text="Выбирайте режим", reply_markup=markup)

    def method(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton(CHOICES2[0])
        button2 = types.KeyboardButton(CHOICES2[1])
        button3 = types.KeyboardButton(CHOICES2[2])
        button4 = types.KeyboardButton("Назад3")
        button5 = types.KeyboardButton('Помощь')
        markup.add(button1, button2, button3, button4, button5)
        bot.send_message(message.chat.id, text="Выбирайте метод", reply_markup=markup)

    @bot.message_handler(commands=['start'])
    def start(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Выбрать язык")
        button2 = types.KeyboardButton('Помощь')
        markup.add(button1, button2)
        bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}! Я шифрую сообщения", reply_markup=markup)

    @bot.message_handler(commands=['help'])
    def helper(message):
        bot.send_message(message.chat.id, HELPTEXT)

    @bot.message_handler(content_types=['text'])
    def cripttext(message):
        nonlocal value1, value2, language, flag_key, key
        if message.text == 'Помощь':
            bot.send_message(message.chat.id, HELPTEXT)
        elif message.text == 'Назад1':
            start(message)
        elif message.text in ['Выбрать язык', 'Назад2']:
            languages(message)
        elif message.text in LANGUAGES:
            language = message.text
            regim(message)
        elif message.text == 'Назад3':
            regim(message)
        elif message.text in CHOICES1:
            value1 = message.text
            method(message)
        elif message.text in CHOICES2:
            flag_key = False
            value2 = message.text
            if value1 == CHOICES1[2] or (value1 == CHOICES1[0] and value2 == CHOICES2[2]):
                flag_key = True
                bot.send_message(message.chat.id, text="Отправьте текст сообщения или txt файл")
            else:
                bot.send_message(message.chat.id, text="Введите ключ или шаг")
        elif flag_key and value1 and value2 and language:
            array = shifr(message.text, language, value1, value2, key)
            for value in array:
                bot.send_message(message.chat.id, text=value)
        else:
            key = message.text
            flag_key = True
            bot.send_message(message.chat.id, text="Ключ выбран\nОтправьте текст сообщения или txt файл")

    @bot.message_handler(content_types=['document'])
    def criptdocument(message):
        nonlocal flag_key, value1, value2, language, key
        if flag_key and value1 and value2 and language:
            try:
                file_info = bot.get_file(message.document.file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                file = message.document.file_name
                with open(file, 'wb') as f:
                    f.write(downloaded_file)
                stroka = ''
                with codecs.open(file, encoding='utf-8') as f:
                    for value in f:
                        stroka += value
                array = shifr(stroka, language, value1, value2, key)
                with open(file, 'w', encoding='utf-8') as f:
                    for value in array:
                        f.write(value)
                        f.write('\n')
                bot.send_document(message.chat.id, open(file, "rb"))
                os.remove(file)

            except Exception as exception:
                bot.reply_to(message, str(exception))
        else:
            bot.send_message(message.chat.id, text="Язык/метод/режим работы/ключ не введены")

    bot.infinity_polling()

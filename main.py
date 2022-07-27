import os
import telebot
import logging
import psycopg2
from telebot import types
from config import *
from flask import Flask, request

bot = telebot.TeleBot(BOT_TOKEN)
server = Flask(__name__)
logger = telebot.logger
logger.setLevel(logging.DEBUG)

db_connection = psycopg2.connect(DB_URI, sslmode='require')
db_object = db_connection.cursor()


def update_messages_count(user_id):
    db_object.execute(f"UPDATE users SET messages = messages + 1 WHERE id = {user_id}")
    db_connection.commit()


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    username = message.from_user.username
    bot.reply_to(message, f'Hi, {username}')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    schedule = types.KeyboardButton("Расписание")
    events = types.KeyboardButton("Мероприятия")
    clubs = types.KeyboardButton("Присоединиться к клубу")
    diary = types.KeyboardButton("Переход в СУШ")
    grades = types.KeyboardButton("Калькулятор оценок и анализ")
    food = types.KeyboardButton("Сегодняшнее меню")
    markup.add(schedule, events, clubs, diary, grades, food)
    bot.send_message(message.chat.id, "Подробную информацию можно найти, нажав на кнопки меню", reply_markup=markup)

    db_object.execute(f"SELECT id FROM users WHERE id = {user_id}")
    result = db_object.fetchone()

    if not result:
        db_object.execute("INSERT INTO users(id, username, messages) VALUES (%s, %s, %s)", (user_id, username, 0))
        db_connection.commit()

    update_messages_count(user_id)


@bot.message_handler(content_types=['text'])
def get_text_from_user(message):
    if message.text == "Расписание":
            markup_inline = types.InlineKeyboardMarkup()
            item_1 = types.InlineKeyboardButton(text='Уроки', callback_data="subjects")
            item_2 = types.InlineKeyboardButton(text="Распорядок дня", callback_data="day")
            markup_inline.add(item_1)
            markup_inline.add(item_2)
            bot.send_message(message.chat.id, "Выберите нужную опцию", reply_markup=markup_inline)
    elif message.text == "Аккаунт в телеграм":
            markup_inline = types.InlineKeyboardMarkup()
            item_2 = types.InlineKeyboardButton(text="Нажми", url="https://t.me/joinchat/VPcI0_xVOL_cRD3d")
            markup_inline.add(item_2)
            bot.send_message(message.chat.id, "Нажми для перехода в Telegram", reply_markup=markup_inline)
    elif message.text == "О проекте":
            markup_inline = types.InlineKeyboardMarkup()
            a = "1. Проект был создан для распространения информации о существовании кондитерской с пользой для здоровья.\n"
            b = "2. Проект был создан в 2020 году.\n"
            reply = a + b
            bot.send_message(message.chat.id, reply)
    elif message.text == "Посмотреть галерею":
            pic = 'https://mykaleidoscope.ru/uploads/posts/2020-01/1579933448_22-p-kremovie-torti-34.jpg'
            bot.send_photo(message.chat.id, pic)
    elif message.text == "Посмотреть видео":
            markup_inline = types.InlineKeyboardMarkup()
            item_3 = types.InlineKeyboardButton(text="Посмотреть", url="https://youtu.be/-wcXHxotvUg")
            markup_inline.add(item_3)
            bot.send_message(message.chat.id, "Нажми для просмотра видео", reply_markup=markup_inline)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == 'subjects':
        markup_inline = types.InlineKeyboardMarkup()
        item_3 = types.InlineKeyboardButton(text='7', callback_data="seven")
        item_4 = types.InlineKeyboardButton(text="8", callback_data="eight")
        item_5 = types.InlineKeyboardButton(text="9", callback_data="nine")
        item_6 = types.InlineKeyboardButton(text="10", callback_data="ten")
        item_7 = types.InlineKeyboardButton(text="11", callback_data="eleven")
        item_8 = types.InlineKeyboardButton(text="12", callback_data="twelve")
        markup_inline.add(item_3)
        markup_inline.add(item_4)
        markup_inline.add(item_5)
        markup_inline.add(item_6)
        markup_inline.add(item_7)
        markup_inline.add(item_8)
        bot.send_message(message.chat.id, "Выберите нужную опцию", reply_markup=markup_inline)
        if call.data == 'seven':
            markup_inline = types.InlineKeyboardMarkup()
            item_9 = types.InlineKeyboardButton(text='A', callback_data="first")
            item_10 = types.InlineKeyboardButton(text="B", callback_data="second")
            item_11 = types.InlineKeyboardButton(text="C", callback_data="third")
            item_12 = types.InlineKeyboardButton(text="D", callback_data="fourth")
            item_13 = types.InlineKeyboardButton(text="E", callback_data="fifth")
            item_14 = types.InlineKeyboardButton(text="K", callback_data="sixth")
            item_15 = types.InlineKeyboardButton(text="L", callback_data="seventh")
            item_16 = types.InlineKeyboardButton(text="M", callback_data="eighth")
            markup_inline.add(item_9, item_10, item_15, item_16)
            markup_inline.add(item_11, item_12)
            markup_inline.add(item_13, item_14)
            markup_inline.add(item_15, item_16)
            bot.send_message(message.chat.id, "Выберите нужную опцию", reply_markup=markup_inline)
            if call.data =='A':
                photo = open('Снимок.png', 'rb')
                bot.send_photo(message.chat.id, photo, parse_mode='html')


@bot.message_handler(commands=["stats"])
def get_stats(message):
    db_object.execute("SELECT * FROM users ORDER BY messages DESC LIMIT 10")
    result = db_object.fetchall()

    if not result:
        bot.reply_to(message, "No data...")
    else:
        reply_message = "- Top flooder:\n"
        for i, item in enumerate(result):
            reply_message += f"[{i + 1}] {item[1].strip()} ({item[0]}) : {item[2]} messages.\n"
        bot.reply_to(message, reply_message)

    update_messages_count(message.from_user.id)


@bot.message_handler(func=lambda message: True, content_types=["text"])
def message_from_user(message):
    user_id = message.from_user.id
    update_messages_count(user_id)


@server.route(f"/{BOT_TOKEN}", methods=["POST"])
def redirect_message():
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

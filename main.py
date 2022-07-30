import os
import telebot
import logging
import psycopg2
from telebot import types
from config import *
from flask import Flask, request
from PIL import Image


x = 0
y = 0

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
    time = types.KeyboardButton("Распорядок дня")
    schedule = types.KeyboardButton("Расписание")
    events = types.KeyboardButton("Сегодняшние мероприятия")
    clubs = types.KeyboardButton("Школьные клубы и кружки")
    menu = types.KeyboardButton("Сегодняшнее меню")
    grades = types.KeyboardButton("Калькулятор оценок")
    sush = types.KeyboardButton("СУШ")
    instagram = types.KeyboardButton("Instagram аккаунт школы")
    markup.add(time, schedule, events, menu, clubs, grades, sush, instagram)
    bot.send_message(message.chat.id, "Подробную информация можно найти, нажав на кнопки меню", reply_markup=markup)

    db_object.execute(f"SELECT id FROM users WHERE id = {user_id}")
    result = db_object.fetchone()

    if not result:
        db_object.execute("INSERT INTO users(id, username, messages) VALUES (%s, %s, %s)", (user_id, username, 0))
        db_connection.commit()

    update_messages_count(user_id)


@bot.message_handler(content_types=['text'])
def get_text_from_user(message):
    if message.text == "Распорядок дня":
        image_path = 'https://drive.google.com/file/d/1RflTYE20booDE_vMMVSX5MaYlcrMYKDa/view?usp=sharing'
        img = Image.open(image_path)
        width, height = img.size
        print(width, height)
        img.show()
    elif message.text == "Расписание":
            markup_inline = types.InlineKeyboardMarkup(row_width=3)
            button_7 = types.InlineKeyboardButton(text='7', callback_data='7')
            button_8 = types.InlineKeyboardButton(text='8', callback_data='8')
            button_9 = types.InlineKeyboardButton(text='9', callback_data='9')
            button_10 = types.InlineKeyboardButton(text='10', callback_data='10')
            button_11 = types.InlineKeyboardButton(text='11', callback_data='11')
            button_12 = types.InlineKeyboardButton(text='12', callback_data='12')
            markup_inline.add(button_7, button_8, button_9, button_10, button_11, button_12)
            bot.send_message(message.chat.id, "Выберите класс:", reply_markup=markup_inline)
    elif message.text == "СУШ":
            markup_inline = types.InlineKeyboardMarkup(row_width=1)
            button_2 = types.InlineKeyboardButton(text='СУШ', url='https://sms.hbalm.nis.edu.kz/')
            markup_inline.add(button_2)
            bot.send_message(message.chat.id, "Нажми для перехода в СУШ", reply_markup=markup_inline)
    elif message.text == "Instagram аккаунт школы":
            markup_inline = types.InlineKeyboardMarkup(row_width=1)
            button_1 = types.InlineKeyboardButton(text="@nis_chembio_almaty",
                                                  url='https://instagram.com/nis_chembio_almaty?igshid=NmZiMzY2Mjc=')
            markup_inline.add(button_1)
            bot.send_message(message.chat.id, "Нажми для перехода в Инстаграм", reply_markup=markup_inline)
    elif message.text == "Сегодняшнее меню":
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, )
        markup = types.ReplyKeyboardMarkup()
        item_break = types.KeyboardButton('Завтрак')
        item_lunch = types.KeyboardButton('Обед')
        item_sup = types.KeyboardButton('Полдник')
        item_ext = types.KeyboardButton('Выход')
        markup.row(item_break)
        markup.row(item_lunch)
        markup.row(item_sup)
        markup.row(item_ext)
        bot.send_message(message.chat.id, "Меню:", reply_markup=markup)
    elif message.text == 'Завтрак':
        bot.reply_to(message, 'Рисовая каша')
    elif message.text == 'Обед':
        bot.reply_to(message, 'Куриный суп и плов')
    elif message.text == 'Полдник':
        bot.reply_to(message, 'Печенье')
    elif message.text == 'Выход':
        markup_close = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Спасибо за обращение", reply_markup=markup_close)
    elif message.text == 'Сегодняшние мероприятия':
        markup_inline = types.InlineKeyboardMarkup()
        item_yes = types.InlineKeyboardButton(text='Олимпиады', callback_data='olympiads')
        item_no = types.InlineKeyboardButton(text='Встречи', callback_data='meetings')
        item_address = types.InlineKeyboardButton(text='Другое', callback_data='other')
        markup_inline.add(item_yes, item_no)
        markup_inline.add(item_address)
        bot.send_message(message.chat.id, "Что вас интересует?", reply_markup=markup_inline)
    elif message.text == 'Школьные клубы и кружки':
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, )
        markup = types.ReplyKeyboardMarkup()
        item_reserve = types.KeyboardButton('Олимпиадный резерв')
        item_art = types.KeyboardButton('Искусство')
        item_project = types.KeyboardButton('Научные проекты')
        item_sport = types.KeyboardButton('Спорт')
        item_contact = types.KeyboardButton('Связаться с координатором')
        item_ext = types.KeyboardButton('Выход')
        markup.row(item_reserve)
        markup.row(item_art)
        markup.row(item_project)
        markup.row(item_sport)
        markup.row(item_contact)
        markup.row(item_ext)
        bot.send_message(message.chat.id, "Кружки и клубы:", reply_markup=markup)
    elif message.text == 'Олимпиадный резерв':
        pic = 'https://drive.google.com/file/d/1Q9s1F7h_PM3L2eaCIwd92OFt5buxeMmv/view?usp=sharing'
        bot.send_photo(message.chat.id, pic)
    elif message.text == 'Искусство':
        bot.reply_to(message, 'Отправляйте свои работы и запросы по этому адресу: aruzhanturash17@gmail.com')
    elif message.text == 'Научные проекты':
        markup_inline = types.InlineKeyboardMarkup(row_width=3)
        markup = types.ReplyKeyboardMarkup()
        item_sci = types.InlineKeyboardButton(text='Вступить',
                                             url='https://www.instagram.com/taza_su2022/?hl=ru')
        markup_inline.add(item_sci)
        bot.reply_to(message, 'Заходите на страничку', reply_markup=markup_inline )
    elif message.text == 'Спорт':
        markup_inline = types.InlineKeyboardMarkup(row_width=3)
        markup = types.ReplyKeyboardMarkup()
        item_tg = types.InlineKeyboardButton(text='Вступить',
                                              url='https://t.me/joinchat/Fyph8BgC5HYLtegB-X_B8g')
        markup_inline.add(item_tg)
        bot.reply_to(message,'Вступить в чат', reply_markup=markup_inline)
    elif message.text == 'Связаться с координатором':
        bot.reply_to(message, 'Позвоните по этому номеру: +7 701 715 79 69')
    elif message. text == 'Выход':
        markup_close = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Спасибо за обращение", reply_markup=markup_close)
    elif message.text == 'Калькулятор оценок':
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, )
        markup = types.ReplyKeyboardMarkup()
        item_table = types.KeyboardButton('Проследить прогресс')
        item_count = types.KeyboardButton('Посчитать оценку')
        markup.row(item_table)
        markup.row(item_count)
        bot.send_message(message.chat.id, "Калькулятор оценок", reply_markup=markup)
    elif message.text == 'Посчитать оценку':
        bot.send_message(message.chat.id, "Введите команду /calc")
    elif message.text == '/calc':
        bot.send_message(message.chat.id, "Введите процент по СОР:")
        bot.register_next_step_handler(message, reg_x)
    elif message.text == '5':
        if x < 35:
            bot.send_message(message.chat.id, "Упс! Похоже стоит выбрать другую оценку")
        else:
            a = 85-x
            b = (y*a)/50
            question = ' Вам нужно набрать как минимум ' + str(b)
            bot.send_message(message.chat.id, text=question)
    elif message.text == '4':
        if x < 15:
            bot.send_message(message.chat.id, "Упс! Похоже стоит выбрать другую оценку")
        else:
            q = 65-x
            w = (y*q)/50
            wet = ' Вам нужно набрать как минимум ' + str(w)
            bot.send_message(message.chat.id, text=wet)
    elif message.text == '3':
        e = 51-x
        r = (y*e)/50
        wer = ' Вам нужно набрать как минимум ' + str(r)
        bot.send_message(message.chat.id, text=wer)
    elif message.text == 'Проследить прогресс':
        bot.send_message(message.chat.id, "Введите команду /draw")





def reg_x(message):
    global x
    x = ''
    try:
        x = float(message.text)
    except Exception:
        bot.send_message(message.chat.id, "Проверьте корректность введенных данных")
    if x == 0:
        bot.register_next_step_handler(message, reg_x)
    elif x > 50:
        bot.send_message(message.chat.id, "Проверьте корректность введенных данных и нажмите на /calc")
    else:
        bot.send_message(message.chat.id, "Сколько баллов в СОЧ?")
        bot.register_next_step_handler(message, reg_y)


def reg_y(message):
    global y
    y = ''
    try:
        y = float(message.text)
    except Exception:
        bot.send_message(message.chat.id, "Проверьте корректность введенных данных")
    if y == 0:
        bot.register_next_step_handler(message, reg_y)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        item_5 = types.KeyboardButton("5")
        item_4 = types.KeyboardButton('4')
        item_3 = types.KeyboardButton('3')
        markup.add(item_5, item_4, item_3)
        bot.send_message(message.chat.id, text='Выберите нужную оценку', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == '7':
        markup_inline = types.InlineKeyboardMarkup(row_width=3)
        button_7a = types.InlineKeyboardButton(text= 'A', callback_data= '7A')
        button_7b = types.InlineKeyboardButton(text= 'B', callback_data= '7B')
        button_7c = types.InlineKeyboardButton(text= 'C', callback_data= '7C')
        button_7d = types.InlineKeyboardButton(text= 'D', callback_data= '7D')
        button_7e = types.InlineKeyboardButton(text= 'E', callback_data= '7E')
        button_7k = types.InlineKeyboardButton(text= 'K', callback_data= '7K')
        button_7l = types.InlineKeyboardButton(text= 'L', callback_data= '7L')
        button_7m = types.InlineKeyboardButton(text= 'M', callback_data= '7M')
        markup_inline.add(button_7a, button_7b, button_7c, button_7d, button_7e, button_7k, button_7l, button_7m)
        bot.send_message(call.message.chat.id, "Выберите литер:", reply_markup=markup_inline)
    elif call.data == '7A':
        markup_inline = types.InlineKeyboardMarkup(row_width=3)
        markup = types.ReplyKeyboardMarkup()
        item_7a = types.InlineKeyboardButton(text='Расписание', url= 'https://drive.google.com/file/d/1JpGVTpNKch40xgejd7bVFF7o5FR9R9Gw/view?usp=sharing')
        markup_inline.add(item_7a)
        bot.send_message(call.message.chat.id, "7А", reply_markup=markup_inline)
    elif call.data == '7B':
     markup_inline = types.InlineKeyboardMarkup(row_width=3)
     markup = types.ReplyKeyboardMarkup()
     item_7b = types.InlineKeyboardButton(text='Расписание', url= 'https://drive.google.com/file/d/1N9GADrAh2mlHRDRq8QOSd9vfhFmOVqRO/view?usp=sharing')
     markup_inline.add(item_7b)
     bot.send_message(call.message.chat.id, "7B", reply_markup=markup_inline)
    elif call.data== '7C':
     markup_inline = types.InlineKeyboardMarkup(row_width=3)
     markup = types.ReplyKeyboardMarkup()
     item_7c = types.InlineKeyboardButton(text='Расписание', url= 'https://drive.google.com/file/d/1RMJw3A128MoB1nWs5DpmECAX9Sa8k2YJ/view?usp=sharing')
     markup_inline.add(item_7c)
     bot.send_message(call.message.chat.id, "7C", reply_markup=markup_inline)
    elif call.data== '7D':
     markup_inline = types.InlineKeyboardMarkup(row_width=3)
     markup = types.ReplyKeyboardMarkup()
     item_7d = types.InlineKeyboardButton(text='Расписание', url= 'https://drive.google.com/file/d/1u6nWV1ZwbLNl-czeOrQH-2jWqCUsmlmN/view?usp=sharing')
     markup_inline.add(item_7d)
     bot.send_message(call.message.chat.id, "7D", reply_markup=markup_inline)
    elif call.data== '7E':
     markup_inline = types.InlineKeyboardMarkup(row_width=3)
     markup = types.ReplyKeyboardMarkup()
     item_7e = types.InlineKeyboardButton(text='Расписание', url= 'https://drive.google.com/file/d/1FlwOcsPO8OSdqVcXgTgOdhD-UYGjeMHH/view?usp=sharing')
     markup_inline.add(item_7e)
     bot.send_message(call.message.chat.id, "7E", reply_markup=markup_inline)
    elif call.data== '7K':
     markup_inline = types.InlineKeyboardMarkup(row_width=3)
     markup = types.ReplyKeyboardMarkup()
     item_7k = types.InlineKeyboardButton(text='Расписание', url= 'https://drive.google.com/file/d/11hJIgmD3ts7J_GKOm6SqqT6VecOtRaBR/view?usp=sharing')
     markup_inline.add(item_7k)
     bot.send_message(call.message.chat.id, "7K", reply_markup=markup_inline)
    elif call.data== '7L':
     markup_inline = types.InlineKeyboardMarkup(row_width=3)
     markup = types.ReplyKeyboardMarkup()
     item_7l = types.InlineKeyboardButton(text='Расписание', url= 'https://drive.google.com/file/d/1tI-FRMnCpdPUFWQ4X0XG46kV3b3H60DL/view?usp=sharing')
     markup_inline.add(item_7l)
     bot.send_message(call.message.chat.id, "7L", reply_markup=markup_inline)
    elif call.data == '7M':
     markup_inline = types.InlineKeyboardMarkup(row_width=3)
     markup = types.ReplyKeyboardMarkup()
     item_7m = types.InlineKeyboardButton(text='Расписание', url= 'https://drive.google.com/file/d/1fUHEs_64iLrIZCEOUHoX7z5pQ4IqAjQb/view?usp=sharing')
     markup_inline.add(item_7m)
     bot.send_message(call.message.chat.id, "7M", reply_markup=markup_inline)
    elif call.data =='olympiads':
       bot.answer_callback_query(call.id, text='На сегодня ничего не запланировано', show_alert=True)
    elif call.data == 'meetings':
     markup_inline = types.InlineKeyboardMarkup(row_width=3)
     markup = types.ReplyKeyboardMarkup()
     item_other = types.InlineKeyboardButton(text="Встречи", url='https://drive.google.com/file/d/1PXIoPomzrfK_jxNr8h9jalYnXKuut3-f/view?usp=sharing')
     markup_inline.add(item_other)
     bot.send_message(call.message.chat.id, "Посмотреть встречи на сегодня", reply_markup=markup_inline)
    elif call.data == 'other':
        bot.answer_callback_query(call.id, text='Сегодня в 17:00 в фойе школы пройдет мастер-класс по рисованию.', show_alert=True)


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

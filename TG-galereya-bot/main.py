import telebot
from telebot import types
from gtts import gTTS
import os
from lists import send_love, love_sticker, stopwords, hello
import parser_func
import gTTs_func 
import time

token = '1779126202:AAHHjvd1x7wC1pWuDHxGbOW-MQJs9GKus7o'
bot = telebot.TeleBot('1779126202:AAHHjvd1x7wC1pWuDHxGbOW-MQJs9GKus7o')

name_author = '' # переменная, принимает на себя имя из сообщения юзера
name_art = ''    # переменная, принимает на себя название картины из сообщения юзера

message_from_user_id = ''  # переменная, id чата
message_chat_id = ''       # переменная, id чата

found_inf = ''             # переменная, принимает на себя описание картины

stop_func = 0              # переменная, нужна для функции stop()

##############################################################################


# ответ бота на команды /start /help
@bot.message_handler(commands=['start', 'help']) 
def send_welcome(message):
	bot.reply_to(message, 
    "Привет! Вот список команд, которые я понимаю:\n"
    "/search  -  ищу описание картины.\nТебе нужно знать имя, фамилию автора и название картины.\n"
    '/website  -  высылаю тебе сайт Третьяковской галереи. Там много всего интересного!\n'
    '/help  -  открываю список команд и доп.инфу обо мне\n\n'
    "Поиск чувствителен к регистру!"
    "Если во время ввода данных ты ошибся, просто напиши 'стоп' и мы начнем заново."
    )

# ответ бота на команду /search
@bot.message_handler(commands=['search'])
def search_cmd(message):
    bot.reply_to(message, "Напиши имя и фамилию автора в род.падеже.\nПоиск чувствителен к регистру!")
    bot.register_next_step_handler(message, get_name_author)

# ответ бота на команду /website
@bot.message_handler(commands=['website'])
def website_cmd(message):
    website = 'https://www.tretyakovgallery.ru/'
    bot.reply_to(message, f"Третьяковская галеря: {website} ")

# ответ бота на все получаемые сообщения
@bot.message_handler(content_types=['text', 'sticker'])
def send_messages(message):
    if message.sticker:
        sticker_id = message.sticker.file_id                    # принимаем стикер и запоминаем его id
        bot.send_sticker(message.from_user.id, f'{sticker_id}') # отвечаем этим же стикером
    elif any([x in message.text.lower() for x in hello]):      # проверяем слова приветствия
        iskat_kartini(message)                                  # вызываем функцию с кнопками с предложеним начать поиск картины
    elif any([x in message.text.lower() for x in send_love]):   # проверяем слова на похвалу и признания в любви
        bot.send_sticker(message.from_user.id, love_sticker)    # отвечаем стикером с сердечком
    elif any([x in message.text.lower() for x in stopwords]):   # проверяем слова на мат и плохие слова
        bot.reply_to(message, "Как некультурно...")             # отвечаем
    elif message.text.lower() == "поиск":                       # если входящее сообщение = "поиск"
        bot.send_message(message.from_user.id, "Напиши имя и фамилию автора в род.падеже.\nПоиск чувствителен к регистру!") # начинаем цикл поиска картины
        bot.register_next_step_handler(message, get_name_author)                             # запоминаем сообщение и вызываем следующую функцию get_name_author()
    elif message.text.lower() == "стоп":                        # если входящее сообщение = "стоп"
        stop(message)                                           # вызываем функци stop(), останавливаем поиск картины
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.") # если входящее сообщение не прошло предыдущие фильтры

# функция для остановки работы цикла по поиску описания картины (действительна на всех функциях получения инфы)
@bot.message_handler(content_types=['text'])
def stop(message):
    global stop_func
    if message.text.lower() == "стоп":
        bot.send_message(message.from_user.id, "Остановилась.")
        stop_func = 1
        return stop_func
    else:
        pass

# функция, в которой мы запоминаем имя и фамилию автора, узнаем название картины
@bot.message_handler(content_types=['text'])
def get_name_author(message): #получаем фамилию имя автора
    global name_author
    global stop_func
    stop_here = 0         
    stop_func = 0
    stop(message)
    while stop_func == 0 and stop_here == 0:
        name_author = message.text #сохраняем имя и фамилию автора
        bot.send_message(message.from_user.id, 'Как называется картина?\nПоиск чувствителен к регистру!')
        bot.register_next_step_handler(message, get_name_art) # запоминаем сообщение и вызываем следующую функцию get_name_art()
        stop_here = 1
    else:
        pass

# функция, в которой мы запоминаем название картины, записываем данные name_author и name_art в два файла: text_author и text_art соотв.
@bot.message_handler(content_types=['text'])
def get_name_art(message): 
    global name_art
    global message_from_user_id
    global message_chat_id
    name_art = message.text #сохраняем название картины
    with open(f"D:\\Python\\TG-galereya-bot\\text\\text_author.txt", "w") as text_author: # создаем док.txt
        text_author.write(f'{name_author}')                                               # сохраняем имя автора в док.txt
        text_author.close()                                                               # закрываем док.txt
    with open(f"D:\\Python\\TG-galereya-bot\\text\\text_art.txt", "w") as text_art:       # создаем док.txt
        text_art.write(f'{name_art}')                                                     # сохраняем название картины в док.txt
        text_art.close()                                                                  # закрываем док.txt
    message_from_user_id = message.from_user.id                        # переопределяем переменные id чата
    message_chat_id = message.chat.id                                  # переопределяем переменные id чата
    msg_info(message)                                                  # вызываем функцию msg_info, которая начнет процесс парсинга

# функция, которая останавливает поисковые процессы, и отправку описания, если будет вызванна
@bot.message_handler(content_types=['text'])
def no_info():
    global stop_func
    global message_from_user_id
    if parser_func.no_info == 1:
        stop_func = 1
        bot.send_message(message_from_user_id, "Я не нашла такой картины. Пиши 'поиск', если хочешь попробовать снова.")
        return stop_func
    else:
        pass
# функция с кнопками, вызывается, когда user здоровается с ботом
@bot.message_handler(content_types=['text'])
def iskat_kartini(message):
    keyboard = types.InlineKeyboardMarkup()
    btn_yes = types.InlineKeyboardButton(text="Да", callback_data="yes")
    btn_no = types.InlineKeyboardButton(text="Нет", callback_data="no")
    keyboard.add(btn_yes, btn_no)
    bot.send_message(message.chat.id, 'Привет, пошли искать картины?', reply_markup=keyboard)

# функция с кнопками, вызывается, когда бот находит нужную информацию. Дает user'у выбор: прочитать, прослушать, и то и другое
@bot.message_handler(content_types=['text'])
def type_info(message):
    keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Прочитать", callback_data="read")
    btn2 = types.InlineKeyboardButton(text="Прослушать", callback_data="listen")
    btn3 = types.InlineKeyboardButton(text="Всё вместе", callback_data="both")
    keyboard.add(btn1, btn2)
    keyboard.add(btn3)
    bot.send_message(message.chat.id, 'Ты хочешь прочитать текст или прослушать?', reply_markup=keyboard)

# функция, которая выполняется при нажатии кнопок, написанных ранее    
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "read":
            send_img()
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Вот, что я нашла: {found_inf}')
        elif call.data == "listen":
            send_img()
            speech()
        elif call.data == "both":
            send_img()
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Вот, что я нашла: {found_inf}')
            speech()
        elif call.data == "yes":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Отлично! Тогда напиши 'поиск', и мы начнем!")
        elif call.data == "no":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Как скажешь.')
    else:
        pass

# основная функция по поиску инфы. Вызывает парсер.
@bot.message_handler(content_types=['text'])
def msg_info(message):
    global found_inf
    global stop_func
    stop_here = 0
    stop_func = 0
    stop(message)
    while stop_func == 0 and stop_here == 0:
        bot.send_message(message.from_user.id, 'Собираю информацию. Подожди немного')
        found_inf = parser_func.get_info()
        if parser_func.no_info == 1:
            no_info()
        else:
            type_info(message)
            stop_here = 1
    else:
        pass
# функция, которая отправляет user'у картину
@bot.message_handler(content_types=['photo'])
def send_img():
    with open(f"D:\\Python\\TG-galereya-bot\\images\\img.jpg", "rb") as imag:
        bot.send_photo(message_chat_id, imag)
        imag.close()
        if os.path.isfile(f'D:\\Python\\TG-galereya-bot\\images\\img.jpg'): 
            os.remove(f'D:\\Python\\TG-galereya-bot\\images\\img.jpg') 
            print("remove success") 
        else: 
            print("File doesn't exists!")

# функция, которая скидывает пользователю голосовое сообщение, где зачитывается описание картины. Вызывает функцию gtts
@bot.message_handler(content_types=['voice'])
def speech():
    bot.send_message(message_from_user_id, 'Записываю тебе голосовуху. Подожди немного')
    gTTs_func.make_speech()
    audio = open(f'D:\\Python\\TG-galereya-bot\\voice\\voice.ogg', 'rb')
    bot.send_audio(message_chat_id, audio)
    audio.close()
    if os.path.isfile(f'D:\\Python\\TG-galereya-bot\\voice\\voice.ogg'): 
        os.remove(f'D:\\Python\\TG-galereya-bot\\voice\\voice.ogg') 
        print("remove success") 
    else: 
        print("File doesn't exists!")

####################################################################
bot.polling(none_stop=True, interval=0)


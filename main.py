# --*-- coding=utf-8 --*--
# Імпорт бібліотек
import telebot
import pytesseract
pytesseract.pytesseract.tesseract_cmd = './Tesseract-OCR'
try:
    from PIL import Image
except ImportError:
    import Image

# Імпорт модулів функціонування розпізнавання
# та функціонального аналізу

from pre_image import get_image
from recognize import  get_text
from finder import  search, get_tel_rieltors, sort_list
from xls_writer import writer, text_writer

# Константи
rieltors = 'filtr.xls'
result =[]
start = 0
count_rooms = 0
lang = 'ukr'
todo = 0
is_xls = 0

if __name__ == '__main__':

    bot = telebot.TeleBot('1028387271:AAEhPKKCfQBNeadeMS1k1jMUZpusniiprv4')

    # Декоратори - обробники вхідних команд, тексту чи зображень
    @bot.message_handler(commands=['start'])
    def start_message(message):
        global count_rooms
        global todo
        global is_xls
        global start
        start = 1
        count_rooms = 0
        todo = 0
        is_xls = 0
        user_markup = None

        # Використання кнопок для керування ботом
        user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
        user_markup.row('Англійська мова')
        user_markup.row('Українська мова')
        bot.send_message(message.chat.id, 'Доброго дня ' + message.from_user.first_name + ', виберіть мову розпізнавання:', reply_markup=user_markup)

    # Декоратори - обробники команди 'about'
    @bot.message_handler(commands=['about'])
    def about_message(message):
        bot.send_message(message.chat.id, "Представлений проект - реалізація системи оптичного розпізнавання символів та функціональне опрацювання фільтрації тексту за ключовими словами на прикладі обробки оголошень про нерухомість журналу 'Від і До'")


    # Функція - обробник режиму керування ботом
    # @bot.message_handler(commands=['tdo'])
    def todo_message(message):
        user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
        user_markup.row('Розпізнавання звичайного тексту')
        user_markup.row("Функціональне OCR для журналу 'Від і До'")
        bot.send_message(message.chat.id, "Виберіть сценарій розпізнавання:", reply_markup=user_markup)


    # Функція - обробник повернення результату
    # @bot.message_handler(commands=['xls'])
    def xls_message(message):
        user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
        user_markup.row('Зберегти в форматі xls')
        user_markup.row('Повернути в діалог')
        bot.send_message(message.chat.id, "Виберіть спосіб повернення опрацьованих даних:", reply_markup=user_markup)


    # Функція - обробник фільтра по оголошеннях
    # @bot.message_handler(commands=['croom'])
    def croom_message(message):
        user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
        user_markup.row('1-кімнатні')
        user_markup.row('2-кімнатні')
        user_markup.row('Повернутись на початок /start')
        bot.send_message(message.chat.id, "Виберіть параметр для фільтрування оголошень ", reply_markup=user_markup)


    # Функція - обробник повернення на початок діалогу з ботом
    # @bot.message_handler(commands=['start'])
    def return_message(message):
        user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
        user_markup.row('Повернутись на початок /start')
        bot.send_message(message.chat.id, "Надішліть зображення для розпізнавання або поверніться на початок", reply_markup=user_markup)


    # Загальний декоратор обробки вхідного тексту
    @bot.message_handler(content_types=['text'])
    def handle_text(message):
        global start
        global lang
        global count_rooms
        global todo
        global is_xls

        if message.text == "Англійська мова":
            lang = 'eng'
        elif message.text == "Українська мова":
            lang = 'ukr'
        if message.text == "Розпізнавання звичайного тексту":
            todo = 1
            #bot.send_message(message.chat.id, 'Надішліть зображення для розпізнавання.')
        elif message.text == "Функціональне OCR для журналу 'Від і До'":
            todo = 2
            #bot.send_message(message.chat.id, 'Надішліть зображення для розпізнавання.')
        if message.text == "Зберегти в форматі xls":
            is_xls = 1
            bot.send_message(message.chat.id, 'Інформацію буде збережено в файл')
        elif message.text == 'Повернути в діалог':
            is_xls = 2
            bot.send_message(message.chat.id, 'Інформацію буде повернено в діалог')
        if message.text == '1-кімнатні':
            count_rooms = 1
            bot.send_message(message.chat.id, 'Надішліть зображення для розпізнавання.')
        elif message.text == '2-кімнатні':
            count_rooms = 2
            bot.send_message(message.chat.id, 'Надішліть зображення для розпізнавання.')
        elif message.text == 'Повернутись на початок /start':
            count_rooms = 0
            todo = 0
            is_xls = 0
            lang = 'ukr'
            start = 0
            #bot.send_message(message.chat.id, '/start')

        # Перевірки констан натиснутих кнопок для вибору вітки функціонування бота
        if not start:
            start_message(message)
        elif not todo:
            todo_message(message)
        elif todo == 1:
            return_message(message)
        elif not is_xls and todo == 2:
            xls_message(message)
        elif not count_rooms and todo == 2:
            croom_message(message)

    # Функція повернення результату в форматі xls
    def send_xls_file(message, file_name):
        file = open(file_name, 'rb')
        bot.send_document(message.chat.id, file)


    # Декоратор обробки вхідного зображення
    @bot.message_handler(content_types=['photo'])
    def handle_docs_photo(message):
        global todo
        global lang
        global is_xls
        global count_rooms

        # Функціонування бота шляхом спеціалізованого розпізнавання журналу "Від і До"
        if todo == 2:
            try:
                fileID = message.photo[-1].file_id
                file_info = bot.get_file(fileID)
                downloaded_file = bot.download_file(file_info.file_path)

                with open("image.jpg", 'wb') as new_file:
                    new_file.write(downloaded_file)
                bot.reply_to(message, "Опрацьовую отримане зображення. Тривалість обробки залежить від кількості символів на зображенні.")
                result = []
                image = get_image("image.jpg")
                ad = get_text(image, lang)
                # print(ad)
                rielt_list = get_tel_rieltors(rieltors)
                #print(rielt_list)
                ad_sorted = sort_list(ad)
                print(ad_sorted)

                for item in ad_sorted[count_rooms - 1]:
                    if search(item):
                        for record in search(item):
                            if record not in rielt_list:
                                result.append([record, item])
                print(result)

                if result != []:
                    bot.send_message(message.chat.id, "Відфільтровані оголошення:")
                    if is_xls == 1:
                        file_name = writer(result, count_rooms)
                        send_xls_file(message, file_name)
                    elif is_xls == 2:
                        for item in result:
                            bot.send_message(message.chat.id, item[1])
                else:
                        bot.send_message(message.chat.id,  message.from_user.first_name + ' , на жаль, співпадінь по фільтру не знайдено.')

            except Exception as e:
                bot.reply_to(message, e)

        # Функціонування бота шляхом звичайного розпізнавання тексту із зображень
        elif todo == 1:
            try:

                fileID = message.photo[-1].file_id
                file_info = bot.get_file(fileID)
                downloaded_file = bot.download_file(file_info.file_path)

                with open("image.png", 'wb') as new_file:
                    new_file.write(downloaded_file)
                bot.reply_to(message, "Опрацьовую отримане зображення. Тривалість обробки залежить від кількості символів на зображенні.")
                text = ''
                #image = get_image("image.png")
                text = pytesseract.image_to_string('image.png', lang)
                bot.send_message(message.chat.id, text)

            except Exception as e:
                bot.reply_to(message, e)


    bot.polling(none_stop=True, interval=0)

import telebot
from telebot import types
import config
import values
import sqlite3

# Registration BOT using TOKEN
bot = telebot.TeleBot(config.TOKEN)

# Registration DB
db = sqlite3.connect('DB/catalog.db', check_same_thread=False)
sql = db.cursor()


# For reading USER's HEIGHT
def height(message, word):
    weight = message.text
    msg = bot.send_message(message.chat.id, 'Введи свой рост (в сантиметрах):\n')
    bot.register_next_step_handler(msg, calc, (weight, word))


# For reading AGE or printing INDEX of body mass
def calc(message, lis):
    h = int(message.text) / 100
    w = int(lis[0])
    if lis[1] == 'Калории':
        msg = bot.send_message(message.chat.id, f'Введи свой возраст:\n')
        bot.register_next_step_handler(msg, age, (h * 100, w))
    elif lis[1] == 'Индекс':
        bot.send_photo(message.chat.id, photo=open('vals.png', 'rb'),
                       caption=f'Ваш индекс массы тела:\n{round(w / (h ** 2), 2)}',
                       parse_mode='html')


# For printing necessary number of calories and reading about type of activity
def age(message, data):
    w = data[1] * 9.99
    h = data[0] * 6.25
    a = int(message.text) * 4.92
    pre_result = round(w + h - a)
    bot.send_message(message.chat.id, f'<em><b>{pre_result}</b></em> — '
                                      f'Столько калорий необходимо вам для того, '
                                      f'чтобы просто существовать.',
                     parse_mode='html')
    msg = bot.send_message(message.chat.id, values.description, parse_mode='html')
    bot.register_next_step_handler(msg, activity, pre_result)


# printing necessary number of calories
def activity(message, res):
    result = round(res * values.values[message.text])
    bot.send_message(message.chat.id, f'Для похудения необходимо <b>{result - 400} -- {result - 200}</b> калорий\n'
                                      f'Необходимо потреблять <b>{result}</b>'
                                      f' калорий в день чтобы нормально восстанавливаться\n'
                                      f'Для набора массы необходимо <b>{result + 200} -- {result + 400}</b> калорий\n',
                     parse_mode='html')


# Read data from DB (item shop) using user_id
def read_from_items_db(user_id):
    data = [el for el in sql.execute(f"SELECT * FROM items WHERE rowid = {values.user_list[str(user_id)][0]}")]
    # print(data)
    return data


# Creating keyboard for card (below)
def create_markup_for_card():
    keyboard = types.InlineKeyboardMarkup()
    key_1 = types.InlineKeyboardButton(text='⬅ Предыдущий товар', callback_data='previous')
    key_2 = types.InlineKeyboardButton(text='Следующий товар ➡', callback_data='next')
    key_3 = types.InlineKeyboardButton(text='🗑 Добавить в корзину', callback_data='add_in_basket')
    keyboard.row(key_1, key_2)
    keyboard.add(key_3)
    return keyboard


# Send message with data about item (card of item)
def send_item(message):
    data = read_from_items_db(message.from_user.id)[0]
    markup = create_markup_for_card()
    if data[4] - data[3] != 0:
        cost = f'{round(data[3])} - {round(data[4])}'
    else:
        cost = round(data[3])
    try:
        msg_id = message.chat.id
    except:
        msg_id = message.message.chat.id
    bot.send_photo(msg_id,
                   open(data[5], 'rb'),
                   caption=f'\n<b>{data[2]}</b>\n\n'
                           f'Цена: <b>{cost} RUB</b>\n\n'
                           f'<em>Описание: {data[6].capitalize()}</em>\n'
                           f'\nВес: {round(data[-1] * 1000)} g.',
                   parse_mode='html',
                   reply_markup=markup)


# Is User in values.user_list
def test_of_being_in_list(msg_data):
    if not (str(msg_data.from_user.id) in values.user_list):
        values.iter_var_changer(msg_data.from_user.id, 1, True)


# How many notes in DB
def count_of_strings():
    sql.execute("SELECT rowid FROM items")
    return len(sql.fetchall())


# Getting data from DB about item in USER's basket
def get_data_from_basket(message):
    user_basket = values.user_list[str(message.from_user.id)][1]
    message_text = '\n'
    for el, count in user_basket.items():
        data = sql.execute(f"SELECT name FROM items WHERE rowid = {int(el)}").fetchone()[0]
        message_text += f'\n• {data} = <b>{count} шт.</b>\n'
    return message_text


def create_markup_for_basket(message):
    try:
        msg_id = message.id
    except:
        msg_id = message.message.id
    keyboard = types.InlineKeyboardMarkup()
    key_1 = types.InlineKeyboardButton(text='❌ Очистить корзину ❌', callback_data=f'clear_basket_{msg_id}')
    key_2 = types.InlineKeyboardButton(text='📋 Оформить заказ ', callback_data='create_order')
    keyboard.row(key_1)
    keyboard.row(key_2)
    return keyboard


def response_for_check_basket(message):
    try:
        msg_id = message.id
        chat_id = message.chat.id
    except:
        msg_id = message.message.id
        chat_id = message.message.chat.id
    text = get_data_from_basket(message)
    if text == '\n':
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='OK', callback_data=f'ok_{msg_id}'))
        text = 'Корзина пуста!'
    else:
        keyboard = create_markup_for_basket(message)
    bot.send_message(chat_id=chat_id,
                     text=f'{text}',
                     parse_mode='html',
                     reply_markup=keyboard)


"""
        ###########################################################
        ------ Starting of actions with different 'handlers' ------
        ###########################################################
"""


@bot.message_handler(commands=['calc'])
def characteristics(message):
    mark = types.ReplyKeyboardMarkup(resize_keyboard=True)
    mark.row(
        'Индекс',
        'Калории',
    )
    bot.send_message(message.chat.id, 'Что вы хотите узнать?', reply_markup=mark)


@bot.message_handler(commands=['hello', 'hi', 'sup'])
def greeting(message):
    msg = bot.send_photo(message.chat.id, open('photos/Rock.jpg', 'rb'))
    keyboard = types.InlineKeyboardMarkup()
    key_1 = types.InlineKeyboardButton(text='Привет', callback_data=f'hi_{msg.id}')
    key_2 = types.InlineKeyboardButton(text='Пока', callback_data=f'bye_{msg.id}')
    keyboard.row(key_1, key_2)
    msg = bot.send_message(message.chat.id,
                           f'Перед тобой бот для подсчета калорий'
                           f' <b>{bot.get_me().first_name}</b>',
                           parse_mode='html',
                           reply_markup=keyboard)


@bot.message_handler(commands=['market', 'shop', 'store'])
def market(message):
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu.row(
        'Каталог',
        'Корзина'
    )
    # menu.add('')
    bot.send_message(message.chat.id, 'Добро пожаловать в магазин!\nИспользуйте меню для навигации: ',
                     reply_markup=menu)
    test_of_being_in_list(message)


@bot.message_handler(content_types=['text'])
def handler(message):
    if message.text == 'Индекс' or message.text == 'Калории':
        word = message.text
        msg = bot.send_message(message.chat.id, 'Введи свой вес:\n')
        bot.register_next_step_handler(msg, height, word)
    elif message.text == 'Каталог':
        test_of_being_in_list(message)
        send_item(message)
    elif message.text == 'Корзина':
        response_for_check_basket(message)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    test_of_being_in_list(call)
    data = call.data.split('_')
    if data[0] == 'hi' or data[0] == 'bye':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=f'{values.for_greet[data[0]]} {call.from_user.first_name}!')
        bot.delete_message(call.message.chat.id, data[1])
    if call.data == 'next':
        index = values.user_list[str(call.from_user.id)]
        if index[0] < count_of_strings():
            values.iter_var_changer(call.from_user.id, index[0] + 1)
        else:
            values.iter_var_changer(call.from_user.id, 1)
        send_item(call)
    elif call.data == 'previous':
        index = values.user_list[str(call.from_user.id)]
        if index[0] > 1:
            values.iter_var_changer(call.from_user.id, index[0] - 1)
        else:
            values.iter_var_changer(call.from_user.id, count_of_strings())
        send_item(call)
    elif call.data == 'add_in_basket':
        index = values.user_list[str(call.from_user.id)]
        try:
            count = values.user_list[str(call.from_user.id)][1][str(index[0])]
            values.add_item(call.from_user.id, index[0], count + 1)
        except Exception as ex:
            # print(f'Firstly!{"#" * 10}Exception: {ex}')
            values.add_item(call.from_user.id, index[0], 1)
        bot.answer_callback_query(callback_query_id=call.id, text='\nТовар добавлен в корзину!\n')
    # for user, data in values.user_list.items():
    #     print(f'  |||{user} --- {data}|||')

    elif data[0] == 'ok':
        # bot.edit_message_text(chat_id=call.message.chat.id, text='Продолжайте покупки!', message_id=call.message.id)
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
            bot.delete_message(chat_id=call.message.chat.id, message_id=data[1])
        except Exception as ex:
            print(ex)

    elif data[0] + '_' + data[1] == 'clear_basket':
        values.clear_basket(call.from_user.id)
        try:
            bot.delete_message(call.message.chat.id, data[2])
            bot.delete_message(call.message.chat.id, call.message.id)
        except Exception as ex:
            print(ex)

    bot.answer_callback_query(call.id)


bot.polling(none_stop=True)

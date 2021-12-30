description = "Ваша дневная активность:\n\n\n" \
              "Сидячий образ жизни == <b>0</b>\n\n" \
              "Малая активность == <b>1</b>\n\n" \
              "Активность ниже средней\n<em>(тренировка - 1 час в неделю)</em> == <b>2</b>\n\n" \
              "Средняя активность\n<em>(3 - 5 часа в неделю)</em> == <b>3</b>\n\n" \
              "Активность выше средней\n<em>(7 - 8 часа в неделю)</em> == <b>4</b>\n\n" \
              "Высокая активность\n<em>( > 8 часов в неделю)</em> == <b>5</b>\n"


values = {
    '0': 1.2,
    '1': 1.25,
    '2': 1.38,
    '3': 1.46,
    '4': 1.64,
    '5': 1.8
}

for_greet = {
    'hi': 'Привет',
    'bye': 'Пока'
}

user_list = {
    'user1234569420': [1, {'item42069': 3, 'item69420': 5}]
}


def iter_var_changer(user_id, index, first_time=False):
    if first_time:
        user_list[str(user_id)] = [index, {}]
    else:
        user_list[str(user_id)][0] = index


def add_item(user_id, index, count=1):
    user_list[str(user_id)][1][str(index)] = count


def clear_basket(user_id):
    user_list[str(user_id)][1] = dict()

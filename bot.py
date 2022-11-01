from config import token, user_id

from enum import Enum

import telebot as tb


bot = tb.TeleBot(token)

quests = list()
message_uid = 0

class State(Enum):
    ENTER_QUEST_NAME = '0'
    SMALL_TALK = '1'

current_state = State.SMALL_TALK


def hijab(face):
    def wrapper(message):
        global current_state
        if not isinstance(current_state, State):
            current_state = State.SMALL_TALK
        if message.from_user.id != user_id:
            bot.send_message(message.chat.id, 'Я не буду с тобой играть')
            return
        return face(message)

    return wrapper


@bot.message_handler(commands=['start'])
@hijab
def start_msg(message):
    button_1 = tb.types.KeyboardButton('Новый квест')
    button_2 = tb.types.KeyboardButton('Открыть ящик пандоры')
    keyboard = tb.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    keyboard.add(button_1)
    keyboard.add(button_2)
    bot.send_message(message.chat.id, 'Ну здравствуй, Кит', reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == 'Новый квест')
@hijab
def add_quest(message):
    global current_state
    current_state = State.ENTER_QUEST_NAME

    bot.send_message(message.chat.id, 'Расскажи что хочешь сделать')

@bot.message_handler(func=lambda _: current_state == State.ENTER_QUEST_NAME)
@hijab
def quest_name_process(message):
    global current_state, message_uid
    current_state = State.SMALL_TALK

    quest = message.text
    callback = tb.types.InlineKeyboardButton(text=quest, callback_data=str(message_uid))
    message_uid += 1
    quests.append(callback)

    bot.send_message(message.chat.id, 'Все добавлено')

@bot.message_handler(func=lambda message: message.text == 'Открыть ящик пандоры')
@hijab
def render_quests(message):
    keyboard = tb.types.InlineKeyboardMarkup()
    for quest in quests:
        keyboard.add(quest)
    bot.send_message(message.chat.id, 'Здесь когда-нибудь будут крутые цитаты))', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda x: True)
@hijab
def process_callback(call):
    finished = call.data
    new_keyboard = tb.types.InlineKeyboardMarkup()
    for quest in quests:
        if quest.callback_data == finished:
            quests.remove(quest)
            break
    for quest in quests:
        new_keyboard.add(quest)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=new_keyboard)
    if not quests:
        bot.send_message(call.message.chat.id, 'Мегахарош, ты завершил все квесты, нарекаешься жоским типом')

if __name__ == '__main__':
    bot.infinity_polling()
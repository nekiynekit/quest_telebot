from states.state import State
from utils.wrappers import hijab

import telebot as tb


#@bot.message_handler(commands=['start'])
@hijab
def start_msg(message, bot):
    button_1 = tb.types.KeyboardButton('Новый квест')
    button_2 = tb.types.KeyboardButton('Открыть ящик пандоры')
    keyboard = tb.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    keyboard.add(button_1)
    keyboard.add(button_2)
    bot.send_message(message.chat.id, 'Ну здравствуй, Кит', reply_markup=keyboard)

#@bot.message_handler(func=lambda message: message.text == 'Новый квест')
@hijab
def add_quest(message, bot):
    global current_state
    current_state = State.ENTER_QUEST_NAME

    bot.send_message(message.chat.id, 'Расскажи что хочешь сделать')

#@bot.message_handler(func=lambda _: current_state == State.ENTER_QUEST_NAME)
@hijab
def quest_name_process(message, bot):
    global current_state, message_uid
    current_state = State.SMALL_TALK

    quest = message.text
    callback = tb.types.InlineKeyboardButton(text=quest, callback_data=str(message_uid))
    message_uid += 1
    quests.append(callback)

    bot.send_message(message.chat.id, 'Все добавлено')

#@bot.message_handler(func=lambda message: message.text == 'Открыть ящик пандоры')
@hijab
def render_quests(message, bot):
    keyboard = tb.types.InlineKeyboardMarkup()
    for quest in quests:
        keyboard.add(quest)
    bot.send_message(message.chat.id, 'Здесь когда-нибудь будут крутые цитаты))', reply_markup=keyboard)
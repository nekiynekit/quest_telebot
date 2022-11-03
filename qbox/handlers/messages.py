from states.state import State
from utils.wrappers import hijab
from logic.qboxes import QuestBox

import telebot as tb

from telebot.types import InlineKeyboardButton as inline


class MessageHandler():

    def __init__(self, db_name: str):
        self.current_state = State.SMALL_TALK
        self.qbox = QuestBox(db_name)
        self.db_name = db_name

    @hijab
    def start_msg(self, message: tb.types.Message, bot: tb.TeleBot):
        add = inline('Добавить квест', callback_data='add')
        activate = inline('Активировать квест', callback_data='activate')
        shedule = inline('Назначить квест', callback_data='shedule')
        delete = inline('Удалить квест', callback_data='delete')
        return_quest = inline('Вернуть квест', callback_data='return')
        close = inline('Закрыть квест', callback_data='close')
        get_quest = inline('Текущие квесты', callback_data='get_quest')
        get_stats = inline('Текущая статистика', callback_data='get_stats')

        menu = tb.types.InlineKeyboardMarkup()
        for item in [add, activate, shedule, delete, return_quest, close,
                     get_stats, get_quest]:
            menu.add(item)
        bot.send_message(message.chat.id, 'Добро пожаловать',
                         reply_markup=menu)

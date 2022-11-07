import datetime
from ..states.state import State
from ..utils.wrappers import hijab
from ..logic.qboxes import QuestBox

import telebot as tb

from telebot.types import InlineKeyboardButton as inline


class MessageHandler():

    def __init__(self, state: State, qbox: QuestBox):
        self.qbox = qbox
        self.qbox.waiting_quest = None

    @hijab
    def start_cmd(self, message: tb.types.Message, bot: tb.TeleBot):
        add = inline('Добавить квест', callback_data='add')
        activate = inline('Активировать квест', callback_data='activate')
        shedule = inline('Назначить квест', callback_data='shedule')
        delete = inline('Удалить квест', callback_data='delete')
        return_quest = inline('Вернуть квест', callback_data='return')
        close = inline('Закрыть квест', callback_data='close')
        get_quest = inline('Текущие квесты', callback_data='get_quest')
        get_shedule = inline('Раписание', callback_data='sheduler')
        get_stats = inline('Текущая статистика', callback_data='get_stats')

        menu = tb.types.InlineKeyboardMarkup()
        for item in [add, activate, shedule, delete, return_quest, close,
                     get_stats, get_quest, get_shedule]:
            menu.add(item)
        bot.send_message(message.chat.id, 'Добро пожаловать',
                         reply_markup=menu)

    @hijab
    def cancel_cmd(self, message: tb.types.Message, bot: tb.TeleBot):
        self.qbox.current_state = State.SMALL_TALK
        bot.send_message(message.chat.id, 'Ок, отмена')

    @hijab
    def small_talk(self, message: tb.types.Message, bot: tb.TeleBot):
        bot.send_message(message.chat.id, 'Че еще расскажешь')

    def small_talk_filter(self, *args, **kwargs):
        return self.qbox.current_state == State.SMALL_TALK

    @hijab
    def add_quest(self, message: tb.types.Message, bot: tb.TeleBot):
        text = message.text
        self.qbox.add_quest(text)
        self.qbox.current_state = State.SMALL_TALK
        bot.send_message(message.chat.id, 'Квест добавлен в Бездну')

    def add_filter(self, *args, **kwargs):
        return self.qbox.current_state == State.ADD_NEW_QUEST

    @hijab
    def shedule_date_quest(self, message: tb.types.Message, bot: tb.TeleBot):
        dirty_date = message.text
        try:
            date = datetime.datetime.strptime(dirty_date, '%Y-%m-%d')
        except Exception:
            bot.send_message(message.chat.id,
                             'Формат даты должен быть YYYY-MM-DD')
            return
        self.qbox.current_state = State.SMALL_TALK
        try:
            self.qbox.shedule_quest(self.qbox.waiting_quest, date.date())
            bot.send_message(message.chat.id, 'Все в порядке')
        except Exception:
            bot.send_message(message.chat.id, 'Что-то пошло не так')
            self.qbox.current_state = State.SMALL_TALK

    def shedule_date_filter(self, *args, **kwargs):
        return self.qbox.current_state == State.SHEDULE_QUEST_DATE

    @hijab
    def shedule_text_quest(self, message: tb.types.Message, bot: tb.TeleBot):
        self.qbox.waiting_quest = message.text
        self.qbox.current_state = State.SHEDULE_QUEST_DATE
        bot.send_message(message.chat.id, 'Теперь назначь квесту дату')

    def shedule_text_filter(self, *args, **kwargs):
        return self.qbox.current_state == State.SHEDULE_QUEST_NAME

    @hijab
    def activate(self, message: tb.types.Message, bot: tb.TeleBot):
        quest = message.text
        self.qbox.current_state = State.SMALL_TALK
        try:
            self.qbox.activate_quest(quest)
            bot.send_message(message.chat.id, 'Все прошло хорошо')
        except Exception:
            bot.send_message(message.chat.id, 'Что-то пошло не так')

    def activate_filter(self, *args, **kwargs):
        return self.qbox.current_state == State.ACTIVATE_QUEST

    @hijab
    def delete(self, message: tb.types.Message, bot: tb.TeleBot):
        quest = message.text
        self.qbox.current_state = State.SMALL_TALK
        for table_name in ['pandora', 'serif_wall']:
            self.qbox.delete_quest(quest, table_name)
        bot.send_message(message.chat.id, 'Квест удален')

    def delete_filter(self, *args, **kwargs):
        return self.qbox.current_state == State.DELETE_QUEST

    @hijab
    def return_quest(self, message: tb.types.Message, bot: tb.TeleBot):
        quest = message.text
        self.qbox.current_state = State.SMALL_TALK
        for table_name in ['pandora', 'serif_wall']:
            self.qbox.return_quest(quest, table_name)
        bot.send_message(message.chat.id, 'Квест возвращен')

    def return_filter(self, *args, **kwargs):
        return self.qbox.current_state == State.RETURN_QUEST

    @hijab
    def close(self, message: tb.types.Message, bot: tb.TeleBot):
        quest = message.text
        self.qbox.current_state = State.SMALL_TALK
        try:
            self.qbox.close_pandora_quest(quest)
        except KeyError:
            pass
        self.qbox.close_serif_quest(quest)
        bot.send_message(message.chat.id, 'Квест закрыт')

    def close_filter(self, *args, **kwargs):
        return self.qbox.current_state == State.CLOSE_QUEST

from ..states.state import State
from ..logic.qboxes import QuestBox
from ..utils.wrappers import hijab

import telebot as tb


def tuple2str(data: tuple):
    if len(data) == 1:
        return data[0]
    print(data)
    string = f'#{data[1]}# --> {data[0]}'
    return string


class CallbackHandler():

    def __init__(self, state: State, qbox: QuestBox):
        self.qbox = qbox

    @hijab
    def add_quest(self, call: tb.types.CallbackQuery, bot: tb.TeleBot):
        self.qbox.current_state = State.ADD_NEW_QUEST
        bot.send_message(call.from_user.id, 'Опиши пожалуйста квест')

    def add_filter(self, call: tb.types.CallbackQuery):
        print(f'id состояния колбэка: {id(self.qbox.current_state)}')
        print(f'Стоит в состоянии {self.qbox.current_state}')
        return self.qbox.current_state == State.SMALL_TALK and\
            call.data == 'add'

    @hijab
    def activate(self, call: tb.types.CallbackQuery, bot: tb.TeleBot):
        self.qbox.current_state = State.ACTIVATE_QUEST
        menu = self.create_keyboard(self.qbox.get_table('void'))
        bot.send_message(call.from_user.id, 'Выбери квест', reply_markup=menu)

    def activate_filter(self, call: tb.types.CallbackQuery):
        return self.qbox.current_state == State.SMALL_TALK and \
            call.data == 'activate'

    @hijab
    def shedule(self, call: tb.types.CallbackQuery, bot: tb.TeleBot):
        self.qbox.current_state = State.SHEDULE_QUEST_NAME
        menu = self.create_keyboard(self.qbox.get_table('void'))
        bot.send_message(call.from_user.id, 'Выбери квест', reply_markup=menu)

    def shedule_filter(self, call: tb.types.CallbackQuery):
        return self.qbox.current_state == State.SMALL_TALK and \
            call.data == 'shedule'

    @hijab
    def delete(self, call: tb.types.CallbackQuery, bot: tb.TeleBot):
        self.qbox.current_state = State.DELETE_QUEST
        pandoras = self.qbox.get_table('pandora')
        serifs = self.qbox.get_table('serif_wall')
        pandoras.extend(serifs)
        print(serifs)
        menu = self.create_keyboard(pandoras)
        bot.send_message(call.from_user.id, 'Выбери квест', reply_markup=menu)

    def delete_filter(self, call: tb.types.CallbackQuery):
        return self.qbox.current_state == State.SMALL_TALK and \
            call.data == 'delete'

    @hijab
    def return_quest(self, call: tb.types.CallbackQuery, bot: tb.TeleBot):
        self.qbox.current_state = State.RETURN_QUEST
        pandoras = self.qbox.get_table('pandora')
        serifs = self.qbox.get_table('serif_wall')
        pandoras.extend(serifs)
        menu = self.create_keyboard(pandoras)
        bot.send_message(call.from_user.id, 'Выбери квест', reply_markup=menu)

    def return_filter(self, call: tb.types.CallbackQuery):
        return self.qbox.current_state == State.SMALL_TALK and \
            call.data == 'return'

    @hijab
    def close_quest(self, call: tb.types.CallbackQuery, bot: tb.TeleBot):
        self.qbox.current_state = State.CLOSE_QUEST
        pandoras = self.qbox.get_table('pandora')
        serifs = self.qbox.get_table('serif_wall')
        pandoras.extend(serifs)
        menu = self.create_keyboard(pandoras)
        bot.send_message(call.from_user.id, 'Выбери квест', reply_markup=menu)

    def close_filter(self, call: tb.types.CallbackQuery):
        return self.qbox.current_state == State.SMALL_TALK and \
            call.data == 'close'

    @hijab
    def render(self, call: tb.types.CallbackQuery, bot: tb.TeleBot):
        self.qbox.current_state = State.SMALL_TALK
        quests = self.qbox.get_table('pandora')
        menu = self.create_inline_keyboard(quests)
        bot.send_message(call.from_user.id, 'Пандора:', reply_markup=menu)

    def render_filter(self, call: tb.types.CallbackQuery):
        return self.qbox.current_state == State.SMALL_TALK and \
            call.data == 'get_quest'

    @hijab
    def serifs(self, call: tb.types.CallbackQuery, bot: tb.TeleBot):
        self.qbox.current_state = State.SMALL_TALK
        quests = self.qbox.get_table('serif_wall')
        menu = self.create_inline_keyboard(quests)
        bot.send_message(call.from_user.id, 'Засечки:', reply_markup=menu)

    def serifs_filter(self, call: tb.types.CallbackQuery):
        return self.qbox.current_state == State.SMALL_TALK and \
            call.data == 'sheduler'

    @hijab
    def statistics(self, call: tb.types.CallbackQuery, bot: tb.TeleBot):
        self.qbox.current_state = State.SMALL_TALK
        stats = self.qbox.get_statistics()
        helper = f'Закрыто задач: #{len(stats)}#'
        data = tuple([helper])
        data = [data]
        menu = self.create_inline_keyboard(data)
        bot.send_message(call.from_user.id, 'Статистики:', reply_markup=menu)

    def stats_filter(self, call: tb.types.CallbackQuery):
        return self.qbox.current_state == State.SMALL_TALK and \
            call.data == 'get_stats'

    def create_inline_keyboard(self, data: list):
        menu = tb.types.InlineKeyboardMarkup()
        for idx, item in enumerate(data):
            butt = tb.types.InlineKeyboardButton(tuple2str(item),
                                                 callback_data=str(idx))
            menu.add(butt)
        return menu

    def create_keyboard(self, data: list, short_term=True):
        menu = tb.types.ReplyKeyboardMarkup(one_time_keyboard=short_term,
                                            resize_keyboard=True)
        for item in data:
            butt = tb.types.KeyboardButton(item[0])
            menu.add(butt)
        return menu

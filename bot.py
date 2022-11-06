from qbox.states.state import State
from qbox.handlers.messages import MessageHandler
from qbox.logic.qboxes import QuestBox
from qbox.handlers.callback import CallbackHandler

import telebot as tb
import os

db_name = 'quest_box.db'
token = os.environ.get('TOKEN')
bot = tb.TeleBot(token)
current_state = State.SMALL_TALK

qbox = QuestBox(db_name)
m_handler = MessageHandler(current_state, qbox)
c_handler = CallbackHandler(current_state, qbox)


def register_message_handlers():
    bot.register_message_handler(m_handler.start_cmd, commands=['start'],
                                 pass_bot=True)
    bot.register_message_handler(m_handler.cancel_cmd, commands=['cancel'],
                                 pass_bot=True)
    bot.register_message_handler(m_handler.add_quest,
                                 func=m_handler.add_filter, pass_bot=True)
    bot.register_message_handler(m_handler.small_talk,
                                 func=m_handler.small_talk_filter,
                                 pass_bot=True)
    bot.register_message_handler(m_handler.shedule_date_quest,
                                 func=m_handler.shedule_date_filter,
                                 pass_bot=True)
    bot.register_message_handler(m_handler.shedule_text_quest,
                                 func=m_handler.shedule_text_filter,
                                 pass_bot=True)
    bot.register_message_handler(m_handler.activate,
                                 func=m_handler.activate_filter,
                                 pass_bot=True)
    bot.register_message_handler(m_handler.delete,
                                 func=m_handler.delete_filter,
                                 pass_bot=True)


def register_callback_handlers():
    bot.register_callback_query_handler(c_handler.add_quest,
                                        func=c_handler.add_filter,
                                        pass_bot=True)
    bot.register_callback_query_handler(c_handler.activate,
                                        func=c_handler.activate_filter,
                                        pass_bot=True)
    bot.register_callback_query_handler(c_handler.shedule,
                                        func=c_handler.shedule_filter,
                                        pass_bot=True)
    bot.register_callback_query_handler(c_handler.delete,
                                        func=c_handler.delete_filter,
                                        pass_bot=True)


if __name__ == '__main__':
    register_callback_handlers()
    register_message_handlers()
    bot.infinity_polling()

from qbox.states.state import State
from qbox.handlers.messages import MessageHandler
from qbox.logic.qboxes import QuestBox
from qbox.handlers.callback import CallbackHandler

import telebot as tb
import os

db_name = 'quest_box.db'
token = os.environ('TOKEN')
bot = tb.TeleBot(token)
current_state = State.SMALL_TALK

qbox = QuestBox(db_name)
m_handler = MessageHandler(current_state, qbox)
c_handler = CallbackHandler(current_state, qbox)


def register_message_handlers():
    bot.register_message_handler(m_handler.start_msg, commands=['start'],
                                 pass_bot=True)
    bot.register_message_handler(m_handler.cancel_cmd, commands=['cancel'],
                                 pass_bot=True)


def register_callback_handlers():
    pass


if __name__ == '__main__':
    bot.infinity_polling()

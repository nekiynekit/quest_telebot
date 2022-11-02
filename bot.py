from qbox.states.state import State
from qbox.handlers.messages import start_msg, quest_name_process

import telebot as tb
import os


token = os.environ('TOKEN')

bot = tb.TeleBot(token)

current_state = State.SMALL_TALK

def register_all():
    pass


if __name__ == '__main__':
    bot.infinity_polling()
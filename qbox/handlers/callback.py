from states.state import State
from logic.qboxes import QuestBox
from utils.wrappers import hijab

import telebot as tb


class CallbackHandler():

    def __init__(self, state: State, qbox: QuestBox):
        self.qbox = qbox
        self.current_state = state

    @hijab
    def add_quest(self, call: tb.types.CallbackQuery, bot: tb.TeleBot):
        self.current_state = State.ADD_NEW_QUEST
        # TODO

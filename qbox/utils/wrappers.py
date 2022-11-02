import os

from states.state import State


user_id = os.environ('USER_ID')


def hijab(face, bot):
    
    def wrapper(message):
        global current_state
        if not isinstance(current_state, State):
            current_state = State.SMALL_TALK
        if message.from_user.id != user_id:
            bot.send_message(message.chat.id, 'Я не буду с тобой играть')
            return
        return face(message, bot)

    return wrapper

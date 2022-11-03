import os


def hijab(face):
    def wrapper(message):
        global bot
        user_id = os.environ('USER_ID')

        if message.from_user.id != user_id:
            bot.send_message(message.chat.id, 'Папа не разрешает мне \
разговаривать с незнакомцами...')
        else:
            return face(message, bot)

    return wrapper

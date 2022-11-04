import os
import telebot as tb


def hijab(face):
    print('Вход в декоратор')

    def wrapper(self, message, *args, **kwargs):
        global bot
        user_id = int(os.environ.get('USER_ID'))
        print('вход в функцию ' + face.__name__)
        if isinstance(message, tb.types.Message):
            if message.chat.id != user_id:
                bot.send_message(message.chat.id, 'Папа не разрешает мне \
    разговаривать с незнакомцами...')
            else:
                return face(self, message, *args, **kwargs)
        else:
            if message.from_user.id != user_id:
                bot.send_message(message.chat.id, 'Папа не разрешает мне \
    разговаривать с незнакомцами...')
            else:
                return face(self, message, *args, **kwargs)
    return wrapper

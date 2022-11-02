from bot import bot, hijab, quests

import telebot as tb

@bot.callback_query_handler(func=lambda x: True)
@hijab
def process_callback(call):
    finished = call.data
    new_keyboard = tb.types.InlineKeyboardMarkup()
    for quest in quests:
        if quest.callback_data == finished:
            quests.remove(quest)
            break
    for quest in quests:
        new_keyboard.add(quest)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=new_keyboard)
    if not quests:
        bot.send_message(call.message.chat.id, 'Мегахарош, ты завершил все квесты, нарекаешься жоским типом')
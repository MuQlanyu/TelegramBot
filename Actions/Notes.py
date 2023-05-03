from Constants import History, bot


def note(message):
    History.add(message)


def notes(message):
    History.add(bot.send_message(message.chat.id, "Введите заметку"))
    bot.register_next_step_handler_by_chat_id(message.chat.id, )

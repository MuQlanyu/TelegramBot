from Actions.Diary import *
from Actions.Notes import *
from Actions.Commands import *


def diary(message):
    """Выводит кнопки для дневника"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    write = types.KeyboardButton(Buttons.diary_write)
    read = types.KeyboardButton(Buttons.diary_read)
    change = types.KeyboardButton(Buttons.diary_rewrite)
    back_button = types.KeyboardButton(Buttons.back)
    markup.add(write, read, change, back_button)

    History.add(bot.send_message(message.chat.id, Messages.diary_press, reply_markup=markup))


def back_to_menu(message):
    """Возвращает пользователя в главное меню"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    clear = types.KeyboardButton(Buttons.clear_chat)
    help_ = types.KeyboardButton(Buttons.help)
    diary_ = types.KeyboardButton(Buttons.diary)
    markup.add(clear, help_, diary_)

    History.add(bot.send_message(message.chat.id, Messages.back_to_meu, reply_markup=markup))


def help_button(message):
    """Выводит 'помощь'"""
    History.add(bot.send_message(message.chat.id, Messages.command_help))


@bot.message_handler(content_types=['text'])
def user_input(message):
    """Метод обработки всех кнопок"""
    History.add(message)
    History.add(bot.send_message(message.chat.id, Messages.in_process))
    History.delete_last(message)
    if message.text == Buttons.diary or message.text == Buttons.back_to_diary:
        diary(message)
    elif message.text == Buttons.diary_write:
        write_mode(message)
    elif message.text == Buttons.diary_read:
        read_mode(message)
    elif message.text == Buttons.diary_rewrite:
        rewrite_mode(message)
    elif message.text == Buttons.yesterday_note:
        write_yesterday(message)
    elif message.text == Buttons.today_note:
        write_today(message)
    elif message.text == Buttons.back:
        display_menu(message)
    elif message.text == Buttons.clear_chat:
        clear_chat(message)
    elif message.text == Buttons.help:
        help_button(message)
    else:
        History.add(bot.send_message(message.chat.id, Messages.incorrect_command))

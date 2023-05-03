import os
import datetime as dt
from Constants import *


def write_mode(message):
    """Обрабатывает нажатие на кнопку новой записи"""
    History.add(message)
    date = '-'.join(str(dt.date.today()).split('-')[::-1]) + ".txt"
    path = storage_path + '/' + str(message.from_user.id)
    today_notes = Messages.today_no_notes
    if date in os.listdir(path):
        with open(path + '/' + date, 'r') as file:
            today_notes = file.read()
    History.add(bot.send_message(message.chat.id, Messages.show_today_notes + today_notes + "\n\n"))
    History.add(bot.send_message(message.chat.id, Messages.ask_new_note))
    bot.register_next_step_handler_by_chat_id(message.chat.id, write_date)


def read_mode(message):
    """Обрабатывает нажатие на кнопку просмотра записи"""
    History.add(message)
    History.add(
        bot.send_message(message.chat.id, Messages.ask_for_date_to_read))
    bot.register_next_step_handler_by_chat_id(message.chat.id, read_call_back)


def rewrite_mode(message):
    """Обрабатывает нажатие на кнопку перезаписывания"""
    History.add(message)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    yesterday = types.KeyboardButton(Buttons.yesterday_note)
    today = types.KeyboardButton(Buttons.today_note)
    back_to_diary = types.KeyboardButton(Buttons.back_to_diary)
    markup.add(yesterday, today, back_to_diary)
    History.add(bot.send_message(message.chat.id, Messages.rewrite, reply_markup=markup))


def show_diary(message, date):
    """Выводит дневник"""
    path = storage_path + '/' + str(message.from_user.id)
    day = '-'.join(date.split('-')[::-1]) + ".txt"
    if day in os.listdir(path):
        with open(path + '/' + day, 'r') as file:
            History.add(bot.send_message(message.chat.id, file.read()))
            History.add(bot.send_message(message.chat.id, "\n\n Запись: " + day[:-3]))
    else:
        History.add(bot.send_message(message.chat.id, Messages.date_no_notes))


def read_call_back(message):
    """Обрабатывает введенную дату"""
    History.add(message)
    date = '-'.join(message.text.split('-')[::-1])
    show_diary(message, date)


def get_correct_date(date):
    """Приводит дату из datetime к нужному формату"""
    return '-'.join(str(date).split('-')[::-1]) + ".txt"


def write_date(message, day=dt.date.today()):
    """Добавляет запись в day"""
    History.add(message)
    History.add(bot.send_message(message.chat.id, Messages.successful_new_note))
    path = storage_path + '/' + str(message.from_user.id)
    with open(path + '/' + get_correct_date(day), 'a') as file:
        file.write('\n\n' + message.text)


def write_yesterday_call_back(message):
    write_date(message, dt.date.today() - dt.timedelta(days=1))


def write_yesterday(message):
    """Перезаписывает вчерашнюю дату"""
    yesterday = get_correct_date(dt.date.today() - dt.timedelta(days=1))
    if yesterday not in os.listdir(storage_path + '/' + str(message.from_user.id)):
        History.add(bot.send_message(message.chat.id, Messages.yesterday_no_notes))
        return
    History.add(bot.send_message(message.chat.id, Messages.show_yesterday_notes))
    show_diary(message, str(dt.date.today() - dt.timedelta(days=1)))
    os.remove(storage_path + '/' + str(message.from_user.id) + '/' + yesterday)
    bot.register_next_step_handler_by_chat_id(message.chat.id, write_yesterday_call_back)


def write_today(message):
    """Перезаписывает сегодняшнюю дату"""
    today = get_correct_date(dt.date.today())
    if today not in os.listdir(storage_path + '/' + str(message.from_user.id)):
        History.add(bot.send_message(message.chat.id,  Messages.today_no_notes))
        return
    History.add(bot.send_message(message.chat.id, Messages.show_today_notes))
    show_diary(message, str(dt.date.today()))
    os.remove(storage_path + '/' + str(message.from_user.id) + '/' + today)
    bot.register_next_step_handler_by_chat_id(message.chat.id, write_date)

import os
import shutil
from Constants import *


@bot.message_handler(commands=["start"])
def command_start(message):
    """Обрабатывает команду начала работы"""
    History.add(message)
    if str(message.from_user.id) in os.listdir(storage_path):
        display_menu(message)
    else:  # sign up
        user = message.from_user
        History.add(bot.send_message(message.chat.id, Messages.sign_up.format(message.from_user.first_name)))
        bot.register_next_step_handler_by_chat_id(message.chat.id, create_user)


def display_menu(message):
    """Отображает меню"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    clear = types.KeyboardButton(Buttons.clear_chat)
    help_ = types.KeyboardButton(Buttons.help)
    diary_ = types.KeyboardButton(Buttons.diary)
    markup.add(clear, help_, diary_)

    History.add(bot.send_message(message.chat.id, Messages.sign_in, reply_markup=markup))


def create_user(message):
    """Создает пользователя и подтверждает введенный пароль"""
    History.add(message)
    markup = types.InlineKeyboardMarkup(row_width=2)
    agree = types.InlineKeyboardButton("Да", callback_data="yes")
    disagree = types.InlineKeyboardButton("Нет", callback_data="no")
    markup.add(agree, disagree)

    path = storage_path + '/' + str(message.from_user.id)
    os.mkdir(path)
    with open(path + '/password.txt', 'w') as password_file:
        password_file.write(message.text)
    History.add(bot.send_message(message.chat.id, Messages.verify_password.format(message.text), reply_markup=markup))


@bot.callback_query_handler(func=lambda call: True)
def sign_up_password_agree(call):
    """Обрабатывает верность введенного пароля"""
    if call.message:
        for i in range(2):
            History.delete_last(call.message)
        if call.data == "yes":
            History.add(bot.send_message(call.message.chat.id, Messages.successful_registration))
            display_menu(call.message)
            return
        elif call.data == "no":
            History.add(bot.send_message(call.message.chat.id, Messages.choose_new_password))
            shutil.rmtree(storage_path + '/' + str(call.message.chat.id))
            bot.register_next_step_handler_by_chat_id(call.message.chat.id, create_user)


def delete_account_verification(message):
    """Подтверждает удаление аккаунта пользователя"""
    History.add(message)
    if message.text == str(message.from_user.id):
        if str(message.from_user.id) in os.listdir(storage_path):
            shutil.rmtree(storage_path + '/' + str(message.from_user.id))
        clear_chat(message)
        History.add(bot.send_message(message.chat.id, Messages.deleted_account))
    else:
        History.add(bot.send_message(message.chat.id, Messages.incorrect_verify_delete_account))


@bot.message_handler(commands=["delete_account"])
def command_delete_account(message):
    """Удаляет аккаунт"""
    History.add(message)
    History.add(bot.send_message(message.chat.id,
                                 Messages.verify_delete_account.format(str(message.from_user.id))))
    bot.register_next_step_handler_by_chat_id(message.chat.id, delete_account_verification)


def clear_chat(chat):
    """Очищает чат"""
    for mess in History.history[chat.chat.id]:
        bot.delete_message(chat.chat.id, mess)
    History.history.pop(chat.chat.id)
    display_menu(chat)

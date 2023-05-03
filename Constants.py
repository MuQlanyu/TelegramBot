import telebot as tb
import sys
from telebot import types

storage_path = "Storage"
bot = tb.TeleBot(sys.argv[1])

days = ["Понедельник", "Вторник", "Среда",
        "Четверг", "Пятница", "Суббота", "Воскресенье"]


class History:
    """Класс для работы с историей, введенных пользователем и ботом сообщений"""
    history = dict()

    @classmethod
    def add(cls, message):
        if message.chat.id in cls.history:
            cls.history[message.chat.id].append(message.id)
        else:
            cls.history[message.chat.id] = [message.id]

    @classmethod
    def delete_last(cls, message):
        bot.delete_message(message.chat.id, History.history[message.chat.id][-1])
        History.history[message.chat.id].pop()


class Buttons:
    """Класс имен кнопок"""
    clear_chat = "Очистить чат"
    help = "Помощь"
    back = "Вернуться"
    diary = "Дневник"
    diary_write = "Запись"
    diary_read = "Просмотр"
    diary_rewrite = "Перезапись"
    yesterday_note = "Вчерашняя запись"
    today_note = "Сегодняшняя запись"
    back_to_diary = "Вернуться к дневнику"


class Messages:
    """Класс собщений, которые выводятся пользователю"""
    in_process = "Обрабатываю запрос"
    sign_up = 'Привет, {}! \n\nЭто телеграм бот для ведения дневника.\n' \
              'Так как ты тут впервые тебе не помешало бы зарегистрироваться, ' \
              'для этого введи пароль, который ты бы хотел использовать'
    sign_in = 'Добро пожаловать'
    verify_password = 'Ты уверен, что хочешь этот пароль: {}?'
    successful_registration = "Эх, ещё один пользователь"
    choose_new_password = "Введи, пожалуйста, новый пароль"
    deleted_account = "Аккаунт успешно удалён"
    verify_delete_account = 'Ты уверен, что хочешь удалить аккаунт?\n В таком случае все твои записи будут стёрты\n' \
                            'Если ты правда этого хочешь введи: {}'

    incorrect_verify_delete_account = "Видимо мне с тобой ещё долго возиться."
    incorrect_command = "Прости, но я тебя не понимаю"

    command_help = "Хмм, даже не могу понять, что тебя смущает.\n\n" \
                   "Все максимально просто: то, где ты находишься - это главное меню данного бота.\n" \
                   "Отсюда у тебя есть три пути, один из которых ты уже прошел, собственно '{}'. " \
                   "Другой говорит сам за себя, '{}'\n" \
                   "И остался самый не тривиальный, '{}' - место, в котором ты можешь сделать новую запись," \
                   " посмотреть его содержимое или перезаписать ближайшую дату.\n\n\n" \
                   "Также есть команда, с помощью которой ты можешь удалить свой аккаунт: " \
                   "/delete_account".format(Buttons.help, Buttons.clear_chat, Buttons.diary)
    diary_press = "Это твой дневник"
    back_to_meu = "Меню"

    today_no_notes = "Ты сегодня ещё ничего не записывал"
    yesterday_no_notes = "Ты вчера ещё ничего не записывал"
    date_no_notes = "В этот день ты не вёл записей"
    show_today_notes = "Вот, что ты сегодня написал\n"
    show_yesterday_notes = "Вот, что ты вчера записал\n"

    ask_new_note = "Теперь ты можешь добавить новую запись"
    ask_for_date_to_read = "Введи дату записи, которую бы ты хотел увидеть\nФормат: дд-мм-гггг"

    rewrite = "С помощью этого режима ты можешь изменить только запись, " \
              "сделанную вчера или сегодня. Весь твой стыд будет сохранён"

    successful_new_note = "Запись добавлена"


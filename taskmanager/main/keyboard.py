from telebot.callback_data import CallbackData
from telebot import types
from .callback import *


#MAIN WOOD EXPORT MENU GATE
def tg_bot_menu():
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            text='Гибкие льготы 📝',
            callback_data='benefits'
        )
    )
    markup.add(
        types.InlineKeyboardButton(
            text='Мой баланс 💵',
            callback_data='my_balance'
        )
    )
    markup.add(
        types.InlineKeyboardButton(
            text='Мои сотрудники 👥',
            callback_data='my_workers'
        )
    )
    markup.add(
        types.InlineKeyboardButton(
            text='Больничный ⚕️',
            callback_data='sick_leave'
        )
    )
    markup.add(
        types.InlineKeyboardButton(
            text='Выход 🔙',
            callback_data='exit'
        )
    )
    return markup

def benefits_create_app():
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            text='Да',
            callback_data='anonymously'
        ),
        types.InlineKeyboardButton(
            text='Нет',
            callback_data='not_anonymously'
        ),
    )
    markup.add(
        types.InlineKeyboardButton(
            text='Назад 🔙',
            callback_data='feedback'
        )
    )
    return markup

#SICK_LEAVE
def sick_leave_menu():
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            text='Открыть больничный',
            callback_data='open_sick_leave'
        )
    )
    markup.add(
        types.InlineKeyboardButton(
            text='Закрыть больничный',
            callback_data='close_sick_leave'
        )
    )
    markup.add(
        types.InlineKeyboardButton(
            text='Назад 🔙',
            callback_data='baack'
        )
    )
    return markup


def anonymously_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            text='Да 🙈',
            callback_data='anonymously'
        ),
        types.InlineKeyboardButton(
            text='Нет 🐵',
            callback_data='not_anonymously'
        ),
    )
    markup.add(
        types.InlineKeyboardButton(
            text='Назад 🔙',
            callback_data='feedback'
        )
    )
    return markup
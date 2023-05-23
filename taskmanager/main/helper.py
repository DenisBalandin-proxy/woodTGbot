from django.core.management.base import BaseCommand
from django.conf import settings
from telebot import types
import telebot
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from django.core.signals import request_finished
from django.dispatch import receiver
from .management.commands.bot import CheckingAvailability

#+++++++++++++++++++++++++++++++++++++++++++++

def user_saved_signal_approved(chat_id):
    print("Request finished!")
    CheckingAvailability.mailing(chat_id,
                                 "Поздравляем! Вы успешно прошли регистрацию. Нажми /botmenu чтобы воспользоваться функционалом бота.")
    CheckingAvailability.work_experience(chat_id)
    return


def user_saved_signal_refused(chat_id):
    CheckingAvailability.mailing(chat_id,
                                 "У нас не получилось убедиться в том, что вы наш сотрудник. Обратитесь в отдел управления персоналом.")

def calculate_work_experience(chat_id):
    CheckingAvailability.work_experience(chat_id)
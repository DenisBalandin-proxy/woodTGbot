from .bot_init import bot
from telebot import types
import telebot
from telebot import TeleBot
from datetime import datetime, time, date
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from .models import User, Document, ActiveApplication, DocumentsInApplication, TempUser, Department, SickLeave



class Sick_Leave():

    application = None

    @staticmethod
    def mailing(message):
        bot.send_message(message.from_user.id, "Function success")


    @staticmethod
    def sick_leave_gate(message):
        from .keyboard import sick_leave_menu
        keyboard = sick_leave_menu()
        question = 'Выберите дальнейшие действия'
        bot.send_message(message.chat.id, text=question, reply_markup=keyboard)

    @staticmethod
    def create_celendar(message):
        calendar, step = DetailedTelegramCalendar().build()
        bot.send_message(message.chat.id,
                         f"Select {LSTEP[step]}",
                         reply_markup=calendar)
    @staticmethod
    @bot.callback_query_handler(func=DetailedTelegramCalendar.func())
    def cal(c):
        result, key, step = DetailedTelegramCalendar(locale='ru').process(c.data)
        if not result and key:
            bot.edit_message_text(f"Select {LSTEP[step]}",
                                  c.message.chat.id,
                                  c.message.message_id,
                                  reply_markup=key)
        elif result:
            bot.edit_message_text(f"{result}",
                                  c.message.chat.id,
                                  c.message.message_id)
            if not Sick_Leave.application:
                Sick_Leave.save_sick_leave_application(c.message.chat.id, result)
            else:
                Sick_Leave.save_end_sick_leave_application(c.message.chat.id, Sick_Leave.application, result)


    @staticmethod
    def save_sick_leave_application(message, date):
        user = User.objects.filter(chat_id=message).first()

        SickLeave.objects.create(chat_id=user.chat_id,
                                 fio=user.user_fio,
                                 department=user.department_user,
                                 start_date=date)


    @staticmethod
    def save_end_sick_leave_application(message, app, result):
        app.end_date = result
        app.save()
        Sick_Leave.application = None


    @staticmethod
    def close_sick_leave(message, apps):
        for app in apps:
            print(app)
            date = str(app.start_date)
            if date == message.text:
                print("true")
                Sick_Leave.application = app
                Sick_Leave.create_celendar(message)
        #app = SickLeave.objects.filter(chat_id=message.from_user.id, start_date=message.text).first()
        #Sick_Leave.application = app
        #Sick_Leave.create_celendar(message)

    @staticmethod
    def notify_supervisor_start(message):
        print("notify supervisor")
        print("notify buh")

    @staticmethod
    def notify_supervisor_end(message):
        print("notify supervisor")
        print("notify buh")
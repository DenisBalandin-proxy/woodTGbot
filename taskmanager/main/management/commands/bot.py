import uuid

from django.core.management.base import BaseCommand
from django.conf import settings
from telebot import types
import telebot
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from ...models import User, Document, ActiveApplication, DocumentsInApplication, TempUser, Department, BenefitSession
from datetime import datetime, time, date
from ...bot_init import bot
from ...tasks import supper_sum
#from ....wood_export_bot.celery import app
from ...sick_leave import Sick_Leave
#from ...keyboard import *
#from ...callback import *
#from ...helper import MainBotMenu


#bot = telebot.TeleBot(settings.TOKEN)
class CheckingAvailability():

    def check_user(message):
        #ДОБАВИТЬ FIRST() ЧТОБЫ СРАЗУ ФИЛЬТРОВАТЬ И БРАТЬ ПЕРВЫЙ ЭЛЕМЕНТ ИЗ БАЗЫ
        user = User.objects.filter(chat_id=message.from_user.id).first()

        if not user:
            bot.send_message(message.from_user.id, "Отказано в доступе")
            return False
        else:
            if user.access == "A" and not user.fired:
                return True
            else:
                bot.send_message(message.from_user.id, "Отказано в доступе")
                return False

    def mailing(chat_id, text):
        bot.send_message(chat_id, text)

    def work_experience(chat_id):
        user_data = User.objects.get(chat_id=chat_id)

        date_of_hiring = user_data.dateOfHiring
        date_today = datetime.today().date()

        wort_experience_in_days = date_today - date_of_hiring
        experience = wort_experience_in_days.days

        if experience <= 365:
            user_data.balance = 10000
        elif experience > 365 and experience <= 1095:
            user_data.balance = 20000
        elif experience > 1095 and experience <= 1825:
            user_data.balance = 30000
        elif experience > 1825:
            user_data.balance = 50000

        user_data.save()


class Command(BaseCommand):
  	# Используется как описание команды обычно
    help = 'Implemented to Django application telegram bot setup command'

    sessions = BenefitSession.objects.all()

    if sessions:
        sessions.delete()


    #for i in range(1, 100):
     #   add(i, i)

    def handle(self, *args, **options):
        description = """
        Команды чат-бота.
        Регистрация: /reg
        Состояние:
        то-то ещё
        """

        # REGISTRATION_MENU+++++++++++++++++++++++++++++
        @bot.message_handler(commands=['start', 'auth'])
        def auth_process(message):

            supper_sum(5, 7)

            print("ENDD")
            #print()
            bot.send_message(630157933, "FOCKIN YEAH")
            user = User.objects.filter(chat_id=message.from_user.id).first()

            if user:
                bot.send_message(message.from_user.id, "Вы уже регистрировались")
                return

            bot.send_message(message.from_user.id, 'Авторизация в чате WoodExportBot. Введите ваш номер телефона в формате 89009009090')
            bot.register_next_step_handler(message, auth_phone)

        def auth_phone(message):
            global phone
            if message.content_type == 'text':
                phone = message.text

                user = User.objects.filter(phone=phone).first()

                if user:
                    bot.send_message(message.from_user.id, 'Введите pin-code, который вам предоставил отдел подбора персонала')
                    bot.register_next_step_handler(message, auth_pin, user)
                else:
                    bot.send_message(message.from_user.id, 'Не удалось определить ваш номер телефона. Попробуйте повторно через меню авторизации.')

        def auth_pin(message, user):
            global pin
            if message.content_type == 'text':
                pin = message.text

                if user.phone == phone and user.pin_code == pin:
                    user.access = 'A'
                    user.chat_id = message.from_user.id
                    user.save()

                    CheckingAvailability.work_experience(message.from_user.id)
                    bot.send_message(message.from_user.id, 'Поздравляем! Вы успешно авторизовались в чате! Откройте меню чтобы ознакомиться с функционалом!')
                else:
                    bot.send_message(message.from_user.id,
                                     'Не удалось подтвердить pin-code. Попробуйте повторно через меню авторизации.')


        #BENEFITS MENU+++++++++++++++++++++++++++++++++++++++++
        @bot.message_handler(commands=['menu'])
        def bot_menu_main_gate(message):
            check_user = CheckingAvailability.check_user(message)

            if check_user == False:
                return
            from ...keyboard import tg_bot_menu
            keyboard = tg_bot_menu()
            text = "Выбирите дальнейшие действия"
            bot.send_message(message.from_user.id, text=text, reply_markup=keyboard)




        #RECEIVE MY WORKERS GATE++++++++++++++++
        def my_workers(message):

            my_users = []
            m_u = []
            user = User.objects.filter(chat_id=message).first()
            dep_head = Department.objects.filter(supervisor_dep=user.pk).first()

            if not dep_head:
                bot.send_message(message, 'У вас нет сотрудников')
                return

            users = User.objects.filter(department_user=dep_head.pk)

            if users:
                for user in users:
                    my_users.append(user.user_fio)
                    m_u.append(user)

            keyboard = types.ReplyKeyboardMarkup(
                row_width=2,
                resize_keyboard=True,
                one_time_keyboard=True
            )
            for user in my_users:
                btn = types.KeyboardButton(user)
                keyboard.add(btn)
            # Отправляем клавиатуру
            msg = bot.send_message(
                message, 'Выберите пользователя',
                reply_markup=keyboard
            )
            bot.register_next_step_handler(msg, get_my_workers_info, m_u)


        def get_my_workers_info(message, my_users):
            for user in my_users:
                if user.user_fio == message.text:
                    info = "Баланс: " + user.balance + "\nДата рождения: " + user.dateOfBirth
                    bot.send_message(message, info)


        #В ОТДЕЛЬНЫЙ ФАЙЛ
        def show_balance(message):
            user = User.objects.filter(chat_id=message).first()
            balance = user.balance
            bot.send_message(message, f"Ваш баланс: {balance}")




        # CELENDAR_KEYBOARD+++++++++++++++++++++++++++++++++++
#        def create_celendar(message):
#            calendar, step = DetailedTelegramCalendar().build()
#            bot.send_message(message.chat.id,
#                             f"Select {LSTEP[step]}",
#                             reply_markup=calendar)

#        @bot.callback_query_handler(func=DetailedTelegramCalendar.func())
#        def cal(c):
#            result, key, step = DetailedTelegramCalendar(locale='ru').process(c.data)
#            if not result and key:
#                bot.edit_message_text(f"Select {LSTEP[step]}",
#                                      c.message.chat.id,
#                                      c.message.message_id,
#                                      reply_markup=key)
#            elif result:
#                bot.edit_message_text(f"{result}",
#                                      c.message.chat.id,
#                                     c.message.message_id)
        # REGISTRATION_CALLBACK++++++++++++++++++++++++++++++++++++
        #ПЕРЕНЁС В КОЛБЭКИ
       # @bot.callback_query_handler(func=lambda call: True)
        #def callback_registration_menu(call):
        #    if call.data == "yes":  # call.data это callback_data, которую мы указали при объявлении кнопки
         #       bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
          #      bot.send_message(call.message.chat.id, "Введите ФИО")
   #             bot.register_next_step_handler(call.message, tempRegister)
    #        elif call.data == "no":
     #           bot.delete_message(call.message.chat.id, call.message.message_id)
      #      elif call.data == 'benefits':
       #         #bot.delete_message(call.message.chat.id, call.message.message_id)
        #        select_benefit(call)
#                bot.delete_message(call.message.chat.id, call.message.message_id)
 #           elif call.data == 'balance':
  #              show_balance(call.message.chat.id)
   #             bot.delete_message(call.message.chat.id, call.message.message_id)
    #        elif call.data == 'workers':
     #           my_workers(call.message.chat.id)
      #          bot.delete_message(call.message.chat.id, call.message.message_id)
       #     elif call.data == 'sick_leave':
        #        #create_celendar(call.message)
         #       Sick_Leave.sick_leave_gate(call.message)
          #      bot.delete_message(call.message.chat.id, call.message.message_id)

                #bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            # bot.register_next_step_handler(call.message.chat, set_fio);

        #LONGPOOLING - поменять на WEBHOOK
        bot.polling(none_stop=True, interval=0)
import uuid

from django.core.management.base import BaseCommand
from django.conf import settings
from telebot import types
import telebot
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from ...models import User, Document, ActiveApplication, DocumentsInApplication, TempUser, Department
from datetime import datetime, time, date
#from ...helper import MainBotMenu


bot = telebot.TeleBot(settings.TOKEN)
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

    def handle(self, *args, **options):
        description = """
        Команды чат-бота.
        Регистрация: /reg
        Состояние:
        то-то ещё
        """

        #TEST+++++TEST++++++TEST++++++
        @bot.message_handler(commands=['fuck'])
        def fuck(message):
            from ...helper import MainMenuBot
            MainMenuBot().mailing(message)

        # REGISTRATION_MENU+++++++++++++++++++++++++++++MBMBMBMBMBMBMBMBMBMBMBMBMBM
        @bot.message_handler(commands=['auth'])
        def auth_process(message):
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


        # REGISTRATION_MENU+++++++++++++++++++++++++++++
        @bot.message_handler(commands=['star', 'registratio'])
        def registrationMenu(message):

            user = User.objects.filter(chat_id=message.from_user.id).first()

            if user:
                bot.send_message(message.from_user.id, "Вы уже регистрировались")
                return

            keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
            key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')  # кнопка «Да»
            keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
            key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
            keyboard.add(key_no)
            question = 'Зарегистрироваться сейчас?'
            bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


        #SET USER'S FIO++++++++++++++++++++++++++
        def set_fio(message):
            bot.send_message(message.from_user.id, "Введите ФИО")
            bot.register_next_step_handler(message, tempRegister)

        #REGISTER NEW USER IN DATABASE+++++++++++++++++++++++++
        def tempRegister(message):

            TempUser.objects.create(chat_id=message.from_user.id, user_fio=message.text, access="R")
            User.objects.create(chat_id=message.from_user.id, user_fio=message.text)
            bot.send_message(message.from_user.id, "Ваша заявка на рассмотрении")

        #BENEFITS MENU+++++++++++++++++++++++++++++++++++++++++
        @bot.message_handler(commands=['menu'])
        def bot_menu_main_gate(message):
            check_user = CheckingAvailability.check_user(message)

            if check_user == False:
                return

            keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
            key_yes = types.InlineKeyboardButton(text='Гибкие льготы 📝', callback_data='benefits')  # кнопка «Да»
            keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
            key_no = types.InlineKeyboardButton(text='Мой баланс 💵', callback_data='balance')
            keyboard.add(key_no)
            key_no = types.InlineKeyboardButton(text='Мои сотрудники 👥', callback_data='workers')
            keyboard.add(key_no)
            question = 'Выберите дальнейшие действия'
            bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)




        def select_test(message):
            # Создаем клавиатуру

            check_user = CheckingAvailability.check_user(message)

            if check_user == False:
                return

            document = Document.objects.all()
            buttons = document
            keyboard = types.ReplyKeyboardMarkup(
                row_width=2,
                resize_keyboard=True,
                one_time_keyboard=True
            )
            for but in buttons:
                btn = types.KeyboardButton(but.document)
                keyboard.add(btn)
            # Отправляем клавиатуру
            msg = bot.send_message(
                message.from_user.id, 'Выберите услугу',
                reply_markup=keyboard
            )
            bot.register_next_step_handler(msg, on_selection)


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


        def select_benefit(message):
            # Создаем клавиатуру

            check_user = CheckingAvailability.check_user(message)

            if check_user == False:
                return

            buttons = ["Путешествия", "Здоровье", "Образование", "Выйти из меню"]
            keyboard = types.ReplyKeyboardMarkup(
                row_width=2,
                resize_keyboard=True,
                one_time_keyboard=True
            )
            for but in buttons:
                btn = types.KeyboardButton(but)
                keyboard.add(btn)
            # Отправляем клавиатуру
            msg = bot.send_message(
                message.from_user.id, 'Выберите услугу',
                reply_markup=keyboard
            )
            bot.register_next_step_handler(msg, on_selection)

        # Функция обработки выбора из клавиатуры из бенифитсов
        def on_selection(message):
            photos = []
            if message.content_type == 'text':
                selection = message.text
                if selection == "Путешествия":
                    bot.send_message(message.from_user.id,
                                     'ВАЖНО! Отправляйте фото по одной штуке. Когда все фото будут отправлены, нажмите "Завершить подачу документов"')
                    benefit_application_cycle(message, None, selection, photos)
                elif selection == "Здоровье":
                    bot.send_message(message.from_user.id,
                                     'ВАЖНО! Отправляйте фото по одной штуке. Когда все фото будут отправлены, нажмите "Завершить подачу документов"')
                    benefit_application_cycle(message, None, selection, photos)
                elif selection == "Образование":
                    bot.send_message(message.from_user.id,
                                     'ВАЖНО! Отправляйте фото по одной штуке. Когда все фото будут отправлены, нажмите "Завершить подачу документов"')
                    benefit_application_cycle(message, None, selection, photos)
                elif selection == "Выйти из меню":
                    return
                else:
                    select_benefit(message)
                ### В selection теперь будет текст с кнопки, на которую нажал
            else:
                select_benefit(message)


            #ЦЕПОЧТА ПРИКРЕПЛЕНИЯ ДОКУМЕНТОВ В БАЗУ
        def benefit_application_cycle(message, app_id, benefit, photos):

            buttons = ["Завершить подачу документов"]
            keyboard = types.ReplyKeyboardMarkup(
                row_width=2,
                resize_keyboard=True,
                one_time_keyboard=True
            )
            for but in buttons:
                btn = types.KeyboardButton(but)
                keyboard.add(btn)
            # Отправляем клавиатуру
            msg = bot.send_message(
                message.from_user.id, 'Ожидаю действий',
                reply_markup=keyboard
            )
            #bot.send_message(message.from_user.id, description)
            bot.register_next_step_handler(message, save_photo_to_database, app_id, benefit, photos)

#++++++++DELETE++++++++++
        def on_selection_saving_photo_gate(message, app_id, benefit):
            if message.content_type == 'photo':
                save_photo_to_database(message, app_id, benefit)
            elif message.text == "Завершить подачу документов" and not app_id:
                bot.send_message(message.from_user.id, 'Заявка не сформирована, нет ни одного фото')
                return
            elif message.text == "Завершить подачу документов" and app_id:
                user = User.objects.get(chat_id=message.from_user.id)
                bot.send_message(message.from_user.id, 'Ваш баланс:' + str(user.balance) + 'Введите сумму выплат')
                bot.register_next_step_handler(message, set_benefits_sum, app_id, user.balance)
            elif message.content_type == 'text' and message.text != 'Завершить подачу документов':
                bot.send_message(message.from_user.id, "Файл должен быть фотографией")
                benefit_application_cycle(message, app_id, benefit)
            ### В selection теперь будет текст с кнопки, на которую нажал

        def set_benefits_sum(message, app_id, balance, photos, benefit):
            if message.content_type != 'text':
                bot.send_message(message.from_user.id, "Введите сумму выплаты")
                bot.register_next_step_handler(message, set_benefits_sum, app_id, balance, photos, benefit)
            else:
                if message.text.isdigit():
                    integer_sum = int(message.text)
                    if balance >= integer_sum and integer_sum > 0:
                        count = balance - integer_sum
                        user = User.objects.get(chat_id=message.from_user.id)
                        user.balance = count
                        user.save()

                        save_application_processing(message, None, photos, benefit, integer_sum)
                        #app = ActiveApplication.objects.get(pk=app_id)
                        #app.sum = integer_sum
                        #app.save()
                    else:
                        bot.send_message(message.from_user.id, "Введённая сумма больше баланса. Введите снова")
                        bot.register_next_step_handler(message, set_benefits_sum, app_id, balance, photos, benefit)
                else:
                    bot.send_message(message.from_user.id, "Введите сумму цифрами")
                    bot.register_next_step_handler(message, set_benefits_sum, app_id, balance, photos, benefit)


        def save_photo_to_database(message, app_id, benefit, arrPhotos):
            if message.content_type == 'photo':
                application_id = app_id
                photos = arrPhotos

                file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                file = message.photo[1].file_id + ".jpg"
                src = "C:/Users/Operator11/Desktop/PC WORK/Python/WoodExport_BOT_DJANGO/taskmanager/media/" + \
                    message.photo[1].file_id + ".jpg"
                with open(src, 'wb') as new_file:
                    new_file.write(downloaded_file)

                    arrPhotos.append(file)

                bot.send_message(message.from_user.id, "Сохранил фото")
                benefit_application_cycle(message, app_id, benefit, arrPhotos)

            elif message.text == "Завершить подачу документов" and not arrPhotos:
                bot.send_message(message.from_user.id, 'Заявка не сформирована, нет ни одного фото')
                return
            elif message.text == "Завершить подачу документов" and arrPhotos:
                user = User.objects.get(chat_id=message.from_user.id)
                bot.send_message(message.from_user.id, 'Ваш баланс:' + ' ' + str(user.balance) + '. ' + 'Введите сумму выплат')
                bot.register_next_step_handler(message, set_benefits_sum, app_id, user.balance, arrPhotos, benefit)
            elif message.content_type == 'text' and message.text != 'Завершить подачу документов':
                bot.send_message(message.from_user.id, "Файл должен быть фотографией")
                benefit_application_cycle(message, app_id, benefit, arrPhotos)
            ### В selection теперь будет текст с кнопки, на которую нажал


                # item = Item.objects.get()
                # cart = Cart.object.get(fio=user.user_fio, benefit="Путешествие")

                #bot.register_next_step_handler(message, traveling_check, application_id)
            #else:
            #    bot.send_message(message.from_user.id, "Файл не является фотографией!!!")
            #    bot.register_next_step_handler(message, save_photo_to_database, None)

        def traveling_final(message):
            bot.send_message(message.from_user.id, "Ваша заявка на рассмотрении.")



        def save_application_processing(message, app_id, photos, benefit, balance):
            user = User.objects.get(chat_id=message.from_user.id)

            application = ActiveApplication.objects.create(chat_id=user.chat_id, fio=user.user_fio, benefit=benefit, sum=balance)

            for photo in photos:
                document = Document.objects.create(document="Документ", image=photo)
                DocumentsInApplication.objects.create(application_id=application.pk, document_id=document.pk)

            bot.send_message(message.from_user.id, 'Ваша заявка на рассмотрении')


        #В ОТДЕЛЬНЫЙ ФАЙЛ
        def show_balance(message):
            user = User.objects.filter(chat_id=message).first()
            balance = user.balance
            bot.send_message(message, f"Ваш баланс: {balance}")



        # CELENDAR_KEYBOARD+++++++++++++++++++++++++++++++++++
        def create_celendar(message):
            calendar, step = DetailedTelegramCalendar().build()
            bot.send_message(message.chat.id,
                             f"Select {LSTEP[step]}",
                             reply_markup=calendar)

        @bot.callback_query_handler(func=DetailedTelegramCalendar.func())
        def cal(c):
            result, key, step = DetailedTelegramCalendar().process(c.data)
            if not result and key:
                bot.edit_message_text(f"Select {LSTEP[step]}",
                                      c.message.chat.id,
                                      c.message.message_id,
                                      reply_markup=key)
            elif result:
                bot.edit_message_text(f"You selected {result}",
                                      c.message.chat.id,
                                      c.message.message_id)

        # REGISTRATION_CALLBACK++++++++++++++++++++++++++++++++++++
        @bot.callback_query_handler(func=lambda call: True)
        def callback_registration_menu(call):
            if call.data == "yes":  # call.data это callback_data, которую мы указали при объявлении кнопки
                bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
                bot.send_message(call.message.chat.id, "Введите ФИО")
                bot.register_next_step_handler(call.message, tempRegister)
            elif call.data == "no":
                bot.delete_message(call.message.chat.id, call.message.message_id)
            elif call.data == 'benefits':
                #bot.delete_message(call.message.chat.id, call.message.message_id)
                select_benefit(call)
                bot.delete_message(call.message.chat.id, call.message.message_id)
            elif call.data == 'balance':
                show_balance(call.message.chat.id)
                bot.delete_message(call.message.chat.id, call.message.message_id)
            elif call.data == 'workers':
                my_workers(call.message.chat.id)
                bot.delete_message(call.message.chat.id, call.message.message_id)

                #bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            # bot.register_next_step_handler(call.message.chat, set_fio);

        #LONGPOOLING - поменять на WEBHOOK
        bot.polling(none_stop=True, interval=0)
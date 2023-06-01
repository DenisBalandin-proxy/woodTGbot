from django.core.management.base import BaseCommand
from django.conf import settings
from telebot import types
import telebot
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from django.core.signals import request_finished
from django.dispatch import receiver
from .management.commands.bot import CheckingAvailability
from .models import User, Document, ActiveApplication, DocumentsInApplication, TempUser, Department, SickLeave
from .bot_init import bot
#from .management.commands.bot import bot

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


class MainMenuBot():

    @staticmethod
    def mailing(message, bot):
        bot.send_message(message.from_user.id, "Function success")



#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class Benefits():

    @staticmethod
    def testt(message):
        if bot.get_updates():
            print("HAVA LULU")

    @staticmethod
    def select_benefit_gate(message):
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
        bot.register_next_step_handler(msg, Benefits.on_selection)

    @staticmethod
    def on_selection(message):
        photos = []
        if message.content_type == 'text':
            selection = message.text
            if selection == "Путешествия":
                bot.send_message(message.from_user.id,
                                 'ВАЖНО! Отправляйте фото по одной штуке. Когда все фото будут отправлены, нажмите "Завершить подачу документов"')
                Benefits.benefit_application_cycle(message, None, selection, photos)
            elif selection == "Здоровье":
                bot.send_message(message.from_user.id,
                                 'ВАЖНО! Отправляйте фото по одной штуке. Когда все фото будут отправлены, нажмите "Завершить подачу документов"')
                Benefits.benefit_application_cycle(message, None, selection, photos)
            elif selection == "Образование":
                bot.send_message(message.from_user.id,
                                 'ВАЖНО! Отправляйте фото по одной штуке. Когда все фото будут отправлены, нажмите "Завершить подачу документов"')
                Benefits.benefit_application_cycle(message, None, selection, photos)
            elif selection == "Выйти из меню":
                return
            else:
                Benefits.select_benefit(message)
            ### В selection теперь будет текст с кнопки, на которую нажал
        else:
            Benefits.select_benefit(message)

    @staticmethod
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
        # bot.send_message(message.from_user.id, description)
        bot.register_next_step_handler(message, Benefits.save_photo_to_database, app_id, benefit, photos)


    @staticmethod
    def test_http(message):
        url = f"http://www.onlinestor.com?chat=f{message.from_user.id}&fio=f{message.text}"
        bot.send_message(message.from_user.id, text=url)



    @staticmethod
    def save_photo_to_database(message, app_id, benefit, arrPhotos):
        if message.content_type == 'photo':
            application_id = app_id
            photos = arrPhotos

            for i in message.photo:
                print(i)

            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            file = message.photo[1].file_id + ".jpg"
            src = "C:/Users/Operator11/Desktop/WTG/woodTGbot/taskmanager/media/" + \
                  message.photo[1].file_id + ".jpg"
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)

                arrPhotos.append(file)

            bot.send_message(message.from_user.id, "Сохранил фото")
            Benefits.benefit_application_cycle(message, app_id, benefit, arrPhotos)

        elif message.text == "Завершить подачу документов" and not arrPhotos:
            bot.send_message(message.from_user.id, 'Заявка не сформирована, нет ни одного фото')
            return
        elif message.text == "Завершить подачу документов" and arrPhotos:
            user = User.objects.get(chat_id=message.from_user.id)
            bot.send_message(message.from_user.id,
                             'Ваш баланс:' + ' ' + str(user.balance) + '. ' + 'Введите сумму выплат')
            bot.register_next_step_handler(message, Benefits.set_benefits_sum, app_id, user.balance, arrPhotos, benefit)
        elif message.content_type == 'text' and message.text != 'Завершить подачу документов':
            bot.send_message(message.from_user.id, "Файл должен быть фотографией")
            Benefits.benefit_application_cycle(message, app_id, benefit, arrPhotos)
        ### В selection теперь будет текст с кнопки, на которую нажал


    @staticmethod
    def set_benefits_sum(message, app_id, balance, photos, benefit):
        if message.content_type != 'text':
            bot.send_message(message.from_user.id, "Введите сумму выплаты")
            bot.register_next_step_handler(message, Benefits.set_benefits_sum, app_id, balance, photos, benefit)
        else:
            if message.text.isdigit():
                integer_sum = int(message.text)
                if balance >= integer_sum and integer_sum > 0:

                    buttons = ["Да", "Нет"]
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
                        message.from_user.id, f'Сформировать заявку на {benefit}, сумма выплаты: {integer_sum} ?',
                        reply_markup=keyboard
                    )
                    bot.register_next_step_handler(message, Benefits.save_application_processing, None, photos, benefit, balance,
                                                   integer_sum)
                    # save_application_processing(message, None, photos, benefit, integer_sum)
                    # app = ActiveApplication.objects.get(pk=app_id)
                    # app.sum = integer_sum
                    # app.save()
                else:
                    bot.send_message(message.from_user.id, "Введённая сумма больше баланса. Введите снова")
                    bot.register_next_step_handler(message, Benefits.set_benefits_sum, app_id, balance, photos, benefit)
            else:
                bot.send_message(message.from_user.id, "Введите сумму цифрами")
                bot.register_next_step_handler(message, Benefits.set_benefits_sum, app_id, balance, photos, benefit)

    @staticmethod
    def save_application_processing(message, app_id, photos, benefit, balance, sum):
        if message.text == "Да":
            count = balance - sum
            user = User.objects.get(chat_id=message.from_user.id)  # FILTER AND FIRST
            user.balance = count
            user.save()

            application = ActiveApplication.objects.create(chat_id=user.chat_id, fio=user.user_fio, benefit=benefit,
                                                           sum=sum)

            for photo in photos:
                document = Document.objects.create(document="Документ", image=photo)
                DocumentsInApplication.objects.create(application_id=application.pk, document_id=document.pk)

            bot.send_message(message.from_user.id, 'Ваша заявка на рассмотрении')

        else:
            bot.send_message(message.from_user.id, "Заявка не сформирована")




class MyWorkers():
    @staticmethod
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
        bot.register_next_step_handler(msg, MyWorkers.get_my_workers_info, m_u)

    @staticmethod
    def get_my_workers_info(message, my_users):
        for user in my_users:
            if user.user_fio == message.text:
                info = "Баланс: " + user.balance + "\nДата рождения: " + user.dateOfBirth
                bot.send_message(message, info)
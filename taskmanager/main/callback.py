from telebot.callback_data import CallbackData
from telebot import types
from .bot_init import bot
from .sick_leave import Sick_Leave
from .models import SickLeave
from .helper import Benefits, Balance


#@bot.callback_query_handler(func=lambda call: True)
#def callback_registration_menu(call):
   # if call.data == "yes":  # call.data это callback_data, которую мы указали при объявлении кнопки
   #     bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
   #     bot.send_message(call.message.chat.id, "Введите ФИО")
   #     bot.register_next_step_handler(call.message, tempRegister)
   # elif call.data == "no":
        #bot.delete_message(call.message.chat.id, call.message.message_id)
#    if call.data == 'benefits':
#        # bot.delete_message(call.message.chat.id, call.message.message_id)
#        select_benefit(call)
#        bot.delete_message(call.message.chat.id, call.message.message_id)
#    elif call.data == 'balance':
#        show_balance(call.message.chat.id)
#        bot.delete_message(call.message.chat.id, call.message.message_id)
#    elif call.data == 'workers':
#        my_workers(call.message.chat.id)
#        bot.delete_message(call.message.chat.id, call.message.message_id)
#    elif call.data == 'sick_leav':
        # create_celendar(call.message)
        ##Sick_Leave.sick_leave_gate(call.message)
#        bot.delete_message(call.message.chat.id, call.message.message_id)
#    elif call.data == 'exit':
#        bot.delete_message(call.message.chat.id, call.message.message_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('benefit_menu'))
def benefits_gate(call):
    from .keyboard import benefit_menu
    keyboard = benefit_menu()
    bot.edit_message_text("Выбирите действие", call.message.chat.id, call.message.message_id, reply_markup=keyboard)
    #Benefits.select_benefit_gate(call)
    #Benefits.testt(call)
    #Benefits.benefits_gate(call)


@bot.callback_query_handler(func=lambda call: call.data.startswith('benefits'))
def benefits_gate(call):
    Benefits.benefits_gate(call)

@bot.callback_query_handler(func=lambda call: call.data.startswith('traveling'))
def traveling(call):
    bot.send_message(call.message.chat.id, "Введите сумму выплаты")
    bot.register_next_step_handler(call.message, Benefits.create_benefits_url, call.data)
    bot.delete_message(call.message.chat.id, call.message.message_id)
    #Benefits.create_benefits_url(call.message, "Путешествие")

@bot.callback_query_handler(func=lambda call: call.data.startswith('health'))
def health(call):
    bot.send_message(call.message.chat.id, "Введите сумму выплаты")
    bot.register_next_step_handler(call.message, Benefits.create_benefits_url, call.data)
    bot.delete_message(call.message.chat.id, call.message.message_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('education'))
def education(call):
    bot.send_message(call.message.chat.id, "Введите сумму выплаты")
    bot.register_next_step_handler(call.message, Benefits.create_benefits_url, call.data)
    bot.delete_message(call.message.chat.id, call.message.message_id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('sport'))
def sport(call):
    bot.send_message(call.message.chat.id, "Введите сумму выплаты")
    bot.register_next_step_handler(call.message, Benefits.create_benefits_url, call.data)
    bot.delete_message(call.message.chat.id, call.message.message_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('sick_leave'))
def sick_leave_gate(call):
    Sick_Leave.sick_leave_gate(call.message)
    bot.delete_message(call.message.chat.id, call.message.message_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('open_sick_leave'))
def sick_leave_start(call):
    Sick_Leave.create_celendar(call.message)
    bot.delete_message(call.message.chat.id, call.message.message_id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('close_sick_leave'))
def sick_leave_end(call):
    app = SickLeave.objects.filter(chat_id=call.message.chat.id, end_date=None)
    bot.delete_message(call.message.chat.id, call.message.message_id)

    my_app = []
    m_u = []

    if not app:
        bot.send_message(call.message.chat.id, "У вас нет больничных")
        return

    if app:
        for a in app:
            date = str(a.start_date)
            my_app.append(date)
            #m_u.append(a)

    keyboard = types.ReplyKeyboardMarkup(
        row_width=2,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    for a in my_app:
        btn = types.KeyboardButton(a)
        keyboard.add(btn)
    # Отправляем клавиатуру
    msg = bot.send_message(
        call.message.chat.id, 'Выберите больничный',
        reply_markup=keyboard
    )
    bot.register_next_step_handler(msg, Sick_Leave.close_sick_leave, app)

@bot.callback_query_handler(func=lambda call: call.data.startswith('back_to_main_menu'))
def back_to_menu(call):
    from .keyboard import tg_bot_menu
    keyboard = tg_bot_menu()
    bot.edit_message_text("Выбирите действие", call.message.chat.id, call.message.message_id, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith('back_to_benefit_menu'))
def back_to_menu(call):
    from .keyboard import benefit_menu
    keyboard = benefit_menu()
    bot.edit_message_text("Выбирите действие", call.message.chat.id, call.message.message_id, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith('my_balance'))
def receive_balance(call):
    Balance.receive_my_balance(call.message)
    #bot.delete_message(call.message.chat.id, call.message.message_id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('exit'))
def exit_main_menu(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
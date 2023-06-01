import telebot
from telebot import TeleBot
from django.conf import settings

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class SingletonBot(TeleBot, metaclass=Singleton):
    def __init__(self, *args, **kwargs):
        #token = telebot.TeleBot(settings.TOKEN)
        token = settings.TOKEN
        super().__init__(token, *args, **kwargs)

bot = SingletonBot()
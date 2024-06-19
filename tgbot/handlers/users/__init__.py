from aiogram import Dispatcher

from .user import register_user
from .secret_phrase import register_secret_phrase_handlers


def register_all_user_handlers(dp: Dispatcher):
    register_user(dp)
    register_secret_phrase_handlers(dp)

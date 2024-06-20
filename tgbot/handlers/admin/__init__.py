from aiogram import Dispatcher

from tgbot.handlers.admin.admin import register_admin
from tgbot.handlers.admin.group import register_groups_handler


def register_admin_handlers(dp: Dispatcher):
    register_admin(dp)
    register_groups_handler(dp)

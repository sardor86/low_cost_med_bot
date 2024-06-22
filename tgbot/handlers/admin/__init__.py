from aiogram import Dispatcher

from tgbot.handlers.admin.admin import register_admin
from tgbot.handlers.admin.group import register_groups_handler
from tgbot.handlers.admin.product import register_product_handler
from tgbot.handlers.admin.edit_product import register_edit_product_handlers
from tgbot.handlers.admin.discount import register_discount_handler


def register_admin_handlers(dp: Dispatcher):
    register_admin(dp)
    register_groups_handler(dp)
    register_product_handler(dp)
    register_edit_product_handlers(dp)
    register_discount_handler(dp)

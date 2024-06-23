from aiogram import Dispatcher

from .user import register_user
from .secret_phrase import register_secret_phrase_handlers
from .listing import register_listing_handlers
from .basket import register_basket_handler
from .checkout import register_checkout_handler
from .order import register_order_handler


def register_all_user_handlers(dp: Dispatcher):
    register_user(dp)
    register_secret_phrase_handlers(dp)
    register_listing_handlers(dp)
    register_basket_handler(dp)
    register_checkout_handler(dp)
    register_order_handler(dp)

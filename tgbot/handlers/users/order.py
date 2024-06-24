from aiogram import Dispatcher
from aiogram.types import CallbackQuery

from tgbot.handlers.users.checkout import checkout


async def order_menu(callback: CallbackQuery):
    message_data = await checkout(callback.from_user.id)
    await callback.message.edit_text(message_data['message_text'], reply_markup=message_data['markup'])


def register_order_handler(dp: Dispatcher):
    dp.callback_query.register(order_menu, lambda callback: callback.data == 'orders')

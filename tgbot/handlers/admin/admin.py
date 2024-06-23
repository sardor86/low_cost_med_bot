from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from tgbot.filters import AdminFilter
from tgbot.keyboards.admin import get_menu_inline_keyboard
from tgbot.models import Order


async def admin_start(message: Message):
    await message.reply("Admin panel", reply_markup=get_menu_inline_keyboard().as_markup())


async def admin_panel(callback: CallbackQuery):
    await callback.message.reply("Admin panel", reply_markup=get_menu_inline_keyboard().as_markup())


async def confirm_order(callback: CallbackQuery):
    user_id = callback.data.split('_')[-1]
    order_list = await Order().get_all_orders(int(user_id))

    for order in order_list:
        await order.update(confirmation=True).apply()
    await callback.message.reply('Order is confirmed')
    await callback.bot.send_message(int(user_id), 'your order is confirmed')


def register_admin(dp: Dispatcher):
    dp.message.register(admin_start, Command('admin'), AdminFilter())
    dp.callback_query.register(admin_panel, AdminFilter(), lambda callback: callback.data == 'admin_panel')
    dp.callback_query.register(confirm_order, AdminFilter(), lambda callback: callback.data.split('_')[0] == 'confirm')

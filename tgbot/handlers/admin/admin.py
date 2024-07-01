from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from tgbot.filters import AdminFilter, MainAdmin
from tgbot.keyboards.admin import get_menu_inline_keyboard, review_inline_keyboard
from tgbot.models import Order, Admin


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
    await callback.bot.send_message(int(user_id),
                                    'your order is confirmed',
                                    reply_markup=review_inline_keyboard().as_markup())


async def add_admin(message: Message):
    admin_id = message.text.split(' ')[-1]
    if not admin_id.isdigit():
        await message.reply('There is not id')
        return

    await Admin().add_admin(int(admin_id))
    await message.reply('Admin added')


async def del_admin(message: Message):
    admin_id = message.text.split(' ')[-1]
    if not admin_id.isdigit():
        await message.reply('There is not id')
        return
    admin_id = int(admin_id)
    if not await Admin().check_in_db_admin(admin_id):
        await message.reply('We don\'t have this admin')
        return

    await Admin().remove_admin(int(admin_id))
    await message.reply('Admin deleted')


def register_admin(dp: Dispatcher):
    dp.message.register(admin_start, Command('admin'), AdminFilter())
    dp.callback_query.register(admin_panel, AdminFilter(), lambda callback: callback.data == 'admin_panel')
    dp.callback_query.register(confirm_order, AdminFilter(), lambda callback: callback.data.split('_')[0] == 'confirm')
    dp.message.register(add_admin, Command('add'), MainAdmin())
    dp.message.register(del_admin, Command('del'), MainAdmin())

from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from tgbot.filters import AdminFilter
from tgbot.keyboards.admin import get_menu_inline_keyboard


async def admin_start(message: Message):
    await message.reply("Admin panel", reply_markup=get_menu_inline_keyboard().as_markup())


async def admin_panel(callback: CallbackQuery):
    await callback.message.reply("Admin panel", reply_markup=get_menu_inline_keyboard().as_markup())


def register_admin(dp: Dispatcher):
    dp.message.register(admin_start, Command('admin'), AdminFilter())
    dp.callback_query.register(admin_panel, AdminFilter(), lambda callback: callback.data == 'admin_panel')

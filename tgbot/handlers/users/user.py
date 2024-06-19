from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

from tgbot.models import Users
from tgbot.keyboards.user import get_register_inline_keyboard


async def user_start(message: Message):
    await message.reply(f'Welcome, {message.from_user.first_name} !')
    if not await Users().check_in_db_user(message.from_user.id):
        await message.reply('🔐 You need to set a secret phrase to access the bot. '
                            'This will then appear with every verified bot. '
                            'The secret phrase allows you to stay safe and buy only from verified stores.',
                            reply_markup=get_register_inline_keyboard().as_markup())


def register_user(dp: Dispatcher):
    dp.message.register(user_start, Command("start"))

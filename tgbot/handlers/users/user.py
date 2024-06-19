from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters import Command


async def user_start(message: Message):
    await message.reply("Hello, user!")


def register_user(dp: Dispatcher):
    dp.message.register(user_start, Command("start"))

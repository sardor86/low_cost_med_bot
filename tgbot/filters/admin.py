from aiogram.filters import Filter
from aiogram.types import Message

from tgbot.models import Admin
from tgbot.config import Config


class AdminFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        config: Config = message.bot.config
        return ((await Admin().check_in_db_admin(message.from_user.id)) or
                message.from_user.id in config.tg_bot.admin_ids)

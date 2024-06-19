import asyncio
import logging

from aiogram import Bot, Dispatcher

from tgbot.config import load_config
from tgbot.handlers import register_all_handlers

logger = logging.getLogger(__name__)


async def main():
    """
    this function set main settings and start the bot
    """
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    # set bot
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    bot.config = config
    dp = Dispatcher()

    register_all_handlers(dp)

    # start
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await dp.storage.close()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
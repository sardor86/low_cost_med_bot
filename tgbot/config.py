from dataclasses import dataclass

from environs import Env
from gino import Gino

gino_db = Gino()


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    crypto_token: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig


async def set_gino(data_base: DbConfig) -> None:
    await gino_db.set_bind(f'postgresql://{data_base.user}:'
                           f'{data_base.password}@'
                           f'{data_base.host}/'
                           f'{data_base.database}')


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str('BOT_TOKEN'),
            admin_ids=list(map(int, env.str('ADMINS').split(','))),
            crypto_token=env.str('TOKEN')
        ),
        db=DbConfig(
            host=env.str('DB_HOST'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME')
        ),
    )

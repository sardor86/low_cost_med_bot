import random

from tgbot.config import gino_db
from .base import Base


class Users(Base):
    class UsersTable(gino_db.Model):
        __tablename__ = 'users'

        id = gino_db.Column(gino_db.Integer(), primary_key=True)
        user_id = gino_db.Column(gino_db.BigInteger(), unique=True, nullable=False)
        secret_phrase = gino_db.Column(gino_db.String(), nullable=False)
        public_key = gino_db.Column(gino_db.Text(), nullable=False)

        def __str__(self) -> str:
            return f'<User {self.user_id}>'

        def __repr__(self) -> str:
            return f'<User {self.user_id}>'

    async def add_user(self, user_id: int, secret_phrase: str) -> bool:
        if not await self.check_in_db_user(user_id):
            public_key = ''
            for i in range(3060):
                public_key += random.choice('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890+=-/*')
                if (i + 1) % 48 == 0:
                    public_key += '\n'
            user = self.UsersTable(user_id=user_id,
                                   secret_phrase=secret_phrase,
                                   public_key=public_key)
            await user.create()
            return True
        else:
            return False

    async def check_in_db_user(self, user_id: int) -> bool:
        return not await self.UsersTable.query.where(self.UsersTable.user_id == user_id).gino.first() is None

    async def get_secret_phrase(self, user_id: int) -> str:
        return (await self.UsersTable.query.where(self.UsersTable.user_id == user_id).gino.first()).secret_phrase

    async def get_secret_user(self, user_id: int) -> UsersTable:
        return await self.UsersTable.query.where(self.UsersTable.user_id == user_id).gino.first()

from tgbot.config import gino_db
from .base import Base


class Discussion(Base):
    class DiscussionTable(gino_db.Model):
        __tablename__ = 'discussion'

        id = gino_db.Column(gino_db.Integer(), primary_key=True)
        user = gino_db.Column(gino_db.ForeignKey('users.user_id'), nullable=False)
        role = gino_db.Column(gino_db.String(), nullable=False)
        text = gino_db.Column(gino_db.String(), nullable=False)

        def __str__(self) -> str:
            return f'<Discussion {self.user}:{self.role}:{self.text}>'

        def __repr__(self) -> str:
            return f'<Discussion {self.user}:{self.role}:{self.text}>'

    async def add_basket(self, user: int, role: str, text: str):
        discussion = self.DiscussionTable(user=user, role=role, text=text)
        await discussion.create()

    async def get_all_discussion(self, user: int) -> list[DiscussionTable]:
        return await self.DiscussionTable.query.where(self.DiscussionTable.user == user).gino.all()

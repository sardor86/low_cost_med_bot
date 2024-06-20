from tgbot.config import gino_db
from .base import Base


class Groups(Base):
    class GroupsTable(gino_db.Model):
        __tablename__ = 'group'

        id = gino_db.Column(gino_db.Integer(), primary_key=True)
        group_name = gino_db.Column(gino_db.String(), unique=True, nullable=False)

        def __str__(self) -> str:
            return f'<Group {self.group_name}>'

        def __repr__(self) -> str:
            return f'<Group {self.group_name}>'

    async def add_group(self, group_name: str) -> bool:
        if not await self.check_in_db_group_name(group_name):
            user = self.GroupsTable(group_name=group_name)
            await user.create()
            return True
        else:
            return False

    async def check_in_db_group_name(self, group_name: str) -> bool:
        return not await self.GroupsTable.query.where(self.GroupsTable.group_name == group_name).gino.first() is None

    async def get_all_groups(self) -> list[str]:
        return [group.group_name for group in await self.GroupsTable.query.gino.all()]

    async def delete_group(self, group_name: str) -> bool:
        if await self.check_in_db_group_name(group_name):
            group = await self.GroupsTable.query.where(self.GroupsTable.group_name == group_name).gino.first()
            await group.delete()
            return True
        return False

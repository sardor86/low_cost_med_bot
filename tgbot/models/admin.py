from tgbot.config import gino_db
from .base import Base


class Admin(Base):
    class AdminTable(gino_db.Model):
        __tablename__ = 'admin'

        id = gino_db.Column(gino_db.Integer(), primary_key=True)
        admin_id = gino_db.Column(gino_db.Integer(), unique=True, nullable=False)

        def __str__(self) -> str:
            return f'<AdminTable {self.name}>'

        def __repr__(self) -> str:
            return f'<AdminTable {self.name}>'

    async def add_admin(self, admin_id: int) -> bool:
        if not await self.check_in_db_admin(admin_id):
            admin = self.AdminTable(admin_id=admin_id)
            await admin.create()
            return True
        else:
            return False

    async def check_in_db_admin(self, admin_id: int) -> bool:
        return not await self.AdminTable.query.where(self.AdminTable.admin_id == admin_id).gino.first() is None

    async def remove_admin(self, admin_id: int) -> bool:
        if not await self.check_in_db_admin(admin_id):
            return False
        admin = await self.AdminTable.query.where(self.AdminTable.admin_id == admin_id).gino.first()
        await admin.delete()
        return True

from tgbot.config import gino_db
from .base import Base


class Discount(Base):
    class DiscountTable(gino_db.Model):
        __tablename__ = 'discount'

        id = gino_db.Column(gino_db.Integer(), primary_key=True)
        code = gino_db.Column(gino_db.String(), unique=True, nullable=False)
        percent = gino_db.Column(gino_db.Integer(), nullable=False)

        def __str__(self) -> str:
            return f'<Discount {self.code}>'

        def __repr__(self) -> str:
            return f'<Discount {self.code}>'

    async def add_discount(self, code: str, percent: int) -> bool:
        if not await self.check_in_db_discount(code):
            group = self.DiscountTable(code=code, percent=percent)
            await group.create()
            return True
        else:
            return False

    async def check_in_db_discount(self, code: str) -> bool:
        return not await self.DiscountTable.query.where(self.DiscountTable.code == code).gino.first() is None

    async def get_all_discount(self) -> list[DiscountTable]:
        return await self.DiscountTable.query.gino.all()

    async def get_discount(self, code: str) -> DiscountTable:
        return await self.DiscountTable.query.where(self.DiscountTable.code == code).gino.first()

    async def get_discount_by_id(self, discount_id: int) -> DiscountTable:
        return await self.DiscountTable.query.where(self.DiscountTable.id == discount_id).gino.first()

    async def delete_discount(self, code: str) -> bool:
        if await self.check_in_db_discount(code):
            discount = await self.DiscountTable.query.where(self.DiscountTable.code == code).gino.first()
            await discount.delete()
            return True
        return False

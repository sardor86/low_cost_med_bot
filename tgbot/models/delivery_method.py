from tgbot.config import gino_db
from .base import Base


class DeliveryMethod(Base):
    class DeliveryMethodTable(gino_db.Model):
        __tablename__ = 'delivery_method'

        id = gino_db.Column(gino_db.Integer(), primary_key=True)
        name = gino_db.Column(gino_db.String(), unique=True, nullable=False)
        price = gino_db.Column(gino_db.Integer(), nullable=False)

        def __str__(self) -> str:
            return f'<DeliveryMethodTable {self.name}>'

        def __repr__(self) -> str:
            return f'<DeliveryMethodTable {self.name}>'

    async def add_delivery_method(self, name: str, price: int) -> bool:
        if not await self.check_in_db_delivery_method(name):
            delivery_method = self.DeliveryMethodTable(name=name, price=price)
            await delivery_method.create()
            return True
        else:
            return False

    async def check_in_db_delivery_method(self, name: str) -> bool:
        result = await self.DeliveryMethodTable.query.where(self.DeliveryMethodTable.name == name).gino.first() is None
        return not result

    async def get_all_delivery_method(self) -> list[DeliveryMethodTable]:
        return await self.DeliveryMethodTable.query.gino.all()

    async def get_delivery_method(self, name: str) -> DeliveryMethodTable:
        return await self.DeliveryMethodTable.query.where(self.DeliveryMethodTable.code == name).gino.first()

    async def delete_delivery_method(self, name: str) -> bool:
        if not await self.check_in_db_delivery_method(name):
            return False
        delivery_method = await self.DeliveryMethodTable.query.where(self.DeliveryMethodTable.name == name).gino.first()
        await delivery_method.delete()
        return True

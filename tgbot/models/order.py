from tgbot.config import gino_db
from .base import Base


class Order(Base):
    class OrderTable(gino_db.Model):
        __tablename__ = 'order'

        id = gino_db.Column(gino_db.Integer(), primary_key=True)
        product = gino_db.Column(gino_db.ForeignKey('products.id'), nullable=False)
        user = gino_db.Column(gino_db.ForeignKey('users.user_id'), nullable=False)
        quantity = gino_db.Column(gino_db.Integer(), nullable=False)
        discount = gino_db.Column(gino_db.ForeignKey('discount.id'), nullable=True)
        delivery_method = gino_db.Column(gino_db.ForeignKey('delivery_method.id'), nullable=True)
        address = gino_db.Column(gino_db.String(), nullable=True)
        confirmation = gino_db.Column(gino_db.Boolean(), default=False)

        def __str__(self) -> str:
            return f'<Basket {self.product}:{self.user}>'

        def __repr__(self) -> str:
            return f'<Basket {self.product}:{self.user}>'

    async def add_order(self, product_id: int,
                        user_id: int,
                        quantity: int,
                        discount_id: int | None,
                        delivery_method_id: int | None,
                        address: str | None) -> OrderTable:
        if not await self.check_in_db_order(product_id, user_id):
            order = self.OrderTable(product=product_id,
                                    user=user_id,
                                    quantity=quantity,
                                    discount=discount_id,
                                    delivery_method=delivery_method_id,
                                    address=address)
            await order.create()
            return order
        else:
            return await self.get_order(product_id, user_id)

    async def check_in_db_order(self, product_id: int, user_id: int) -> bool:
        return not await self.OrderTable.query.where(self.OrderTable.product == product_id and
                                                     self.OrderTable.user == user_id).gino.first() is None

    async def get_all_orders(self, user_id) -> list[OrderTable]:
        return await self.OrderTable.query.where(self.OrderTable.user == user_id).gino.all()

    async def get_order(self, product_id, user_id) -> OrderTable:
        return await self.OrderTable.query.where(self.OrderTable.product == product_id and
                                                 self.OrderTable.user == user_id).gino.first()

    async def delete_order(self, product_id: int, user_id: int) -> bool:
        if await self.check_in_db_order(product_id, user_id):
            order = await self.OrderTable.query.where(self.OrderTable.product == product_id and
                                                      self.OrderTable.user == user_id).gino.first()
            await order.delete()
            return True
        return False

    async def delete_all_products(self, product_id):
        product_list = await self.OrderTable.query.where(self.OrderTable.product == product_id).gino.all()
        for product in product_list:
            await product.delete()

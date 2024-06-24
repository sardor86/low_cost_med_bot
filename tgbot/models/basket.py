from tgbot.config import gino_db
from .base import Base


class Basket(Base):
    class BasketTable(gino_db.Model):
        __tablename__ = 'basket'

        id = gino_db.Column(gino_db.Integer(), primary_key=True)
        product = gino_db.Column(gino_db.ForeignKey('products.id'), nullable=False)
        user = gino_db.Column(gino_db.ForeignKey('users.user_id'), nullable=False)
        quantity = gino_db.Column(gino_db.Integer(), nullable=False)

        def __str__(self) -> str:
            return f'<Basket {self.product}:{self.user}>'

        def __repr__(self) -> str:
            return f'<Basket {self.product}:{self.user}>'

    async def add_basket(self, product_id: int, user_id: int, quantity: int) -> bool:
        if not await self.check_in_db_basket(product_id, user_id):
            basket = self.BasketTable(product=product_id,
                                      user=user_id,
                                      quantity=quantity)
            await basket.create()
            return True
        else:
            return False

    async def check_in_db_basket(self, product_id: int, user_id: int) -> bool:
        return not (await self.BasketTable.query.where(self.BasketTable.product == product_id).
                    where(self.BasketTable.user == user_id).gino.first() is None)

    async def get_all_products(self, user_id) -> list[BasketTable]:
        return await self.BasketTable.query.where(self.BasketTable.user == user_id).gino.all()

    async def get_basket(self, product_id, user_id) -> BasketTable:
        return await (self.BasketTable.query.where(self.BasketTable.product == product_id).
                      where(self.BasketTable.user == user_id).gino.first())

    async def delete_basket(self, product_id: int, user_id: int) -> bool:
        if await self.check_in_db_basket(product_id, user_id):
            basket = await (self.BasketTable.query.where(self.BasketTable.product == product_id).
                            where(self.BasketTable.user == user_id).gino.first())
            await basket.delete()
            return True
        return False

    async def delete_all_products(self, product_id):
        product_list = await self.BasketTable.query.where(self.BasketTable.product == product_id).gino.all()
        for product in product_list:
            await product.delete()

    async def change_basket(self, product_id: int, user_id: int, quantity: int) -> bool:
        if await self.check_in_db_basket(product_id, user_id):
            basket = await (self.BasketTable.query.where(self.BasketTable.product == product_id).
                            where(self.BasketTable.user == user_id).gino.first())
            await basket.update(quantity=basket.quantity + quantity).apply()
            return True
        return False

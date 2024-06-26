from tgbot.config import gino_db
from .order import Order
from .base import Base
from .basket import Basket


class Products(Base):
    class ProductsTable(gino_db.Model):
        __tablename__ = 'products'

        id = gino_db.Column(gino_db.Integer(), primary_key=True)
        group_id = gino_db.Column(gino_db.ForeignKey('group.id'), nullable=False)
        name = gino_db.Column(gino_db.String(), nullable=False, unique=True)
        description = gino_db.Column(gino_db.String(), nullable=False)
        price = gino_db.Column(gino_db.Float(), nullable=False)
        image = gino_db.Column(gino_db.String(), nullable=False)

        def __str__(self) -> str:
            return f'<Product {self.group_name}>'

        def __repr__(self) -> str:
            return f'<Product {self.group_name}>'

    async def add_product(self,
                          group_id: int,
                          name: str,
                          description: str,
                          price: int,
                          image: str) -> bool:
        if not await self.check_in_db_product(name):
            product = self.ProductsTable(group_id=group_id,
                                         name=name,
                                         description=description,
                                         price=price,
                                         image=image)
            await product.create()
            return True
        else:
            return False

    async def check_in_db_product(self, product_name: str) -> bool:
        return not await self.ProductsTable.query.where(self.ProductsTable.name == product_name).gino.first() is None

    async def get_all_products_by_group(self, group_id: int) -> list[ProductsTable]:
        return await self.ProductsTable.query.where(self.ProductsTable.group_id == group_id).gino.all()

    async def get_product_by_name(self, name: str) -> ProductsTable:
        return await self.ProductsTable.query.where(self.ProductsTable.name == name).gino.first()

    async def get_product_by_id(self, product_id: int) -> ProductsTable:
        return await self.ProductsTable.query.where(self.ProductsTable.id == product_id).gino.first()

    async def get_all_products(self) -> list[ProductsTable]:
        return await self.ProductsTable.query.gino.all()

    async def delete_product(self, product_name: str) -> bool:
        if await self.check_in_db_product(product_name):
            product = await self.ProductsTable.query.where(self.ProductsTable.name == product_name).gino.first()
            await Basket().delete_all_products(product.id)
            await Order().delete_all_products(product.id)
            await product.delete()
            return True
        return False

    async def edit_product(self,
                           product_name: str,
                           name: str = None,
                           description: str = None,
                           price: int = None,
                           image: str = None):
        product = await self.ProductsTable.query.where(self.ProductsTable.name == product_name).gino.first()

        if name:
            await product.update(name=name).apply()
        elif description:
            await product.update(description=description).apply()
        elif price:
            await product.update(price=price).apply()
        elif image:
            await product.update(image=image).apply()

from tgbot.config import gino_db
from .base import Base


class ReviewProduct(Base):
    class ReviewProductTable(gino_db.Model):
        __tablename__ = 'review_product'

        id = gino_db.Column(gino_db.Integer(), primary_key=True)
        review = gino_db.Column(gino_db.ForeignKey('review.id'), nullable=False)
        product = gino_db.Column(gino_db.ForeignKey('products.id'), nullable=False)

        def __str__(self) -> str:
            return f'<ReviewProduct {self.product}:{self.review}>'

        def __repr__(self) -> str:
            return f'<ReviewProduct {self.product}:{self.review}>'

    async def add_review(self, review: int, product: int):
        reviews = self.ReviewProductTable(review=review, product=product)
        await reviews.create()

    async def get_all_reviews(self, product: int) -> list[ReviewProductTable]:
        return await self.ReviewProductTable.query.where(self.ReviewProductTable.product == product).gino.all()

    async def delete_review(self, product: int):
        reviews_list = self.ReviewProductTable.query.where(self.ReviewProductTable.product == product).gino.all()
        for review in reviews_list:
            await review.delete()

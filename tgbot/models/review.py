from datetime import datetime

from tgbot.config import gino_db
from .base import Base


class Review(Base):
    class ReviewTable(gino_db.Model):
        __tablename__ = 'review'

        id = gino_db.Column(gino_db.Integer(), primary_key=True)
        user = gino_db.Column(gino_db.ForeignKey('users.user_id'), nullable=False)
        stars = gino_db.Column(gino_db.Integer(), nullable=False)
        date = gino_db.Column(gino_db.String(), nullable=False)
        price = gino_db.Column(gino_db.Integer(), nullable=False)
        text = gino_db.Column(gino_db.String(), nullable=True)

        def __str__(self) -> str:
            return f'<Review {self.user}:{self.text}>'

        def __repr__(self) -> str:
            return f'<Review {self.user}:{self.text}>'

    async def add_review(self, user: int, stars: int, price: int, text: str) -> ReviewTable:
        date = datetime.today().date().strftime('%Y-%m-%d')
        review = self.ReviewTable(user=user, stars=stars, date=date, price=price, text=text)
        await review.create()
        return review

    async def get_all_reviews(self) -> list[ReviewTable]:
        return await self.ReviewTable.query.gino.all()

    async def get_review(self, review_id: int) -> ReviewTable:
        return await self.ReviewTable.query.where(self.ReviewTable.id == review_id).gino.first()

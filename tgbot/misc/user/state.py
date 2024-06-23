from aiogram.fsm.state import State, StatesGroup


class SetSecretPhrase(StatesGroup):
    secret_phrase = State()


class ListingState(StatesGroup):
    choice_group = State()
    show_product = State()


class ProductState(StatesGroup):
    product = State()


class BasketState(StatesGroup):
    basket = State()


class CheckoutState(StatesGroup):
    checkout = State()
    discount = State()
    payment = State()
    delivery_address = State()
    delivery_method = State()


class DiscussionState(StatesGroup):
    discussion = State()


class ReviewState(StatesGroup):
    review = State()
    review_text = State()

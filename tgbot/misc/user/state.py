from aiogram.fsm.state import State, StatesGroup


class SetSecretPhrase(StatesGroup):
    secret_phrase = State()


class ListingState(StatesGroup):
    choice_group = State()
    show_product = State()


class ProductState(StatesGroup):
    product = State()

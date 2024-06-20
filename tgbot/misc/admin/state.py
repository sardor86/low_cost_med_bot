from aiogram.fsm.state import State, StatesGroup


class AddGroup(StatesGroup):
    group_name = State()


class DeleteGroup(StatesGroup):
    chose_group = State()


class ShowProducts(StatesGroup):
    chose_group = State()


class AddProduct(StatesGroup):
    chose_group = State()
    name = State()
    description = State()
    price = State()
    image = State()

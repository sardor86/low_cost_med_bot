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


class DeleteProduct(StatesGroup):
    chose_group = State()
    chose_product = State()


class EditProductState(StatesGroup):
    chose_group = State()
    chose_product = State()
    edit_information = State()
    edit_product = State()


class AddDiscount(StatesGroup):
    code = State()
    percent = State()


class DeleteDiscount(StatesGroup):
    code = State()


class AddDeliveryMethod(StatesGroup):
    name = State()
    price = State()


class DeleteDeliveryMethod(StatesGroup):
    name = State()


class DiscussionState(StatesGroup):
    discussion = State()

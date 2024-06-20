from aiogram.fsm.state import State, StatesGroup


class AddGroup(StatesGroup):
    group_name = State()


class DeleteGroup(StatesGroup):
    chose_group = State()

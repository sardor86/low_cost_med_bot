from aiogram.fsm.state import State, StatesGroup


class SetSecretPhrase(StatesGroup):
    secret_phrase = State()

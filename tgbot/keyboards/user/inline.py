from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


def get_register_inline_keyboard():
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text='Set your own secret phrase', callback_data='set_secret_phrase'))
    keyboard.row(InlineKeyboardButton(text='About secret phrase', callback_data='about_secret_phrase'))

    return keyboard


def understand_secret_phrase_inline_keyboard():
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text='I understand', callback_data='understand_secret_phrase'))

    return keyboard


def about_secret_phrase_inline_keyboard():
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text='About secret phrase', callback_data='about_secret_phrase'))

    return keyboard

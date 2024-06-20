from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


def get_register_inline_keyboard() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text='Set your own secret phrase', callback_data='set_secret_phrase'))
    keyboard.row(InlineKeyboardButton(text='About secret phrase', callback_data='about_secret_phrase'))

    return keyboard


def understand_secret_phrase_inline_keyboard() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text='I understand', callback_data='understand_secret_phrase'))

    return keyboard


def about_secret_phrase_inline_keyboard() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text='About secret phrase', callback_data='about_secret_phrase'))

    return keyboard


def user_menu_inline_keyboard() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text='Listings', callback_data='listings'))
    keyboard.row(InlineKeyboardButton(text='About', callback_data='about'))
    keyboard.row(InlineKeyboardButton(text='Rating', callback_data='rating'),
                 InlineKeyboardButton(text='PGP', callback_data='secret_key'))
    keyboard.row(InlineKeyboardButton(text='Orders', callback_data='orders'),
                 InlineKeyboardButton(text='basket', callback_data='basket'))
    keyboard.row(InlineKeyboardButton(text='Contact', callback_data='contact'))

    return keyboard


def back_to_menu_inline_keyboard() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text='Menu', callback_data='menu'))

    return keyboard

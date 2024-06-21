from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


def get_choice_group_inline_keyboard(groups_list: list[str]) -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    for group in groups_list:
        keyboard.row(InlineKeyboardButton(text=group, callback_data=f'{group}'))

    return keyboard


def get_choice_product_inline_keyboard(product_list: list[str]) -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    for product in product_list:
        keyboard.row(InlineKeyboardButton(text=product, callback_data=f'{product}'))

    return keyboard

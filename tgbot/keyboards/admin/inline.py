from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


def get_menu_inline_keyboard() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text='groups', callback_data='admin_group'))
    keyboard.row(InlineKeyboardButton(text='products', callback_data='admin_products'))

    return keyboard


def get_group_menu_inline_keyboard() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text='show all groups', callback_data='show_all_groups'))
    keyboard.row(InlineKeyboardButton(text='add group', callback_data='add_group'))
    keyboard.row(InlineKeyboardButton(text='delete group', callback_data='delete_group'))
    keyboard.row(InlineKeyboardButton(text='Admin panel', callback_data='admin_panel'))

    return keyboard


def get_choose_group_inline_keyboard(groups_list: list[str]) -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    for group in groups_list:
        keyboard.row(InlineKeyboardButton(text=group, callback_data=f'{group}'))

    return keyboard


def get_product_menu_inline_keyboard() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text='show all products', callback_data='show_all_products'))
    keyboard.row(InlineKeyboardButton(text='add product', callback_data='add_product'))
    keyboard.row(InlineKeyboardButton(text='delete product', callback_data='delete_product'))
    keyboard.row(InlineKeyboardButton(text='Admin panel', callback_data='admin_panel'))

    return keyboard

from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from tgbot.models import Discount, DeliveryMethod


def get_menu_inline_keyboard() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text='groups', callback_data='admin_group'))
    keyboard.row(InlineKeyboardButton(text='products', callback_data='admin_products'))
    keyboard.row(InlineKeyboardButton(text='discount', callback_data='admin_discount'))
    keyboard.row(InlineKeyboardButton(text='delivery method', callback_data='admin_delivery'))

    return keyboard


def get_group_menu_inline_keyboard() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text='show all groups', callback_data='show_all_groups'))
    keyboard.row(InlineKeyboardButton(text='add group', callback_data='add_group'))
    keyboard.row(InlineKeyboardButton(text='delete group', callback_data='delete_group'))
    keyboard.row(InlineKeyboardButton(text='Admin panel', callback_data='admin_panel'))

    return keyboard


def get_product_menu_inline_keyboard() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text='show all products', callback_data='show_all_products'))
    keyboard.row(InlineKeyboardButton(text='add product', callback_data='add_product'))
    keyboard.row(InlineKeyboardButton(text='edit product', callback_data='edit_product'))
    keyboard.row(InlineKeyboardButton(text='delete product', callback_data='delete_product'))
    keyboard.row(InlineKeyboardButton(text='Admin panel', callback_data='admin_panel'))

    return keyboard


def get_choice_edit_information_product_keyboard() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text='name', callback_data='name'))
    keyboard.row(InlineKeyboardButton(text='description', callback_data='description'))
    keyboard.row(InlineKeyboardButton(text='price', callback_data='price'))
    keyboard.row(InlineKeyboardButton(text='image', callback_data='image'))

    return keyboard


def get_discount_menu_inline_keyboard() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text='show all codes', callback_data='show_all_discount'))
    keyboard.row(InlineKeyboardButton(text='add code', callback_data='add_discount'))
    keyboard.row(InlineKeyboardButton(text='delete code', callback_data='delete_discount'))
    keyboard.row(InlineKeyboardButton(text='Admin panel', callback_data='admin_panel'))

    return keyboard


def get_choice_discount(discount_list: list[Discount.DiscountTable]) -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    for discount in discount_list:
        keyboard.row(InlineKeyboardButton(text=discount.code, callback_data=f'{discount.code}'))

    return keyboard


def get_delivery_menu_inline_keyboard() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text='show all delivery method', callback_data='show_all_delivery_method'))
    keyboard.row(InlineKeyboardButton(text='add delivery method', callback_data='add_delivery_method'))
    keyboard.row(InlineKeyboardButton(text='delete delivery method', callback_data='delete_delivery_method'))
    keyboard.row(InlineKeyboardButton(text='Admin panel', callback_data='admin_panel'))

    return keyboard


def get_choice_delivery(delivery_method_list: list[DeliveryMethod.DeliveryMethodTable]) -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    for delivery_method in delivery_method_list:
        keyboard.row(InlineKeyboardButton(text=delivery_method.name, callback_data=f'{delivery_method.name}'))

    return keyboard

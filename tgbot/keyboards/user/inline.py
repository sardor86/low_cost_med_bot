from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from tgbot.models import Basket, Products


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


def product_menu_inline_keyboard(quantity: int, price: int, basket: int) -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text='+1.00', callback_data='+product'),
                 InlineKeyboardButton(text=f'🛒 {basket * price}', callback_data='basket'),
                 InlineKeyboardButton(text='-1.00', callback_data='-product'))
    keyboard.row(InlineKeyboardButton(text=f'Add to Cart {quantity} pcs[£{quantity * price}]',
                                      callback_data='add_to_cart'))
    keyboard.row(InlineKeyboardButton(text=f'135 reviews for this product', callback_data='reviews'))
    keyboard.row(InlineKeyboardButton(text='Menu', callback_data='menu'))

    return keyboard


async def get_basket_menu(basket_list: list[Basket.BasketTable]) -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    product_model = Products()

    for basket in basket_list:
        product = await product_model.get_product_by_id(basket.product)
        keyboard.row(InlineKeyboardButton(text=f'{product.name} '
                                               f'{basket.quantity} pcs - '
                                               f'£{basket.quantity * product.price}',
                                          callback_data=f'{product.id}.delete'))
    keyboard.row(InlineKeyboardButton(text='Menu', callback_data='menu'),
                 InlineKeyboardButton(text='Checkout', callback_data='checkout'))

    return keyboard

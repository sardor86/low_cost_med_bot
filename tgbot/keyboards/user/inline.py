from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from tgbot.models import Basket, Products, DeliveryMethod


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


def user_menu_inline_keyboard(price: int) -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text='💊 Listings', callback_data='listings'))
    keyboard.row(InlineKeyboardButton(text='About', callback_data='about'))
    keyboard.row(InlineKeyboardButton(text='📈 Rating', callback_data='rating'),
                 InlineKeyboardButton(text='📦 Orders', callback_data='orders'),
                 InlineKeyboardButton(text='🔑 PGP', callback_data='secret_key'))
    keyboard.row(InlineKeyboardButton(text=f'🛒 £{price}', callback_data='basket'))
    keyboard.row(InlineKeyboardButton(text='📭 Contact', callback_data='contact'))

    return keyboard


def back_to_menu_inline_keyboard() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text='Menu', callback_data='menu'))

    return keyboard


def product_menu_inline_keyboard(quantity: int, price: int, basket: int, review_len: int) -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text='+1.00', callback_data='+product'),
                 InlineKeyboardButton(text=f'🛒 {basket * price}', callback_data='basket'),
                 InlineKeyboardButton(text='-1.00', callback_data='-product'))
    keyboard.row(InlineKeyboardButton(text=f'Enter Quantity Manually', callback_data='quantity_manually'))
    keyboard.row(InlineKeyboardButton(text=f'Add to Cart {quantity} pcs[£{quantity * price}]',
                                      callback_data='add_to_cart'))
    keyboard.row(InlineKeyboardButton(text=f'{review_len} reviews for this product', callback_data='listing_reviews'))
    keyboard.row(InlineKeyboardButton(text='Back', callback_data='listing_back'))

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


def checkout_menu_inline_keyboard(discount_code: bool | None = None,
                                  delivery_address: bool | None = None,
                                  delivery_method: bool | None = None,
                                  payment_method: bool | None = None) -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    if discount_code:
        keyboard.row(InlineKeyboardButton(text='✅Enter a discount code', callback_data='checkout_discount'))
    else:
        keyboard.row(InlineKeyboardButton(text='Enter a discount code', callback_data='checkout_discount'))
    if delivery_address:
        keyboard.row(InlineKeyboardButton(text='✅Enter Delivery Address', callback_data='checkout_address'))
    else:
        keyboard.row(InlineKeyboardButton(text='Enter Delivery Address', callback_data='checkout_address'))
    if delivery_method:
        keyboard.row(InlineKeyboardButton(text='✅Enter Delivery Method', callback_data='checkout_delivery_method'))
    else:
        keyboard.row(InlineKeyboardButton(text='Enter Delivery Method', callback_data='checkout_delivery_method'))
    if payment_method:
        keyboard.row(InlineKeyboardButton(text='✅Enter Payment Method', callback_data='checkout_payment_method'))
    else:
        keyboard.row(InlineKeyboardButton(text='Enter Payment Method', callback_data='checkout_payment_method'))

    if delivery_method and delivery_address and payment_method:
        keyboard.row(InlineKeyboardButton(text='Checkout', callback_data='checkout_payment'))

    keyboard.row(InlineKeyboardButton(text='Delete Order', callback_data='checkout_delete'))

    return keyboard


def checkout_cancellation_inline_keyboard() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text='cancel', callback_data='checkout_cancel'))

    return keyboard


def get_choice_delivery(delivery_method_list: list[DeliveryMethod.DeliveryMethodTable]) -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    for delivery_method in delivery_method_list:
        keyboard.row(InlineKeyboardButton(text=f'{delivery_method.name} - {delivery_method.price}',
                                          callback_data=f'{delivery_method.name}'))

    keyboard.row(InlineKeyboardButton(text='cancel', callback_data='checkout_cancel'))

    return keyboard


def get_choice_payment_method_inline_keyboard() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text='USDT', callback_data='USDT'),
                 InlineKeyboardButton(text='USDC', callback_data='USDC'),
                 InlineKeyboardButton(text='BTC', callback_data='BTC'))
    keyboard.row(InlineKeyboardButton(text='ETH', callback_data='ETH'),
                 InlineKeyboardButton(text='TON', callback_data='TON'),
                 InlineKeyboardButton(text='BNB', callback_data='BNB'))

    keyboard.row(InlineKeyboardButton(text='cancel', callback_data='checkout_cancel'))

    return keyboard


def checkout_address_menu_inline_keyboard() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text='Why is it safe?', callback_data='checkout_about'))
    keyboard.row(InlineKeyboardButton(text='Vendor PGP key', callback_data='vendor_secret_key'))
    keyboard.row(InlineKeyboardButton(text='cancel', callback_data='checkout_cancel'))

    return keyboard


def checkout_payment_inline_keyboard(payment_url) -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text='Pay', url=payment_url),
                 InlineKeyboardButton(text='Check payment', callback_data='checkout_checkout_payment'))

    return keyboard


def delete_message_inline_keyboard() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text='Delete Message', callback_data='delete_message'))

    return keyboard


def discussion_menu_inline_keyboard() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text='Vendor PGP key', callback_data='vendor_secret_key'))
    keyboard.row(InlineKeyboardButton(text='Close', callback_data='close_discussion'))

    return keyboard


def discussion_cancel_inline_keyboard() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text='Reopen the chat', callback_data='contact'))
    keyboard.row(InlineKeyboardButton(text='History of dialogue', callback_data='discussion_history'))
    keyboard.row(InlineKeyboardButton(text='Menu', callback_data='menu'))

    return keyboard


def review_menu_inline_keyboard(stars: int = 5) -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()
    keyboard_star_list = []
    for star_number in range(5):
        if star_number <= stars:
            keyboard_star_list.append(InlineKeyboardButton(text='★', callback_data=f'review_star_{star_number}'))
            continue
        keyboard_star_list.append(InlineKeyboardButton(text='☆', callback_data=f'review_star_{star_number}'))
    keyboard.row(*keyboard_star_list)
    keyboard.row(InlineKeyboardButton(text='Write comment', callback_data='review_comment'))
    keyboard.row(InlineKeyboardButton(text='Save', callback_data='review_save'))

    return keyboard


def cancel_listing_quantity_manually_inline_keyboard() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text='Cancel', callback_data='cancel_listing_quantity_manually'))

    return keyboard

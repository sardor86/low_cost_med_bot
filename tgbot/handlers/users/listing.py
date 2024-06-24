from aiogram import Dispatcher
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, BufferedInputFile

from tgbot.models import Groups, Products, Basket, ReviewProduct, Review
from tgbot.misc.user import ListingState, ProductState
from tgbot.keyboards import get_choice_group_inline_keyboard, get_choice_product_inline_keyboard
from tgbot.keyboards.user import (product_menu_inline_keyboard,
                                  delete_message_inline_keyboard,
                                  cancel_listing_quantity_manually_inline_keyboard)


async def list_of_group(callback: CallbackQuery, state: FSMContext):
    groups_list = await Groups().get_all_groups()

    basket_list = await Basket().get_all_products(callback.from_user.id)
    product_model = Products()

    basket_price = 0

    for basket in basket_list:
        basket_price += (await product_model.get_product_by_id(basket.product)).price

    groups_list_keyboard = get_choice_group_inline_keyboard(groups_list)
    groups_list_keyboard.row(InlineKeyboardButton(text='Back', callback_data='menu'),
                             InlineKeyboardButton(text='Price List', callback_data='price_list'),
                             InlineKeyboardButton(text=f'🛒 £{basket_price}', callback_data='basket'))
    await callback.message.edit_text('Select a product category to fill your shopping basket',
                                     reply_markup=groups_list_keyboard.as_markup())
    await state.set_state(ListingState.choice_group)


async def price_list(callback: CallbackQuery):
    products_list = await Products().get_all_products()

    file_text = ''

    for product in products_list:
        file_text += f'\n{product.name}\n'
        file_text += f'price: £{product.price}\n\n-------------------------'

    await callback.bot.send_document(callback.from_user.id,
                                     BufferedInputFile(bytes(file_text, 'utf-8'), 'Price List.txt'),
                                     reply_markup=delete_message_inline_keyboard().as_markup())


async def show_product_list(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    data = await state.get_data()
    if 'group' in data:
        group = data['group']
    else:
        group = await Groups().get_group(callback.data)
        await state.update_data(group=group)
    product_list = [product.name for product in await Products().get_all_products_by_group(group_id=group.id)]

    basket_list = await Basket().get_all_products(callback.from_user.id)
    product_model = Products()

    basket_price = 0

    for basket in basket_list:
        basket_price += (await product_model.get_product_by_id(basket.product)).price

    product_list_keyboard = get_choice_product_inline_keyboard(product_list)

    product_list_keyboard.row(InlineKeyboardButton(text='Back', callback_data='listing_back'),
                              InlineKeyboardButton(text=f'🛒 £{basket_price}', callback_data='basket'))

    await callback.bot.send_message(callback.from_user.id,
                                    f'Category: {group.group_name}',
                                    reply_markup=product_list_keyboard.as_markup())
    await state.set_state(ListingState.show_product)


async def listing_back(callback: CallbackQuery, state: FSMContext):
    state_name = await state.get_state()
    if state_name == 'ListingState:show_product':
        await list_of_group(callback, state)
        return
    elif state_name == 'ProductState:product':
        await show_product_list(callback, state)


async def product_details(callback: CallbackQuery, data: dict):
    basket_model = Basket()
    if await basket_model.check_in_db_basket(product_id=data['product'].id, user_id=callback.from_user.id):
        basket = await Basket().get_basket(product_id=data['product'].id, user_id=callback.from_user.id)
        basket = basket.quantity
    else:
        basket = 0
    await callback.message.delete()

    all_review = await ReviewProduct().get_all_reviews(data['product'].id)
    review_model = Review()
    review_middle = 0
    for review in all_review:
        review_middle += (await review_model.get_review(review.review)).stars + 1

    await callback.bot.send_photo(callback.message.chat.id,
                                  caption=f'{data["product"].name}\n'
                                          f'{data["group"].group_name} • Stock Unlimited • ★ '
                                          f'{review_middle / len(all_review)} ({len(all_review)})\n\n'
                                          f'{data["product"].description}\n\n'
                                          f'price: £{data["product"].price} for 1 pcs',
                                  photo=data['product'].image,
                                  reply_markup=product_menu_inline_keyboard(data['quantity'],
                                                                            data['product'].price,
                                                                            basket,
                                                                            len(all_review)).as_markup())


async def show_product_details(callback: CallbackQuery, state: FSMContext):
    product_name = callback.data
    product = await Products().get_product_by_name(product_name)
    group = (await state.get_data())['group']
    await state.clear()

    await state.set_state(ProductState.product)
    await state.update_data(product=product,
                            quantity=1,
                            group=group)
    data = {
        'product': product,
        'group': group,
        'quantity': 1,
    }
    await product_details(callback, data)


async def add_quantity_product(callback: CallbackQuery, state: FSMContext):
    product_data = await state.get_data()
    await state.update_data(quantity=product_data['quantity'] + 1)
    await product_details(callback, product_data)


async def delete_quantity_product(callback: CallbackQuery, state: FSMContext):
    product_data = await state.get_data()
    if product_data['quantity'] != 1:
        await state.update_data(quantity=product_data['quantity'] - 1)
    await product_details(callback, product_data)


async def add_to_basket(callback: CallbackQuery, state: FSMContext):
    product_data = await state.get_data()
    basket_model = Basket()
    if await basket_model.check_in_db_basket(product_id=product_data['product'].id,
                                             user_id=callback.from_user.id):
        await basket_model.change_basket(product_id=product_data['product'].id,
                                         user_id=callback.from_user.id,
                                         quantity=product_data['quantity'])
    else:
        await basket_model.add_basket(product_id=product_data['product'].id,
                                      user_id=callback.from_user.id,
                                      quantity=product_data['quantity'])
    await state.update_data(quantity=1)
    await product_details(callback, product_data)


async def get_rating(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    message_text = 'Reviews \n\n'
    all_review = await ReviewProduct().get_all_reviews(data['product'].id)
    review_model = Review()
    for product_review in all_review:
        review = await review_model.get_review(product_review.review)
        message_text += f'{review.date} '
        for star_number in range(5):
            if star_number <= review.stars:
                message_text += '★'
            else:
                message_text += '☆'
        message_text += f' — £{review.price}\n{review.text}\n\n'
    await callback.message.reply(message_text)


async def enter_quantity_manually(callback: CallbackQuery, state: FSMContext):
    await callback.message.reply('Send the quantity of the product you want to add to the shopping '
                                 'basket in the chat. The minimum quantity is 1.00 pcs.',
                                 reply_markup=cancel_listing_quantity_manually_inline_keyboard().as_markup())
    await state.update_data(callback=callback)
    await state.set_state(ListingState.quantity_manually)


async def get_quantity_manually(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.reply('Try again, There is not number')
        return
    if int(message.text) <= 0:
        await message.reply('Try again, There is not valid pcs')
        return

    product_data = await state.get_data()
    await state.update_data(quantity=int(message.text))
    await product_details(product_data['callback'], product_data)
    await state.set_state(ProductState.product)


async def cancel_quantity_manually(callback: CallbackQuery, state: FSMContext):
    await product_details(callback, await state.get_data())
    await state.set_state(ProductState.product)


def register_listing_handlers(dp: Dispatcher):
    dp.callback_query.register(list_of_group, lambda callback: callback.data == 'listings')
    dp.callback_query.register(price_list, lambda callback: callback.data == 'price_list')
    dp.callback_query.register(listing_back, lambda callback: callback.data == 'listing_back')
    dp.callback_query.register(show_product_list, StateFilter(ListingState.choice_group))
    dp.callback_query.register(show_product_details, StateFilter(ListingState.show_product))
    dp.callback_query.register(add_quantity_product, StateFilter(ProductState.product),
                               lambda callback: callback.data == '+product')
    dp.callback_query.register(delete_quantity_product, StateFilter(ProductState.product),
                               lambda callback: callback.data == '-product')
    dp.callback_query.register(add_to_basket, StateFilter(ProductState.product),
                               lambda callback: callback.data == 'add_to_cart')
    dp.callback_query.register(get_rating,
                               StateFilter(ProductState.product),
                               lambda callback: callback.data == 'listing_reviews')
    dp.callback_query.register(cancel_quantity_manually,
                               lambda callback: callback.data == 'cancel_listing_quantity_manually')
    dp.callback_query.register(enter_quantity_manually, lambda callback: callback.data == 'quantity_manually')
    dp.message.register(get_quantity_manually, StateFilter(ListingState.quantity_manually))

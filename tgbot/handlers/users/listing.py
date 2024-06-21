from aiogram import Dispatcher
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from tgbot.models import Groups, Products
from tgbot.misc.user import ListingState, ProductState
from tgbot.keyboards import get_choice_group_inline_keyboard, get_choice_product_inline_keyboard
from tgbot.keyboards.user import product_menu_inline_keyboard


async def list_of_group(callback: CallbackQuery, state: FSMContext):
    groups_list = await Groups().get_all_groups()
    await callback.message.edit_text('Select a product category to fill your shopping basket',
                                     reply_markup=get_choice_group_inline_keyboard(groups_list).as_markup())
    await state.set_state(ListingState.choice_group)


async def show_product_list(callback: CallbackQuery, state: FSMContext):
    group = await Groups().get_group(callback.data)
    await state.update_data(group=group)
    product_list = [product.name for product in await Products().get_all_products_by_group(group_id=group.id)]
    await callback.message.edit_text(f'Category: {group.group_name}',
                                     reply_markup=get_choice_product_inline_keyboard(product_list).as_markup())
    await state.set_state(ListingState.show_product)


async def product_details(callback: CallbackQuery, data: dict):
    await callback.message.delete()
    await callback.bot.send_photo(callback.message.chat.id,
                                  caption=f'{data["product"].name}\n'
                                          f'{data["group"].group_name} • Stock Unlimited • ★ 5.0 (87)\n\n'
                                          f'{data["product"].description}\n\n'
                                          f'£{data["product"].price}',
                                  photo=data['product'].image,
                                  reply_markup=product_menu_inline_keyboard(data['quantity'],
                                                                            data['product'].price).as_markup())


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


def register_listing_handlers(dp: Dispatcher):
    dp.callback_query.register(list_of_group, lambda callback: callback.data == 'listings')
    dp.callback_query.register(show_product_list, StateFilter(ListingState.choice_group))
    dp.callback_query.register(show_product_details, StateFilter(ListingState.show_product))
    dp.callback_query.register(add_quantity_product, StateFilter(ProductState.product),
                               lambda callback: callback.data == '+product')
    dp.callback_query.register(delete_quantity_product, StateFilter(ProductState.product),
                               lambda callback: callback.data == '-product')

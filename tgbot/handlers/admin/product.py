import random

from aiogram import Dispatcher
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from tgbot.filters import AdminFilter
from tgbot.keyboards.admin import (get_product_menu_inline_keyboard,
                                   get_choose_group_inline_keyboard)
from tgbot.misc.admin import ShowProducts, AddProduct
from tgbot.models import Groups
from tgbot.models.products import Products


async def product_menu(callback: CallbackQuery):
    await callback.message.edit_text('Products', reply_markup=get_product_menu_inline_keyboard().as_markup())


async def start_show_product(callback: CallbackQuery, state: FSMContext):
    groups_list = await Groups().get_all_groups()
    await callback.message.edit_text('Choose name of group',
                                     reply_markup=get_choose_group_inline_keyboard(groups_list).as_markup())
    await state.set_state(ShowProducts.chose_group)


async def show_product(callback: CallbackQuery, state: FSMContext):
    group = await Groups().get_group(callback.data)
    product_list = await Products().get_all_products_by_group(group.id)
    text_string = 'Products:\n\n'
    for product in product_list:
        text_string += f'|{product.name}\n|'

    await callback.message.edit_text(text_string)
    await callback.message.reply('Products', reply_markup=get_product_menu_inline_keyboard().as_markup())
    await state.clear()


async def start_add_product(callback: CallbackQuery, state: FSMContext):
    groups_list = await Groups().get_all_groups()
    await callback.message.edit_text('Choose name of group',
                                     reply_markup=get_choose_group_inline_keyboard(groups_list).as_markup())
    await state.set_state(AddProduct.chose_group)


async def set_name_product(callback: CallbackQuery, state: FSMContext):
    group = await Groups().get_group(callback.data)
    await state.update_data(group=group)
    await callback.message.edit_text('Write name of product')
    await state.set_state(AddProduct.name)


async def set_description_product(message: Message, state: FSMContext):
    if await Products().check_in_db_product(message.text):
        await message.reply('Try again, this product is already exists')
        return

    await state.update_data(name=message.text)
    await message.reply('Write description of product')
    await state.set_state(AddProduct.description)


async def set_price_product(message: Message, state: FSMContext):
    await state.update_data(description=message.text)

    await message.reply('Write price of product')
    await state.set_state(AddProduct.price)


async def set_image_product(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.reply('Try again, there is not number')
        return

    await state.update_data(price=int(message.text))

    await message.reply('Send image of product')
    await state.set_state(AddProduct.image)


async def set_end_up_product(message: Message, state: FSMContext):
    if not message.photo:
        await message.reply('Try again, there is not photo')
        return
    photo = message.photo[-1].file_id
    data = await state.get_data()
    await Products().add_product(group_id=data['group'].id,
                                 name=data['name'],
                                 description=data['description'],
                                 price=data['price'],
                                 image=photo)

    await message.reply('Product added successfully')
    await state.clear()


def register_product_handler(dp: Dispatcher):
    dp.callback_query.register(product_menu, AdminFilter(), lambda callback: callback.data == 'admin_products')
    dp.callback_query.register(start_show_product, AdminFilter(), lambda callback: callback.data == 'show_all_products')
    dp.callback_query.register(show_product, AdminFilter(), StateFilter(ShowProducts.chose_group))
    dp.callback_query.register(start_add_product, AdminFilter(), lambda callback: callback.data == 'add_product')
    dp.callback_query.register(set_name_product, AdminFilter(), StateFilter(AddProduct.chose_group))
    dp.message.register(set_description_product, AdminFilter(), StateFilter(AddProduct.name))
    dp.message.register(set_price_product, AdminFilter(), StateFilter(AddProduct.description))
    dp.message.register(set_image_product, AdminFilter(), StateFilter(AddProduct.price))
    dp.message.register(set_end_up_product, AdminFilter(), StateFilter(AddProduct.image))

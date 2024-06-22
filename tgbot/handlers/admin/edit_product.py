from aiogram import Dispatcher
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from tgbot.filters import AdminFilter
from tgbot.keyboards.admin import get_choice_edit_information_product_keyboard, get_menu_inline_keyboard
from tgbot.keyboards import get_choice_group_inline_keyboard, get_choice_product_inline_keyboard
from tgbot.misc.admin import EditProductState
from tgbot.models import Groups
from tgbot.models import Products


async def choice_group(callback: CallbackQuery, state: FSMContext):
    groups_list = await Groups().get_all_groups()
    await callback.message.edit_text('Choice name of group',
                                     reply_markup=get_choice_group_inline_keyboard(groups_list).as_markup())
    await state.set_state(EditProductState.chose_group)


async def choice_product(callback: CallbackQuery, state: FSMContext):
    group = await Groups().get_group(callback.data)
    await state.update_data(group=group)

    product_list = [product.name for product in await Products().get_all_products_by_group(group_id=group.id)]
    await callback.message.edit_text('Choice product: ',
                                     reply_markup=get_choice_product_inline_keyboard(product_list).as_markup())
    await state.set_state(EditProductState.chose_product)


async def choice_edit_information(callback: CallbackQuery, state: FSMContext):
    product = await Products().get_product_by_name(callback.data)
    await state.update_data(product=product)

    await callback.message.edit_text('Choice: ',
                                     reply_markup=get_choice_edit_information_product_keyboard().as_markup())
    await state.set_state(EditProductState.edit_information)


async def edit_product(callback: CallbackQuery, state: FSMContext):
    await state.update_data(edit_information=callback.data)

    if callback.data == 'image':
        await callback.message.edit_text('Send a photo')
    else:
        await callback.message.edit_text('Write the value')

    await state.set_state(EditProductState.edit_product)


async def end_edit_product(message: Message, state: FSMContext):
    data = await state.get_data()

    product_model = Products()

    if data['edit_information'] == 'name':
        await product_model.edit_product(product_name=data['product'].name,
                                         name=message.text)
    elif data['edit_information'] == 'description':
        await product_model.edit_product(product_name=data['product'].name,
                                         description=message.text)
    elif data['edit_information'] == 'price':
        if not message.text.isdigit():
            await message.reply('Try again, there is not price')
            return

        await product_model.edit_product(product_name=data['product'].name,
                                         price=int(message.text))
    else:
        if not message.photo:
            await message.reply('Try again, there is not image')
            return

        await product_model.edit_product(product_name=data['product'].name,
                                         image=message.photo[-1].file_id)
    await message.reply('Product edited successfully')

    await message.reply("Admin panel", reply_markup=get_menu_inline_keyboard().as_markup())
    await state.clear()


def register_edit_product_handlers(dp: Dispatcher):
    dp.callback_query.register(choice_group, AdminFilter(), lambda callback: callback.data == 'edit_product')
    dp.callback_query.register(choice_product, AdminFilter(), StateFilter(EditProductState.chose_group))
    dp.callback_query.register(choice_edit_information, AdminFilter(), StateFilter(EditProductState.chose_product))
    dp.callback_query.register(edit_product, AdminFilter(), StateFilter(EditProductState.edit_information))
    dp.message.register(end_edit_product, AdminFilter(), StateFilter(EditProductState.edit_product))

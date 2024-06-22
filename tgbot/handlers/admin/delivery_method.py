from aiogram import Dispatcher
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from tgbot.filters import AdminFilter
from tgbot.keyboards.admin import get_delivery_menu_inline_keyboard, get_menu_inline_keyboard, get_choice_delivery
from tgbot.models import DeliveryMethod
from tgbot.misc.admin import AddDeliveryMethod, DeleteDeliveryMethod


async def delivery_method_menu(callback: CallbackQuery):
    await callback.message.edit_text('Delivery methods',
                                     reply_markup=get_delivery_menu_inline_keyboard().as_markup())


async def show_delivery_methods(callback: CallbackQuery):
    delivery_method_list = await DeliveryMethod().get_all_delivery_method()
    text_sting = ''
    for delivery_method in delivery_method_list:
        text_sting += f'{delivery_method.name} - £{delivery_method.price}\n'
    await callback.message.edit_text(f'Delivery methods:\n\n{text_sting}')
    await callback.message.reply('Delivery methods', reply_markup=get_delivery_menu_inline_keyboard().as_markup())


async def start_add_delivery_method(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Write a name')
    await state.set_state(AddDeliveryMethod.name)


async def get_name_delivery_method(message: Message, state: FSMContext):
    if await DeliveryMethod().check_in_db_delivery_method(message.text):
        await message.reply('Try again, this delivery method already exists')
        return
    await state.update_data(name=message.text)
    await message.reply('Write a price')
    await state.set_state(AddDeliveryMethod.price)


async def add_delivery_method(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.reply('Try again, this is not price')
        return
    delivery_method = (await state.get_data())['name']
    await DeliveryMethod().add_delivery_method(name=delivery_method, price=int(message.text))

    await message.reply('delivery method is added')
    await message.reply("Admin panel", reply_markup=get_menu_inline_keyboard().as_markup())
    await state.clear()


async def start_delete_delivery_method(callback: CallbackQuery, state: FSMContext):
    groups_list = await DeliveryMethod().get_all_delivery_method()
    await callback.message.edit_text('Choice a discount to delete',
                                     reply_markup=get_choice_delivery(groups_list).as_markup())
    await state.set_state(DeleteDeliveryMethod.name)


async def delete_delivery_method(callback: CallbackQuery, state: FSMContext):
    if await DeliveryMethod().delete_delivery_method(callback.data):
        await callback.message.edit_text('delivery method is deleted')
        await callback.message.reply("Admin panel", reply_markup=get_menu_inline_keyboard().as_markup())
    else:
        await callback.message.edit_text('We can`t find this delivery method')
    await state.clear()


def register_delivery_method_handler(dp: Dispatcher):
    dp.callback_query.register(delivery_method_menu, AdminFilter(), lambda callback: callback.data == 'admin_delivery')
    dp.callback_query.register(show_delivery_methods,
                               AdminFilter(),
                               lambda callback: callback.data == 'show_all_delivery_method')
    dp.callback_query.register(start_add_delivery_method,
                               AdminFilter(),
                               lambda callback: callback.data == 'add_delivery_method')
    dp.message.register(get_name_delivery_method, AdminFilter(), StateFilter(AddDeliveryMethod.name))
    dp.message.register(add_delivery_method, AdminFilter(), StateFilter(AddDeliveryMethod.price))
    dp.callback_query.register(start_delete_delivery_method,
                               AdminFilter(),
                               lambda callback: callback.data == 'delete_delivery_method')
    dp.callback_query.register(delete_delivery_method, AdminFilter(), StateFilter(DeleteDeliveryMethod.name))


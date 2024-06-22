from aiogram import Dispatcher
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from tgbot.filters import AdminFilter
from tgbot.keyboards.admin import get_discount_menu_inline_keyboard, get_menu_inline_keyboard, get_choice_discount
from tgbot.models import Discount
from tgbot.misc.admin import AddDiscount, DeleteDiscount


async def discount_menu(callback: CallbackQuery):
    await callback.message.edit_text('Discount', reply_markup=get_discount_menu_inline_keyboard().as_markup())


async def show_discount_menu(callback: CallbackQuery):
    discount_list = await Discount().get_all_discount()
    text_sting = ''
    for discount in discount_list:
        text_sting += f'{discount.code} || {discount.percent}%\n'
    await callback.message.edit_text(f'Discounts:\n\n{text_sting}')
    await callback.message.reply('Discount', reply_markup=get_discount_menu_inline_keyboard().as_markup())


async def start_add_discount(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Write a code')
    await state.set_state(AddDiscount.code)


async def get_code_discount(message: Message, state: FSMContext):
    if await Discount().check_in_db_discount(message.text):
        await message.reply('Try again, this code already exists')
        return
    await state.update_data(code=message.text)
    await message.reply('Write a percent')
    await state.set_state(AddDiscount.percent)


async def add_discount(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.reply('Try again, this is not percent')
        return
    code_name = (await state.get_data())['code']
    await Discount().add_discount(code=code_name, percent=int(message.text))

    await message.reply('discount is added')
    await message.reply("Admin panel", reply_markup=get_menu_inline_keyboard().as_markup())
    await state.clear()


async def start_delete_discount(callback: CallbackQuery, state: FSMContext):
    groups_list = await Discount().get_all_discount()
    await callback.message.edit_text('Choice a discount to delete',
                                     reply_markup=get_choice_discount(groups_list).as_markup())
    await state.set_state(DeleteDiscount.code)


async def delete_discount(callback: CallbackQuery, state: FSMContext):
    if await Discount().delete_discount(callback.data):
        await callback.message.edit_text('Discount is deleted')
        await callback.message.reply("Admin panel", reply_markup=get_menu_inline_keyboard().as_markup())
    else:
        await callback.message.edit_text('We can`t find this discount')
    await state.clear()


def register_discount_handler(dp: Dispatcher):
    dp.callback_query.register(discount_menu, AdminFilter(), lambda callback: callback.data == 'admin_discount')
    dp.callback_query.register(show_discount_menu, AdminFilter(), lambda callback: callback.data == 'show_all_discount')
    dp.callback_query.register(start_add_discount, AdminFilter(), lambda callback: callback.data == 'add_discount')
    dp.message.register(get_code_discount, AdminFilter(), StateFilter(AddDiscount.code))
    dp.message.register(add_discount, AdminFilter(), StateFilter(AddDiscount.percent))
    dp.callback_query.register(start_delete_discount,
                               AdminFilter(),
                               lambda callback: callback.data == 'delete_discount')
    dp.callback_query.register(delete_discount, AdminFilter(), StateFilter(DeleteDiscount.code))


from aiogram import Dispatcher
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from tgbot.filters import AdminFilter
from tgbot.keyboards.admin import (get_group_menu_inline_keyboard,
                                   get_menu_inline_keyboard,
                                   get_choose_group_inline_keyboard)
from tgbot.models import Groups
from tgbot.misc.admin import AddGroup, DeleteGroup


async def group_menu(callback: CallbackQuery):
    await callback.message.edit_text('Groups', reply_markup=get_group_menu_inline_keyboard().as_markup())


async def show_group_menu(callback: CallbackQuery):
    group_list = await Groups().get_all_groups()
    text_sting = ''
    for group in group_list:
        text_sting += f'{group}\n'
    await callback.message.edit_text(f'Groups:\n\n{text_sting}')
    await callback.message.reply('Groups', reply_markup=get_group_menu_inline_keyboard().as_markup())


async def start_add_group(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Write a group name')
    await state.set_state(AddGroup.group_name)


async def add_group(message: Message, state: FSMContext):
    if await Groups().check_in_db_group_name(message.text):
        await message.reply('Try again, this group name already exists')
        return
    await Groups().add_group(message.text)
    await message.reply('group name is added')
    await message.reply("Admin panel", reply_markup=get_menu_inline_keyboard().as_markup())
    await state.clear()


async def start_delete_group(callback: CallbackQuery, state: FSMContext):
    groups_list = await Groups().get_all_groups()
    await callback.message.edit_text('Choose a group to delete',
                                     reply_markup=get_choose_group_inline_keyboard(groups_list).as_markup())
    await state.set_state(DeleteGroup.chose_group)


async def delete_group(callback: CallbackQuery, state: FSMContext):
    if await Groups().delete_group(callback.data):
        await callback.message.edit_text('Groups deleted')
        await callback.message.reply("Admin panel", reply_markup=get_menu_inline_keyboard().as_markup())
    else:
        await callback.message.edit_text('We can`t find the group')
    await state.clear()


def register_groups_handler(dp: Dispatcher):
    dp.callback_query.register(group_menu, AdminFilter(), lambda callback: callback.data == 'admin_group')
    dp.callback_query.register(show_group_menu, AdminFilter(), lambda callback: callback.data == 'show_all_groups')
    dp.callback_query.register(start_add_group, AdminFilter(), lambda callback: callback.data == 'add_group')
    dp.message.register(add_group, AdminFilter(), StateFilter(AddGroup.group_name))
    dp.callback_query.register(start_delete_group, AdminFilter(), lambda callback: callback.data == 'delete_group')
    dp.callback_query.register(delete_group, AdminFilter(), StateFilter(DeleteGroup.chose_group))


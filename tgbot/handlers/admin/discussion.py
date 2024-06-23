from aiogram import Dispatcher
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from tgbot.keyboards.admin import discussion_menu_inline_keyboard
from tgbot.misc.admin import DiscussionState
from tgbot.models import Discussion
from tgbot.filters import AdminFilter


async def start_discussion(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('📩 Send messages to the chat',
                                     reply_markup=discussion_menu_inline_keyboard().as_markup())
    await state.set_state(DiscussionState.discussion)
    await state.update_data(user_id=int(callback.data.split('_')[-1]))


async def discussion(message: Message, state: FSMContext):
    user_id = (await state.get_data())['user_id']
    await Discussion().add_basket(user_id, 'Admin', message.text)
    await message.bot.send_message(user_id, f'Admin: {message.text}')


async def discussion_cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text('Chat is closed.')


def register_discussion_handler(dp: Dispatcher):
    dp.callback_query.register(start_discussion,
                               AdminFilter(),
                               lambda callback: callback.data.split('_')[0] == 'discuss')
    dp.message.register(discussion, AdminFilter(), StateFilter(DiscussionState.discussion))
    dp.callback_query.register(discussion_cancel, AdminFilter(), lambda callback: callback.data == 'close_discussion')

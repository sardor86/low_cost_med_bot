from aiogram import Dispatcher
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message, BufferedInputFile
from aiogram.fsm.context import FSMContext

from tgbot.keyboards.user import discussion_menu_inline_keyboard, discussion_cancel_inline_keyboard
from tgbot.misc.user import DiscussionState
from tgbot.keyboards.admin import start_discussion_inline_keyboard
from tgbot.models import Discussion, Users


async def start_discussion(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('📩 Send messages to the chat, be sure to check your secret phrase.\n\n'
                                     f'Phrase: {await Users().get_secret_phrase(callback.from_user.id)}\n'
                                     'Last seen: recently\n\n'
                                     'This is not a live chat, the seller will '
                                     'reply as soon as he reads your messages.',
                                     reply_markup=discussion_menu_inline_keyboard().as_markup())
    await state.set_state(DiscussionState.discussion)
    for admin_id in callback.bot.config.tg_bot.admin_ids:
        await callback.bot.send_message(admin_id,
                                        f'Discussion with {callback.from_user.first_name}',
                                        reply_markup=start_discussion_inline_keyboard(callback.from_user.id).as_markup())


async def discussion(message: Message):
    await Discussion().add_basket(message.from_user.id, 'User', message.text)
    for admin_id in message.bot.config.tg_bot.admin_ids:
        await message.bot.send_message(admin_id, f'{message.from_user.first_name}: {message.text}')


async def discussion_cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text('Chat with the seller is closed. Wait until the seller sees and '
                                     'responds to your messages.',
                                     reply_markup=discussion_cancel_inline_keyboard().as_markup())


async def discussion_history(callback: CallbackQuery):
    discussion_history_str = ''
    for discuss in await Discussion().get_all_discussion(callback.from_user.id):
        discussion_history_str += f'{discuss.role}: {discuss.text}\n'
    await callback.bot.send_document(callback.from_user.id,
                                     BufferedInputFile(bytes(discussion_history_str, 'utf-8'),
                                                       'discussion.txt'))


def register_discussion_handler(dp: Dispatcher):
    dp.callback_query.register(start_discussion, lambda callback: callback.data == 'contact')
    dp.message.register(discussion, StateFilter(DiscussionState.discussion))
    dp.callback_query.register(discussion_cancel, lambda callback: callback.data == 'close_discussion')
    dp.callback_query.register(discussion_history, lambda callback: callback.data == 'discussion_history')

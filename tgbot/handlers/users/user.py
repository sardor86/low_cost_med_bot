from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from tgbot.models import Users
from tgbot.keyboards.user import get_register_inline_keyboard, user_menu_inline_keyboard, back_to_menu_inline_keyboard


async def user_start(message: Message, state: FSMContext):
    await message.reply(f'Welcome, {message.from_user.first_name} !')
    if not await Users().check_in_db_user(message.from_user.id):
        await message.reply('🔐 You need to set a secret phrase to access the bot. '
                            'This will then appear with every verified bot. '
                            'The secret phrase allows you to stay safe and buy only from verified stores.',
                            reply_markup=get_register_inline_keyboard().as_markup())
        return
    await message.reply('Last seen: recently\n'
                        'Ships from: UK → UK\n'
                        'Sales: 2,457\n'
                        'Currency: GBP\n'
                        'Rating: ★4.92 (913)\n',
                        reply_markup=user_menu_inline_keyboard().as_markup())
    await state.clear()


async def menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.reply('Last seen: recently\n'
                                 'Ships from: UK → UK\n'
                                 'Sales: 2,457\n'
                                 'Currency: GBP\n'
                                 'Rating: ★4.92 (913)\n',
                                 reply_markup=user_menu_inline_keyboard().as_markup())
    await state.clear()


async def about(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('About\n\n'
                                     'Welcome to LowCostMedsUK\n\n'                                     
                                     'All items are UK stock unless mentioned. \n\n'                                     
                                     'SHIPPING\n'
                                     'UK - UK only\n'
                                     'Order cut off is 9pm daily Mon-Fri. When marked as shipped order will be '
                                     'dispatched the following working day.\n'
                                     'Please be sure to encrypt address and any personal information.\n'
                                     'All orders are sent tracked/signed to ensure best success and prompt delivery.\n'
                                     'Delivery time up to 3 days approx\n'
                                     'Please allow 7 days before asking for any tracking information.\n\n'   
                                     'ORDER CANCELLATION\n'
                                     'Orders will be cancelled if unable to decrypt address/error.\n'
                                     'Wrong shipping option is chosen for e.g only use add to order option if you have '
                                     'paid the special delivery fee on another order.\n'
                                     'None UK address will be cancelled.\n\n'                                    
                                     'REFUND/RESHIP\n'
                                     'We are not currently offering any refunds as all orders are sent tracked. '
                                     'Only if a mistake is made on our part we will rectify.',
                                     reply_markup=back_to_menu_inline_keyboard().as_markup())
    await state.clear()


def register_user(dp: Dispatcher):
    dp.message.register(user_start, Command("start"))
    dp.callback_query.register(menu, lambda callback: callback.data == 'menu')
    dp.callback_query.register(about, lambda callback: callback.data == 'about')

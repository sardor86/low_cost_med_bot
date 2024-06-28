from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile

from tgbot.models import Users, Review, Basket, Products
from tgbot.keyboards.user import (user_menu_inline_keyboard,
                                  back_to_menu_inline_keyboard,
                                  delete_message_inline_keyboard)


async def user_start(message: Message, state: FSMContext):
    await message.reply(f'Welcome, {message.from_user.first_name} !')
    await Users().add_user(message.from_user.id)

    all_review = await Review().get_all_reviews()

    all_sum_of_review = 0
    for review in all_review:
        all_sum_of_review += review.stars + 1

    basket_list = await Basket().get_all_products(message.from_user.id)
    product_model = Products()

    basket_price = 0

    for basket in basket_list:
        basket_price += (await product_model.get_product_by_id(basket.product)).price

    if len(all_review) == 0:
        middle_review = 0
    else:
        middle_review = all_sum_of_review / len(all_review)

    await message.reply('Ships from: UK → UK\n'
                        'Currency: GBP\n'
                        f'Rating: ★{middle_review} ({len(all_review)})\n',
                        reply_markup=user_menu_inline_keyboard(basket_price).as_markup())

    await state.clear()


async def menu(callback: CallbackQuery, state: FSMContext):
    all_review = await Review().get_all_reviews()

    all_sum_of_review = 0
    for review in all_review:
        all_sum_of_review += review.stars + 1

    basket_list = await Basket().get_all_products(callback.from_user.id)
    product_model = Products()

    basket_price = 0

    for basket in basket_list:
        basket_price += (await product_model.get_product_by_id(basket.product)).price
    await callback.message.delete()

    if len(all_review) == 0:
        middle_review = 0
    else:
        middle_review = all_sum_of_review / len(all_review)

    await callback.bot.send_message(callback.from_user.id,
                                    'Ships from: UK → UK\n'
                                    'Currency: GBP\n'
                                    f'Rating: ★{middle_review} ({len(all_review)})\n',
                                    reply_markup=user_menu_inline_keyboard(basket_price).as_markup())
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


async def public_key(callback: CallbackQuery):
    user_public_key = (await Users().get_secret_user(callback.from_user.id)).public_key

    await callback.bot.send_document(callback.from_user.id,
                                     BufferedInputFile((b'-----BEGIN PGP PUBLIC KEY BLOCK-----\n\n' +
                                                        user_public_key.encode('UTF-8') +
                                                        b'\n-----END PGP PUBLIC KEY BLOCK-----'),
                                                       'public-pgp-key.txt'),
                                     reply_markup=delete_message_inline_keyboard().as_markup())


async def delete_message(callback: CallbackQuery):
    await callback.message.delete()


async def get_rating(callback: CallbackQuery):
    message_text = 'Reviews \n\n'
    all_review = await Review().get_all_reviews()
    for review in all_review:
        message_text += f'{review.date} '
        for star_number in range(5):
            if star_number <= review.stars:
                message_text += '★'
            else:
                message_text += '☆'
        message_text += f' — £{review.price}\n{review.text}\n\n'
    await callback.message.edit_text(message_text, reply_markup=back_to_menu_inline_keyboard().as_markup())


def register_user(dp: Dispatcher):
    dp.message.register(user_start, Command("start"))
    dp.callback_query.register(menu, lambda callback: callback.data == 'menu')
    dp.callback_query.register(about, lambda callback: callback.data == 'about')
    dp.callback_query.register(public_key, lambda callback: callback.data == 'secret_key')
    dp.callback_query.register(delete_message, lambda callback: callback.data == 'delete_message')
    dp.callback_query.register(get_rating, lambda callback: callback.data == 'rating')

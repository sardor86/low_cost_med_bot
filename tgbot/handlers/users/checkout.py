from aiogram import Dispatcher
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message, BufferedInputFile
from aiogram.fsm.context import FSMContext

from tgbot.models import Order, Basket, Products, Discount, DeliveryMethod, Users
from tgbot.misc.user import CheckoutState
from tgbot.keyboards.user import (checkout_menu_inline_keyboard,
                                  checkout_cancellation_inline_keyboard,
                                  get_choice_delivery,
                                  user_menu_inline_keyboard,
                                  checkout_address_menu_inline_keyboard,
                                  delete_message_inline_keyboard)
from tgbot.keyboards.admin import confirm_order_inline_keyboard


async def checkout(user_id: int) -> dict:
    order_model = Order()
    product_model = Products()
    order_list = await order_model.get_all_orders(user_id)
    if not order_list:
        return {
            'message_text': 'You don\'t have any orders.',
            'markup': user_menu_inline_keyboard().as_markup()
        }
    if order_list[0].confirmation:
        message_text = 'Status: Confirmed \n\n'
        markup = None
    elif order_list[0].payment:
        message_text = 'Status: 🕓 Pending Confirmation \n\n'
        markup = None
    else:
        message_text = 'Status: 🕓 Pending Checkout \n\n'

        message_text += ('Enter the discount code, address and delivery method. '
                         'Once your order has been completed, you will be given payment the details\n\n')
        markup = checkout_menu_inline_keyboard(discount_code=order_list[0].discount,
                                               delivery_address=order_list[0].address,
                                               delivery_method=order_list[0].delivery_method).as_markup()
    total_price = 0
    for order in order_list:
        product = await product_model.get_product_by_id(order.product)
        message_text += f'{product.name} {order.quantity} pcs - £{product.price}\n'

        total_price += product.price

    order = order_list[0]
    if order.discount:
        discount_code = await Discount().get_discount_by_id(order_list[0].discount)
        message_text += f'\n\nDiscount {discount_code.percent}% Total £{int(total_price / 100 * discount_code.percent)}'
    else:
        message_text += f'\n\nTotal £{total_price}'

    return {
        'message_text': message_text,
        'markup': markup,
    }


async def checkout_cancellation(callback: CallbackQuery, state: FSMContext):
    if await state.get_state() != CheckoutState.checkout:
        await state.set_state(CheckoutState.checkout)
        message_data = await checkout(callback.from_user.id)
        await callback.message.edit_text(message_data['message_text'], reply_markup=message_data['markup'])
        return
    await callback.message.edit_text('Ships from: UK → UK\n'
                                     'Sales: 2,457\n'
                                     'Currency: GBP\n'
                                     'Rating: ★4.92 (913)\n',
                                     reply_markup=user_menu_inline_keyboard().as_markup())
    await state.clear()


async def checkout_delete(callback: CallbackQuery, state: FSMContext):
    for order in await Order().get_all_orders(callback.from_user.id):
        await order.delete()
    await state.clear()
    await callback.message.edit_text('Order is deleted')


async def get_checkout_menu(callback: CallbackQuery, state: FSMContext):
    basket_list = await Basket().get_all_products(callback.from_user.id)
    order_model = Order()
    for basket in basket_list:
        await order_model.add_order(basket.product,
                                    callback.from_user.id,
                                    basket.quantity,
                                    None,
                                    None,
                                    None,
                                    None)
        await basket.delete()
    message_data = await checkout(callback.from_user.id)

    await callback.message.edit_text(message_data['message_text'], reply_markup=message_data['markup'])
    await state.set_state(CheckoutState.checkout)


async def enter_discount_code(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Send a discount code to the chat',
                                     reply_markup=checkout_cancellation_inline_keyboard().as_markup())
    await state.set_state(CheckoutState.discount)


async def get_checkout_code(message: Message, state: FSMContext):
    discount_model = Discount()
    if not await discount_model.check_in_db_discount(message.text):
        await message.reply('The discount code is not valid, '
                            'check if the code is correct and try again.',
                            reply_markup=checkout_cancellation_inline_keyboard().as_markup())
        return
    discount_code = await discount_model.get_discount(message.text)
    all_order = await Order().get_all_orders(message.from_user.id)
    for order in all_order:
        await order.update(discount=discount_code.id).apply()
    await state.set_state(CheckoutState.checkout)
    message_data = await checkout(message.from_user.id)
    await message.reply(message_data['message_text'], reply_markup=message_data['markup'])


async def enter_address(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(('You can send a message to the chat either as an '
                                      'encrypted message or as plain text. '
                                      'The bot will handle the encryption of your message and '
                                      'display it to the seller after the order is paid for.\n\n'
                                      'Please type your address in this format:\n\n'
                                      '(YOUR NAME) - JAMES HILLS\n'
                                      '(STREET NAME + NUMBER) - Victoria St 155\n'
                                      '(CITY) - LONDON\n'
                                      '(POSTAL CODE) - SW1E 5N\n'
                                      '(COUNTRY) - UNITED KINGDOM\n'),
                                     reply_markup=checkout_address_menu_inline_keyboard().as_markup())
    await state.set_state(CheckoutState.delivery_address)


async def about_checkout_address(callback: CallbackQuery):
    await callback.message.reply('With PGP encryption, only the intended recipient (the shop owner) '
                                 'possessing the private key can decrypt and access your address. '
                                 'This provides end-to-end encryption, preventing any middlemen or '
                                 'service providers from accessing your private information.',
                                 reply_markup=delete_message_inline_keyboard().as_markup())


async def vendor_secret_key(callback: CallbackQuery):
    admin_public_key = (await Users().get_secret_user(callback.bot.config.tg_bot.admin_ids[0])).public_key

    await callback.bot.send_document(callback.from_user.id,
                                     BufferedInputFile((b'-----BEGIN PGP PUBLIC KEY BLOCK-----\n\n' +
                                                        admin_public_key.encode('UTF-8') + b'\n' +
                                                        b'-----END PGP PUBLIC KEY BLOCK-----'),
                                                       'vendor-public-pgp-key.txt'),
                                     reply_markup=delete_message_inline_keyboard().as_markup())


async def get_address(message: Message, state: FSMContext):
    all_order = await Order().get_all_orders(message.from_user.id)
    for order in all_order:
        await order.update(address=message.text).apply()
    await state.set_state(CheckoutState.checkout)
    message_data = await checkout(message.from_user.id)
    await message.reply('Your address has been encrypted using the seller`s public key and saved. '
                        'The address will be revealed to the seller after the order is paid for.')
    await message.reply(message_data['message_text'], reply_markup=message_data['markup'])


async def enter_delivery_method(callback: CallbackQuery, state: FSMContext):
    delivery_method = await DeliveryMethod().get_all_delivery_method()
    await callback.message.edit_text('Please select a delivery method',
                                     reply_markup=get_choice_delivery(delivery_method).as_markup())
    await state.set_state(CheckoutState.delivery_method)


async def get_delivery_method(callback: CallbackQuery, state: FSMContext):
    delivery_method = await DeliveryMethod().get_delivery_method(callback.data)

    all_order = await Order().get_all_orders(callback.from_user.id)
    for order in all_order:
        await order.update(delivery_method=delivery_method.id).apply()
    await state.set_state(CheckoutState.checkout)
    message_data = await checkout(callback.from_user.id)
    await callback.message.edit_text(message_data['message_text'], reply_markup=message_data['markup'])


async def enter_checkout(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Please send cheque from https://t.me/send',
                                     reply_markup=checkout_cancellation_inline_keyboard().as_markup())
    await state.set_state(CheckoutState.payment)


async def get_checkout(message: Message, state: FSMContext):
    cheque = message.text

    all_order = await Order().get_all_orders(message.from_user.id)
    await state.clear()

    admin_message = ''
    total_price = 0
    product_model = Products()
    for order in all_order:
        await order.update(payment=cheque).apply()
        product = await product_model.get_product_by_id(order.product)
        admin_message += f'{product.name} {order.quantity} pcs - £{product.price}\n'
        total_price += product.price

    if all_order[0].discount:
        discount = await Discount().get_discount_by_id(all_order[0].discount)
        admin_message += (f'\nDiscount: {discount.percent}\n'
                          f'Total: £{total_price / 100 * discount.percent}')
    else:
        admin_message += f'Total: £{total_price}\n\n'

    delivery_method = await DeliveryMethod().get_delivery_method_by_id(all_order[0].delivery_method)
    admin_message += f'Delivery method: {delivery_method.name} - £{delivery_method.price}\n\n'

    admin_message += all_order[0].address
    admin_message += f'\n\nCheque: {cheque}'

    for admin_id in message.bot.config.tg_bot.admin_ids:
        await message.bot.send_message(admin_id, admin_message,
                                       reply_markup=confirm_order_inline_keyboard(message.from_user.id).as_markup())

    await message.reply('Please wait when admin confirm your order',
                        reply_markup=user_menu_inline_keyboard().as_markup())


def register_checkout_handler(dp: Dispatcher):
    dp.callback_query.register(checkout_cancellation, lambda callback: callback.data == 'checkout_cancel')
    dp.callback_query.register(get_checkout_menu, lambda callback: callback.data == 'checkout')
    dp.callback_query.register(enter_discount_code, lambda callback: callback.data == 'checkout_discount')
    dp.message.register(get_checkout_code, StateFilter(CheckoutState.discount))
    dp.callback_query.register(enter_address, lambda callback: callback.data == 'checkout_address')
    dp.message.register(get_address, StateFilter(CheckoutState.delivery_address))
    dp.callback_query.register(about_checkout_address, lambda callback: callback.data == 'checkout_about')
    dp.callback_query.register(vendor_secret_key, lambda callback: callback.data == 'vendor_secret_key')
    dp.callback_query.register(enter_delivery_method, lambda callback: callback.data == 'checkout_delivery_method')
    dp.callback_query.register(get_delivery_method, StateFilter(CheckoutState.delivery_method))
    dp.callback_query.register(enter_checkout, lambda callback: callback.data == 'checkout_payment')
    dp.message.register(get_checkout, StateFilter(CheckoutState.payment))
    dp.callback_query.register(checkout_delete, lambda callback: callback.data == 'checkout_delete')

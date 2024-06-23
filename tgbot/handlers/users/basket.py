from aiogram import Dispatcher
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from tgbot.models import Basket, Products
from tgbot.keyboards.user import get_basket_menu, back_to_menu_inline_keyboard
from tgbot.misc.user import BasketState


async def basket_menu(callback: CallbackQuery):
    basket_model = Basket()
    user_basket = await basket_model.get_all_products(callback.from_user.id)

    if not user_basket:
        await callback.bot.send_message(callback.from_user.id,
                                        'Your basket is empty',
                                        reply_markup=back_to_menu_inline_keyboard().as_markup())
        return

    await callback.message.delete()

    message_text = ('This is a list of all the items in your basket. '
                    'If you want to remove any of them, select the name of the item from the list.\n\n')

    product_model = Products()
    total_price = 0

    for basket in user_basket:
        product = await product_model.get_product_by_id(basket.product)
        total_price += product.price * basket.quantity
        message_text += f'{product.name} {basket.quantity} pcs - £{basket.quantity * product.price}\n'

    message_text += f'Total: £{total_price}'

    await callback.bot.send_message(callback.from_user.id,
                                    message_text,
                                    reply_markup=(await get_basket_menu(user_basket)).as_markup())


async def get_basket(callback: CallbackQuery, state: FSMContext):
    await basket_menu(callback)
    await state.set_state(BasketState.basket)


async def delete_basket(callback: CallbackQuery):
    product_id = callback.data.split('.')[0]
    await Basket().delete_basket(int(product_id), callback.from_user.id)
    await basket_menu(callback)


def register_basket_handler(dp: Dispatcher):
    dp.callback_query.register(get_basket, lambda callback: callback.data == 'basket')
    dp.callback_query.register(delete_basket,
                               StateFilter(BasketState.basket),
                               lambda callback: callback.data.split('.')[-1] == 'delete')

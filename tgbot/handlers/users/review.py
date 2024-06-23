from aiogram import Dispatcher
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from tgbot.misc.user import ReviewState
from tgbot.keyboards.user import review_menu_inline_keyboard
from tgbot.models import Review, ReviewProduct, Order, Products, Discount


async def review_menu(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.edit_text(f'Review: \n{data["comment"]}',
                            reply_markup=review_menu_inline_keyboard(data['stars']).as_markup())


async def review_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ReviewState.review)
    await state.update_data(stars=5, comment='')
    await review_menu(callback.message, state)


async def review_star(callback: CallbackQuery, state: FSMContext):
    await state.update_data(stars=int(callback.data[-1]))
    await review_menu(callback.message, state)


async def review_enter_comment(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Please enter your comment')
    await state.set_state(ReviewState.review_text)


async def review_get_comment(message: Message, state: FSMContext):
    await state.update_data(comment=message.text)
    await state.set_state(ReviewState.review)
    data = await state.get_data()
    await message.reply(f'Review: \n{data["comment"]}',
                        reply_markup=review_menu_inline_keyboard(data['stars']).as_markup())


async def review_save(callback: CallbackQuery, state: FSMContext):
    order_list = await Order().get_all_orders_review(callback.from_user.id)
    total_price = 0
    for order in order_list:
        product_price = (await Products().get_product_by_id(order.product)).price * order.quantity
        total_price += product_price

    if order_list[0].discount:
        discount = await Discount().get_discount_by_id(order_list[0].discount)
        total_price += order_list[0] / 100 * discount.percent

    data = await state.get_data()

    review = await Review().add_review(callback.from_user.id,
                                       data['stars'],
                                       total_price,
                                       data['comment'])
    review_product_model = ReviewProduct()
    for order in order_list:
        await review_product_model.add_review(review.id, order.product)
        await order.delete()
    await state.clear()
    await callback.message.edit_text('Your review has been saved.')


def register_review_handlers(dp: Dispatcher):
    dp.callback_query.register(review_start, lambda callback: callback.data == 'review')
    dp.callback_query.register(review_star, lambda callback: callback.data[0:-2] == 'review_star')
    dp.callback_query.register(review_enter_comment, lambda callback: callback.data == 'review_comment')
    dp.message.register(review_get_comment, StateFilter(ReviewState.review_text))
    dp.callback_query.register(review_save, lambda callback: callback.data == 'review_save')

from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from tgbot.keyboards.user import (understand_secret_phrase_inline_keyboard,
                                  get_register_inline_keyboard,
                                  about_secret_phrase_inline_keyboard,
                                  user_menu_inline_keyboard)
from tgbot.misc.user import SetSecretPhrase
from tgbot.models import Users, Review, Basket, Products


async def get_about_secret_phrase(callback: CallbackQuery):
    await callback.message.reply('The secret phrase system is made to protect you '
                                 'from being scammed using fake bots.\n\n'
                                 '1. No one else will know your passphrase, and it is important to remember '
                                 'and always check that your correct passphrase is shown when using our bots. \n'
                                 '2. If a Tesseract vendor decides to disconnect their bot from the market, '
                                 'you can avoid being scammed by making sure the passphrase is still correct. \n\n'
                                 'The first time you use the bot you will be asked to enter your passphrase. '
                                 'This passphrase will be displayed each time in each Tesseract bot, after the '
                                 '/start command, when you create an order and open a chat.\n\n'
                                 "There are many bots on Telegram so please be cautious when using any of them, "
                                 "especially ones that aren't affiliated with Tesseract. "
                                 "We won't be held responsible if you are scammed by a fake bot, "
                                 "these measures are in place to help as much as we are able.",
                                 reply_markup=understand_secret_phrase_inline_keyboard().as_markup())


async def understand_secret_phrase(callback: CallbackQuery):
    await callback.message.edit_text('🔐 You need to set a secret phrase to access the bot. '
                                     'This will then appear with every verified bot. '
                                     'The secret phrase allows you to stay safe and buy only from verified stores.',
                                     reply_markup=get_register_inline_keyboard().as_markup())


async def start_set_secret_phrase(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Send your phrase to the chat in one message. '
                                     'The phrase must be 4-100 characters.\n\n'
                                     '⚠️ WE WILL NEVER ASK FOR YOUR PASSPHRASE AGAIN! BEWARE OF IMPOSTERS!',
                                     reply_markup=about_secret_phrase_inline_keyboard().as_markup())
    await state.set_state(SetSecretPhrase.secret_phrase)


async def set_secret_phrase(message: Message, state: FSMContext):
    if not (4 <= len(message.text) <= 100):
        await message.reply('Try another phrase. The phrase must be 4-100 characters.')
        return

    await Users().add_user(user_id=message.from_user.id,
                           secret_phrase=message.text)

    await message.bot.send_message(message.chat.id, '🎊 The phrase is saved. '
                                                    'No legitimate bot will ever ask for the phrase again.')
    await message.bot.send_message(message.chat.id, 'Please be aware of fake Telegram ShopBots groups and channels '
                                                    'falsely claiming to be Tesseract. \n'
                                                    "To ensure you're interacting with the genuine Tesseract, "
                                                    'visit our official website: tesseract.bot '
                                                    '(https://tesseract.bot/), and verify through our active 24/7 '
                                                    'public chat (https://t.me/+H8qwc80W3nY5ZWM5).\n\n'
                                                    'Any other groups or channels are unauthorized and may pose '
                                                    'security risks. Stay vigilant and protect yourself from '
                                                    'potential fraud.')
    await message.bot.send_message(message.chat.id, '⚠️ Warning!\n\n'
                                                    f'Phrase: {message.text}\n\n'
                                                    "Please verify the provided phrase. We won't request it again or "
                                                    'permit changes. Beware of scam bots seeking the same phrase.')
    all_review = await Review().get_all_reviews()

    review_middle = 0
    for review in all_review:
        review_middle += review.stars + 1

    basket_list = await Basket().get_all_products(message.from_user.id)
    product_model = Products()

    basket_price = 0

    for basket in basket_list:
        basket_price += (await product_model.get_product_by_id(basket.product)).price

    await message.reply('Ships from: UK → UK\n'
                        'Currency: GBP\n'
                        f'Rating: ★{review_middle / len(all_review)} ({len(all_review)})\n',
                        reply_markup=user_menu_inline_keyboard(basket_price).as_markup())
    await state.clear()


def register_secret_phrase_handlers(dp: Dispatcher):
    dp.callback_query.register(get_about_secret_phrase, lambda callback: callback.data == 'about_secret_phrase')
    dp.callback_query.register(understand_secret_phrase, lambda callback: callback.data == 'understand_secret_phrase')
    dp.callback_query.register(start_set_secret_phrase, lambda callback: callback.data == 'set_secret_phrase')
    dp.message.register(set_secret_phrase, StateFilter(SetSecretPhrase.secret_phrase))

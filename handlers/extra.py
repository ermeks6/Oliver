from random import choice

from aiogram import types, Dispatcher
from config import bot


async def delete_sticker(message: types.Message):
    await message.delete()


async def bad_words_filter(message: types.Message):
    bad_words = ['html', 'js', 'css', 'жинди', 'дурак']
    for word in bad_words:
        if word in message.text.lower().replace(' ', ''):
            await message.answer(f"Не матерись {message.from_user.full_name}, "
                                 f"сам ты {word}")
            await message.delete()
            break

    if message.text.lower() == 'game':
        a = ['⚽', '🎰', '🏀', '🎯', '🎳', '🎲']
        random = choice(a)
        await bot.send_dice(message.chat.id, emoji=random)
    else:
        await bot.send_message(message.from_user.id, message.text)


def register_handlers_extra(dp: Dispatcher):
    dp.register_message_handler(bad_words_filter, content_types=['text'])
    dp.register_message_handler(delete_sticker, content_types=['sticker', 'photo',
                                                               'animation'])
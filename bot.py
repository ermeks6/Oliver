from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from decouple import config
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = config("TOKEN")

bot = Bot(TOKEN)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Hello world!")


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.answer("Сам разбирайся!")


@dp.message_handler(commands=['quiz'])
async def quiz_1(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_1 = InlineKeyboardButton("NEXT", callback_data="button_1")
    markup.add(button_1)

    question = "Ты гей?"
    answer = [
        "Да",
        "Да",
    ]
    await bot.send_poll(
        chat_id=message.from_user.id,
        question=question,
        options=answer,
        is_anonymous=False,
        type='quiz',
        correct_option_id=1,
        explanation="Ой, кажется кто-то ошибся",
        open_period=5,
        reply_markup=markup
    )


@dp.callback_query_handler(text="button_1")
async def quiz_2(call: types.CallbackQuery):
    question = "Кто украл рождество?"
    answer = [
        "Олов",
        "Гринч",
        "Сын маминой подруги",
        "Снегурочка",
        "Вор",
        "Я",
    ]
    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answer,
        is_anonymous=False,
        type='quiz',
        correct_option_id=1,
        explanation="Ошибка!",
        open_period=5,
    )


@dp.message_handler()
async def message_handler(message):
    if message.text.isdigit():
        await bot.send_message(
            chat_id=message.chat.id,
            text=str(int(message.text) ** 2)
        )
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text=message.text
        )


@dp.message_handler(commands=['mem'])
async def mem_handler(message: types.Message):
    url = 'https://i.pinimg.com/originals/b1/3e/19/b13e1928a298443993655983be8577d2.jpg'
    await bot.send_photo(chat_id=message.from_user.id, photo=url)


@dp.message_handler()
async def echo(message: types.Message):

    if message.text == "python":
        await message.answer("I love it!")
    else:
        await bot.send_message(
            chat_id=message.from_user.id,
            text=f"Салам {message.from_user.full_name}"
        )
        await message.answer(f"This is an answer method! {message.message_id}")
        await message.reply("This is a reply method!")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


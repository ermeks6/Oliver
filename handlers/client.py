from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from config import bot
from keyboards.client_kb import start_markup
from database.bot_db import sql_command_random
from parser.news import parser


async def start_command(message: types.Message):
    await message.answer("sup", reply_markup=start_markup)


async def help_command(message: types.Message):
    await message.answer("bro idk")


async def quiz_1(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_1 = InlineKeyboardButton("NEXT", callback_data="button_1")
    markup.add(button_1)

    question = "Столица КР"
    answer = [
        "Ош",
        "Бишкек",
    ]
    await bot.send_poll(
        chat_id=message.from_user.id,
        question=question,
        options=answer,
        is_anonymous=False,
        type='quiz',
        correct_option_id=1,
        explanation="your answer is wrong",
        open_period=5,
        reply_markup=markup
    )


async def get_news(message: types.Message):
    news = parser()
    for i in news:
        await message.answer(
            f"{i['link']}\n\n"
            f"<b><a href='{i['link']}'>{i['title']}</a></b>\n"
            f"{i['description']}\n"
            f"{i['date_from_html']}\n",
            parse_mode=ParseMode.HTML
        )


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(help_command, commands=['help'])
    dp.register_message_handler(quiz_1, commands=['quiz'])
    dp.register_message_handler(get_news, commands=['news'])
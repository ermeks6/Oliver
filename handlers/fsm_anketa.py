from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from database.bot_db import sql_command_insert
from keyboards import client_kb
from uuid import uuid4
from config import ADMINS


class FSMAdmin(StatesGroup):
    id1 = State()
    name = State()
    age = State()
    direction = State()
    group = State()
    submit = State()


async def fsm_start(message: types.Message):
    if message.chat.type == "private" and message.chat.id in ADMINS:
        await FSMAdmin.id1.set()
        await message.answer("Your id is ready!", reply_markup=client_kb.cancel_markup)
    else:
        await message.answer("Write to the group!")


async def load_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = str(uuid4())
    await FSMAdmin.next()
    await message.answer("Enter your name: ",  reply_markup=client_kb.cancel_markup)


async def load_name(message: types.Message, state: FSMContext):
    name = message.text.strip()
    if not name.isalpha():
        await message.answer("Your name should contain only letters")
    else:
        async with state.proxy() as data:
            data['username'] = message.from_user.username
            data['name'] = name
        await FSMAdmin.next()
        await message.answer("Enter your age: ")


async def load_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Write in numbers!")
    elif int(message.text) < 15 or int(message.text) > 40:
        await message.answer("Your age should be a number between 15 and 40")
    else:
        async with state.proxy() as data:
            data['age'] = message.text
        await FSMAdmin.next()
        await message.answer("What direction are you studying?: ", reply_markup=client_kb.direction_markup)


async def load_direction(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['direction'] = message.text
    await FSMAdmin.next()
    await message.answer("What group are you in?: ", reply_markup=client_kb.cancel_markup)


async def load_group(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['group'] = message.text
        await message.answer(f"{data['name']} {data['age']} {data['group']} {data['direction']}\n"
                             f"ID: {data['id']}")
    await FSMAdmin.next()
    await message.answer("Is everything right?", reply_markup=client_kb.submit_markup)


async def submit(message: types.Message, state: FSMContext):
    if message.text == "yes":
        await sql_command_insert(state)
        await message.answer("ghghgfjhgdfkh")
        await state.finish()
    elif message.text == "no":
        await state.finish()
    else:
        await message.answer("Please answer 'yes' or 'no'")


async def cansel_reg(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state:
        await state.finish()
        await message.answer("You completed the operation")
        await message.answer("canceled✔️️")


def register_handlers_fsm_anketa(dp: Dispatcher):
    dp.register_message_handler(cansel_reg, state='*', commands=['cancel'])
    dp.register_message_handler(cansel_reg,
                                Text(equals="cancel", ignore_case=True), state='*')

    dp.register_message_handler(fsm_start, commands=['reg'])
    dp.register_message_handler(load_id, state=FSMAdmin.id1)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_age, state=FSMAdmin.age)
    dp.register_message_handler(load_direction, state=FSMAdmin.direction)
    dp.register_message_handler(load_group, state=FSMAdmin.group)
    dp.register_message_handler(submit, state=FSMAdmin.submit)


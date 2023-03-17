from aiogram import  types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMAdmin(StatesGroup):
    name = State()
    age = State()
    group = State()
    direction = State()


async def fsm_start(message: types.Message):
    if message.chat.type == "private":
        await FSMAdmin.name.set()
        await message.answer("Enter your name: ")
    else:
        await message.answer("Write to the group!")


async def load_name(message: types.Message, state: FSMContext):
    name = message.text.strip()
    if not name.isalpha():
        await message.answer("Your name should contain only letters")
    else:
        async with state.proxy() as data:
            data['id'] = message.from_user.id
            data['username'] = message.from_user.username
            data['name'] = name
        await FSMAdmin.next()
        await message.answer("Enter your age: ")


async def load_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Your age should be a number between 15 and 40")
    elif int(message.text) < 15 or int(message.text) > 40:
        await message.answer("Your age should be a number between 15 and 40")
    else:
        async with state.proxy() as data:
            data['age'] = message.text
        await FSMAdmin.next()
        await message.answer("What group are you in?: ")


async def load_group(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['group'] = message.text
    await FSMAdmin.next()
    await message.answer("What direction are you studying?: ")


async def load_direction(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['direction'] = message.text
        await message.answer(f"{data['name']} {data['age']} {data['group']} {data['direction']}\n"
                             f"@{data['username']}")
    await FSMAdmin.next()
    await message.answer("Is everything right?")


def register_handlers_fsm_anketa(dp: Dispatcher):
    dp.register_message_handler(fsm_start, commands=['reg'])
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_age, state=FSMAdmin.age)
    dp.register_message_handler(load_group, state=FSMAdmin.group)
    dp.register_message_handler(load_direction, state=FSMAdmin.direction)

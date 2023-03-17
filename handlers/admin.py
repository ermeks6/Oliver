from aiogram import types, Dispatcher
from config import ADMINS, bot

async def ban(message: types.Message):
    if message.chat.type != "private":
        if message.from_user.id not in ADMINS:
            await message.answer("You are not admin!")
        elif not message.reply_to_message:
            await message.answer("The command must be a response to a message")
        else:
            await bot.kick_chat_member(
                message.chat.id,
                message.reply_to_message.from_user.id
            )
            await message.answer(f"{message.from_user.first_name} you got kicked out "
                                 f"{message.reply_to_message.from_user.full_name}")
    else:
        await message.answer("Write to the group!")

async def bin_handler(message: types.Message):
    if message.chat.type != 'private':
        if message.from_user.id not in ADMINS:
            await message.answer('Only admins can post here')
        elif not message.reply_to_message:
            await message.answer('The command must be a response to a message')
        else:
            await bot.pin_chat_message(message.chat.id,
                                       message.reply_to_message.message_id)
    else:
        await message.answer('Write to the group!')

def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(bin_handler, commands=['bin'], commands_prefix='!/')
    dp.register_message_handler(ban, commands=['ban'], commands_prefix='!/')
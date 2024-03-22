import asyncio
import logging

from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandObject
from aiogram import F, md

from aiogram.utils.formatting import Text, Bold
from datetime import datetime

from config_reader import config

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [[types.KeyboardButton(text='ROAR'),
           types.KeyboardButton(text='MOAR')]]

    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder='BebeBe')

    await message.answer("What do you excpect?", reply_markup=keyboard)


@dp.message(F.text.upper() == "ROAR")
async def roar(message: types.Message):
    await message.answer("TIGER", reply_markup=types.ReplyKeyboardRemove())


@dp.message(F.text.upper() == "MOAR")
async def moar(message: types.Message):
    await message.answer("MUR", reply_markup=types.ReplyKeyboardRemove())


@dp.message(F.text, Command("test"))
async def cmd_test1(message: types.Message):
    await message.answer("hi, <b>bye</b>", parse_mode=ParseMode.HTML)
    await message.answer("hi, *bye*")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

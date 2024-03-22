import asyncio
import logging

import aiogram.enums.dice_emoji
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

from config_reader import config

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")


@dp.message(Command("show_list"))
async def cmd_test1(message: types.Message, my_list: list[int]):
    await message.answer(f"{my_list}")


@dp.message(Command("add_to_list"))
async def cmd_test1(message: types.Message, my_list: list[int]):
    my_list.append(999)
    await message.reply("Added value is 999")

async def main():
    await dp.start_polling(bot, my_list=[0, 3, 6, 9])


if __name__ == "__main__":
    asyncio.run(main())

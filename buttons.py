import asyncio
import logging

from magic_filter import F
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from typing import Optional

class NumbersCallbackFactory(CallbackData, prefix="fabnum"):
    action: str
    value: Optional[int] = None


from config_reader import config

logging.basicConfig(level=logging.INFO)

user_data = {}

bot = Bot(token=config.bot_token.get_secret_value())

dp = Dispatcher()


@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("HI")


def get_markup():
    buttons = [
        [
            types.InlineKeyboardButton(text="-1", callback_data="num_decr"),
            types.InlineKeyboardButton(text="+1", callback_data="num_incr")
        ],
        [types.InlineKeyboardButton(text="DONE", callback_data="num_done")]]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard




def get_keyboard_fab():
    builder = InlineKeyboardBuilder()

    builder.button(text="-2", callback_data=NumbersCallbackFactory(action="change", value=-2))

    builder.button(text="-1", callback_data=NumbersCallbackFactory(action="change", value=-1))

    builder.button(text="1", callback_data=NumbersCallbackFactory(action="change", value=1))

    builder.button(text="2", callback_data=NumbersCallbackFactory(action="change", value=2))

    builder.button(text="DONE", callback_data=NumbersCallbackFactory(action="done"))

    builder.adjust(4)
    return builder.as_markup()


async def update_text(message: types.Message, user_value: int):
    try:
        await message.edit_text(f"Укажи число: {user_value}", reply_markup=get_keyboard_fab())
    except:
        pass


@dp.message(Command("numbers"))
async def cmd_num(message: types.Message):
    user_data[message.from_user.id] = 0
    await message.answer("Укажи число: 0", reply_markup=get_keyboard_fab())


@dp.callback_query(NumbersCallbackFactory.filter(F.action == "change"))
async def callback_num(callback: types.CallbackQuery, callback_data: NumbersCallbackFactory):
    user_data[callback.from_user.id] += callback_data.value
    await update_text(callback.message, user_data[callback.from_user.id])

    await callback.answer()

@dp.callback_query(NumbersCallbackFactory.filter(F.action == "done"))
async def callback_num(callback: types.CallbackQuery, callback_data: NumbersCallbackFactory):
    await callback.message.edit_text(f"Итого: {user_data[callback.from_user.id]}")

    await callback.answer()

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

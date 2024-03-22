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
    await message.answer("Hello!")


@dp.message(F.text, Command("test"))
async def cmd_test1(message: types.Message):
    await message.answer("hi, <b>bye</b>", parse_mode=ParseMode.HTML)
    await message.answer("hi, *bye*")


@dp.message(F.text, Command("hello"))
async def cmd_hello(message: types.Message):
    context = Text("Hello, ", Bold(message.from_user.full_name))
    await message.answer(**context.as_kwargs())


# @dp.message(F.text)
# async def echo_with_time(message: types.Message):
#     time_now = datetime.now().strftime("%H:%M")
#     added_text = md.underline(f"Создано в {time_now}")
#
#     await message.answer(f"{message.md_text}\n\n{added_text}")

# @dp.message(F.text)
# async def extract_data(message: types.Message):
#     data = {
#         "url": "<N/A>",
#         "email": "<N/A>",
#         "code": "<N/A>"
#     }
#     entities = message.entities or []
#     for item in entities:
#         if item.type in data.keys():
#             data[item.type] = item.extract_from(message.text)
#     await message.reply(
#         f"Вот что я нашёл:\n \
#         URL: {md.quote(data['url'])}\n \
#         email: {md.quote(data['email'])}\n \
#         Пароль: {md.quote(data['code'])}")

@dp.message(Command("args"))
async def com_args(message: types.Message, command: CommandObject):
    if command.args is None:
        await message.answer("Ошибка не переданы аргументы")
        return

    try:
        arg, text = command.args.split(maxsplit=1)
    except ValueError:
        await message.answer("Ошибка. Неправильный формат команды.\n"
                             "Пример: /args <arg> <text>")
        return

    await message.answer("Аргумент получен!\n"
                         f"arg = {arg}\n"
                         f"text = {text}")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

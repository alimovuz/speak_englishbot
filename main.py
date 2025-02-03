import asyncio
import sys
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from dotenv import load_dotenv
import os
from tools import custom_translator, get_word_details, identify_lang

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

dp = Dispatcher()

async def main() -> None:
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)


@dp.message(CommandStart())
async def command_start(message: types.Message):
    await message.answer("Speak Easy English botiga xush kelibsiz!")

@dp.message(Command("help"))
async def command_help(message: types.Message):
    await message.answer("Qanday savollaringiz bor!")

@dp.message()
async def speak_easy_english(message: types.Message):
    lang = await identify_lang(message.text)
    try:
        if len(message.text.split(" ")) >1:
            translation = custom_translator(text=message.text, lang="en")
            await message.reply(translation)
        elif lang.lang == "en":
            details = get_word_details(message.text)
            data = f"word: {message.text},\n definitions: {'\n'.join(details)}"
            await message.reply(data)
        elif lang.lang == "uz":
            word = custom_translator(message.text, lang="en")
            details = get_word_details(word)
            data = f"so'z: {message.text},\n tarjima: {word},\n definitions: {'\n'.join(details)}"
            await message.reply(data)
    except Exception as e:
        print(e)
        await message.reply("Bunday so'z topilmadi!")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
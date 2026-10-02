import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🔎Serch anime'),
        ],
    ],
    resize_keyboard=True,
)

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        'AnimeTracker bot\n'
        'Dev: @saaayq',
        reply_markup=main_keyboard,
    )

@dp.message()
async def handle_message(message:Message):
    if message.text == '🔎Serch anime':
        await message.answer('Enter title')
    
async def main():
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    asyncio.run(main())

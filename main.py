import asyncio
import os

import httpx
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
if BOT_TOKEN is None:
    raise ValueError('BOT_TOKEN is not set')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🔎 Search anime'),
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
    if message.text == '🔎 Search anime':
        await message.answer('Enter title')
        return
    
    if not message.text:
        return
    
    anime = await search_anime(message.text)
    if anime is None:
        await message.answer('Anime not found')
        return
    
    title_english = anime['title']['english'] or anime['title']['romaji']
    title_romaji = anime['title']['romaji']
    
    episodes = anime['episodes'] or 'Unknown'
    score = anime['averageScore'] or 'No rating'
    
    await message.answer(
        f'<b>{title_english}</b>\n'
        f'<i>{title_romaji}</i>\n\n'
        f'⭐Score: {score / 10 if score != 'No rating' else score}/10\n'
        f'🎬Episodes: {episodes}',
        parse_mode='HTML'
    )
    

async def search_anime(title:str):
    query = '''
    query ($search: String) {
        Media(search: $search, type: ANIME) {
            id
            title {
                romaji
                english
            }
            episodes
            averageScore
        }
    }
    '''
    
    variables = {
        'search': title,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            'https://graphql.anilist.co',
            json={
                "query": query,
                "variables": variables,
            },
        )
    if response.status_code != 200:
        return None
    data = response.json()
    
    return data['data']['Media']


async def main():
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    asyncio.run(main())

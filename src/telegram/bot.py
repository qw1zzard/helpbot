import asyncio
import logging
import os
from uuid import uuid4

import aiohttp
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message
from aiogram.utils.markdown import hbold

API_URL = os.getenv('API_URL', 'http://localhost:80/api/v1/get_answer/')

bot = Bot(token=os.getenv('TELEGRAM_TOKEN', ''))
dp = Dispatcher()
router = Router()


@router.message(F.text)
async def handle_user_message(message: Message) -> None:
    user_input = message.text
    session_id = str(uuid4())

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                API_URL,
                json={
                    'session_id': session_id,
                    'history': [{'role': 'user', 'content': user_input}],
                },
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    await message.answer(f'{hbold("Answer")}: {data["answer"]}')
                else:
                    await message.answer('⚠️ Something went wrong.')
        except Exception as e:
            await message.answer(f'Error: {e}')


def start_telegram_bot() -> None:
    dp.include_router(router)
    logging.basicConfig(level=logging.INFO)

    asyncio.run(dp.start_polling(bot))


if __name__ == '__main__':
    start_telegram_bot()

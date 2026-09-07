import asyncio
import logging
import os
from contextlib import suppress

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from handlers import reminders_router, start_router
from services.reminder_worker import reminder_worker


async def main():
    load_dotenv()

    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("Добавьте BOT_TOKEN в файл .env")

    bot = Bot(token=token)
    dp = Dispatcher()

    dp.include_routers(
        start_router,
        reminders_router,
    )

    worker_task = asyncio.create_task(reminder_worker(bot))

    try:
        await dp.start_polling(bot)
    finally:
        worker_task.cancel()
        with suppress(asyncio.CancelledError):
            await worker_task
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

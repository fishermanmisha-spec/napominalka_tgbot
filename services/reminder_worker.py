import asyncio
import logging
from datetime import datetime

from aiogram import Bot

from storage import get_unsent_reminders, mark_as_sent
from utils.dates import parse_date


logger = logging.getLogger(__name__)


async def reminder_worker(bot: Bot):
    while True:
        reminders = get_unsent_reminders()
        now = datetime.now()

        for reminder in reminders:
            remind_at = parse_date(reminder["remind_at"])

            if remind_at is None or remind_at > now:
                continue

            try:
                await bot.send_message(
                    chat_id=int(reminder["user_id"]),
                    text=f'Напоминание:\n{reminder["text"]}',
                )
                mark_as_sent(
                    int(reminder["id"]),
                    int(reminder["user_id"]),
                )
            except Exception:
                logger.exception(
                    "Не удалось отправить напоминание id=%s",
                    reminder.get("id"),
                )

        await asyncio.sleep(10)

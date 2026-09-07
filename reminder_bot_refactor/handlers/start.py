from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


router = Router(name="start")


@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "Привет. Я бот-напоминалка.\n\n"
        "Команды:\n"
        "/add — добавить напоминание\n"
        "/list — список напоминаний\n"
        "/about — о боте\n"
        "/cancel — отменить текущее действие\n"
        "/history — история отправленных напоминаний\n"
        "/today — напоминания на сегодня\n"
        "/change — изменить напоминание\n"
        "/count — количество напоминаний"
    )


@router.message(Command("about"))
async def about_handler(message: Message):
    await message.answer(
        "Я бот-напоминалка.\n"
        "Я напомню о событиях, которые вы добавите."
    )

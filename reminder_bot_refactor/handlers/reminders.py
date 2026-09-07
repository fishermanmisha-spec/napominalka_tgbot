from datetime import datetime

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


import storage
from states import ChangeReminderState, ReminderState
from utils.dates import format_date, parse_date


router = Router(name="reminders")


def read_user_reminders(user_id: int):
    reminders = storage.read_reminders(user_id=user_id)

    if not reminders or reminders == "Нет напоминаний.":
        return []

    future_reminders = []
    now = datetime.now()

    for reminder in reminders:
        reminder_date = parse_date(reminder[1])

        if reminder_date is not None and reminder_date > now:
            future_reminders.append(reminder)

    return future_reminders


@router.message(Command("list"))
async def list_handler(message: Message):
    reminders = read_user_reminders(user_id=message.from_user.id)

    if not reminders:
        await message.answer("У вас пока нет напоминаний.")
        return

    reminders = sorted(
        reminders,
        key=lambda reminder: parse_date(reminder[1]) or datetime.max,
    )

    text = "Ваши напоминания:\n\n"
    text += "\n".join(
        f"#{number}. {remind_at} — {info}"
        for number, (_, remind_at, info) in enumerate(reminders, start=1)
    )

    await message.answer(text)


@router.message(Command("today"))
async def today_handler(message: Message):
    reminders = read_user_reminders(user_id=message.from_user.id)
    today = datetime.now().date()
    today_reminders = []

    for reminder in reminders:
        reminder_date = parse_date(reminder[1])

        if reminder_date is not None and reminder_date.date() == today:
            today_reminders.append(reminder)

    if not today_reminders:
        await message.answer("На сегодня напоминаний нет.")
        return

    today_reminders = sorted(
        today_reminders,
        key=lambda reminder: parse_date(reminder[1]) or datetime.max,
    )

    text = "Напоминания на сегодня:\n\n"
    text += "\n".join(
        f"#{number}. {remind_at} — {info}"
        for number, (_, remind_at, info) in enumerate(today_reminders, start=1)
    )

    await message.answer(text)


@router.message(Command("history"))
async def history_handler(message: Message):
    reminders = storage.read_sent_reminders(user_id=message.from_user.id)

    if not reminders:
        await message.answer("История отправленных напоминаний пуста.")
        return

    reminders = sorted(
        reminders,
        key=lambda reminder: parse_date(reminder[1]) or datetime.min,
        reverse=True,
    )

    text = "История отправленных напоминаний:\n\n"
    text += "\n".join(
        f"#{number}. {remind_at} — {info}"
        for number, (_, remind_at, info) in enumerate(reminders, start=1)
    )

    await message.answer(text)


@router.message(Command("count"))
async def count_handler(message: Message):
    reminders = read_user_reminders(user_id=message.from_user.id)
    await message.answer(f"У вас {len(reminders)} напоминаний.")


@router.message(Command("change"))
async def change_handler(message: Message, state: FSMContext):
    reminders = read_user_reminders(user_id=message.from_user.id)

    if not reminders:
        await message.answer("У вас нет напоминаний для изменения.")
        return

    reminders = sorted(
        reminders,
        key=lambda reminder: parse_date(reminder[1]) or datetime.max,
    )

    await state.clear()
    await state.update_data(reminders=reminders)
    await state.set_state(ChangeReminderState.waiting_number)

    text = "Выберите напоминание, которое хотите изменить:\n\n"
    text += "\n".join(
        f"#{number}. {remind_at} — {info}"
        for number, (_, remind_at, info) in enumerate(reminders, start=1)
    )
    text += "\n\nВведите номер напоминания:"

    await message.answer(text)


@router.message(Command("add"))
async def add_handler(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(ReminderState.waiting_date)
    await message.answer(
        "Введите дату в формате:\n"
        "31.01.2027 14:30"
    )


@router.message(Command("cancel"))
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state is None:
        await message.answer("Сейчас нет действия, которое можно отменить.")
        return

    await state.clear()
    await message.answer("Действие отменено.")


@router.message(Command("get_time"))
async def get_time_handler(message: Message):
    await message.answer(datetime.now().strftime("%d.%m.%Y %H:%M:%S"))


@router.message(ChangeReminderState.waiting_number)
async def changing_number_handler(message: Message, state: FSMContext):
    if not message.text or not message.text.isdigit():
        await message.answer("Введите номер напоминания, например: 1")
        return

    number = int(message.text)
    data = await state.get_data()
    reminders = data["reminders"]

    if number < 1 or number > len(reminders):
        await message.answer("Напоминания с таким номером нет.")
        return

    selected_reminder = reminders[number - 1]
    reminder_id = int(selected_reminder[0])

    await state.update_data(reminder_id=reminder_id)
    await state.set_state(ChangeReminderState.waiting_date)
    await message.answer(
        "Введите новую дату в формате:\n"
        "31.01.2027 14:30"
    )


@router.message(ChangeReminderState.waiting_date)
async def changing_date_handler(message: Message, state: FSMContext):
    new_date = (message.text or "").strip()

    try:
        parsed_date = parse_date(new_date)
    except ValueError:
        await message.answer(
            "Некорректная дата.\n"
            "Введите дату в формате:\n"
            "31.01.2027 14:30"
        )
        return

    if parsed_date is None:
        await message.answer(
            "Некорректная дата.\n"
            "Введите дату в формате:\n"
            "31.01.2027 14:30"
        )
        return

    if parsed_date <= datetime.now():
        await message.answer(
            "Эта дата уже прошла.\n"
            "Введите будущую дату."
        )
        return

    new_date = parsed_date.strftime("%d.%m.%Y %H:%M")

    await state.update_data(new_date=new_date)
    await state.set_state(ChangeReminderState.waiting_info)

    await message.answer("Введите новый текст напоминания.")

@router.message(ChangeReminderState.waiting_info)
async def changing_info_handler(message: Message, state: FSMContext):
    new_info = (message.text or "").strip()

    if not new_info:
        await message.answer("Текст напоминания не может быть пустым.")
        return

    data = await state.get_data()
    changed = storage.change_reminder(
        user_id=message.from_user.id,
        reminder_id=data["reminder_id"],
        remind_at=data["new_date"],
        text=new_info,
    )

    if changed:
        await message.answer(
            "Напоминание изменено:\n\n"
            f'{data["new_date"]} — {new_info}'
        )
    else:
        await message.answer("Не получилось изменить напоминание.")

    await state.clear()


@router.message(ReminderState.waiting_date)
async def date_handler(message: Message, state: FSMContext):
    date_text = (message.text or "").strip()
    remind_at = parse_date(date_text)

    if remind_at is None:
        await message.answer("Не понял дату. Введите так: 31.01.2027 14:30")
        return

    if remind_at <= datetime.now():
        await message.answer("Эта дата уже прошла. Введите будущую дату.")
        return

    date_text = format_date(remind_at)
    await state.update_data(date=date_text)
    await state.set_state(ReminderState.waiting_info)
    await message.answer(
        f"Введённая дата: {date_text}\n"
        "Введите событие для этой даты:"
    )


@router.message(ReminderState.waiting_info)
async def info_handler(message: Message, state: FSMContext):
    info = (message.text or "").strip()

    if not info:
        await message.answer("Текст напоминания не может быть пустым.")
        return

    data = await state.get_data()
    date = data["date"]

    storage.add_reminder(
        user_id=message.from_user.id,
        text=info,
        remind_at=date,
    )

    await message.answer(f"Напоминание добавлено:\n{date} — {info}")
    await state.clear()

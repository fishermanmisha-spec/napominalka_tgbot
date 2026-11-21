from aiogram.fsm.state import State, StatesGroup


class ReminderState(StatesGroup):
    waiting_date = State()
    waiting_info = State()


class ChangeReminderState(StatesGroup):
    waiting_number = State()
    waiting_date = State()
    waiting_info = State()

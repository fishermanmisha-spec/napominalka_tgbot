import csv
from pathlib import Path

FILE_PATH = Path("reminders.csv")
FIELDNAMES = ["id", "user_id", "text", "remind_at", "is_sent"]


def ensure_file():
    if FILE_PATH.exists():
        return

    with open(FILE_PATH, "w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES, delimiter=";")
        writer.writeheader()


def read_reminders(user_id: int) -> list[list[str]]:
    ensure_file()
    user_reminders = []

    with open(FILE_PATH, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file, delimiter=";")

        for reminder in reader:
            if (
                reminder["user_id"] == str(user_id)
                and reminder["is_sent"] == "0"
            ):
                user_reminders.append([
                    reminder["id"],
                    reminder["remind_at"],
                    reminder["text"],
                ])

    return user_reminders


def get_next_id(user_id: int) -> int:
    ensure_file()
    reminder_ids = []

    with open(FILE_PATH, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file, delimiter=";")

        for reminder in reader:
            if reminder["user_id"] == str(user_id):
                reminder_ids.append(int(reminder["id"]))

    if not reminder_ids:
        return 1

    return max(reminder_ids) + 1

def add_reminder(user_id: int, text: str, remind_at: str):
    ensure_file()
    if text == '':
        return 'событие не можетбыть пустым.'
    reminder = {
        "id": get_next_id(user_id),
        "user_id": user_id,
        "text": text,
        "remind_at": remind_at,
        "is_sent": "0",
    }

    with open(FILE_PATH, "a", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES, delimiter=";")
        writer.writerow(reminder)


def write_reminders(add_reminders:list[dict]):
    with open(FILE_PATH, 'w', encoding='utf-8-sig', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES, delimiter=";")
        writer.writeheader()
        writer.writerows(add_reminders)

def get_unsent_reminders() -> list[dict]:
    ensure_file()

    with open(FILE_PATH, 'r', encoding='utf-8-sig', newline='') as file:
        reader = csv.DictReader(file, delimiter=';')
        reminders = list(reader)

    return [
        reminder
        for reminder in reminders
        if reminder['is_sent'] == '0'
    ]
def mark_as_sent(reminder_id: int, user_id: int):
    ensure_file()

    with open(FILE_PATH, 'r', encoding='utf-8-sig', newline='') as file:
        reader = csv.DictReader(file, delimiter=';')
        reminders = list(reader)

    for reminder in reminders:
        if (
            int(reminder['id']) == reminder_id
            and int(reminder['user_id']) == user_id
        ):
            reminder['is_sent'] = '1'

    write_reminders(reminders)

def read_sent_reminders(user_id: int) -> list[list]:
    ensure_file()
    sent_reminders = []

    with open(FILE_PATH, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file, delimiter=";")

        for reminder in reader:
            if (
                reminder["user_id"] == str(user_id)
                and reminder["is_sent"] == "1"
            ):
                sent_reminders.append([
                    reminder["id"],
                    reminder["remind_at"],
                    reminder["text"]
                ])

    return sent_reminders

def delete_reminders(user_id: int, reminder_id: int) -> bool:
    reminders = read_reminders()
    new_reminders = []
    deleted = False

    for reminder in  reminders:
        same_user = int(reminder['user_id']) == user_id
        same_id = int(reminder['id']) == reminder_id

        if same_user and same_id and reminder['is_sent'] == '0':
            deleted = True
            continue

            new_reminders.append(reminder)

        write_reminders(new_reminders)
        return deleted

def change_reminder(
            user_id: int,
            reminder_id: int,
            text: str,
            remind_at: str
    ) -> bool:
        ensure_file()

        with open(
                FILE_PATH,
                'r',
                encoding='utf-8-sig',
                newline=''
        ) as file:
            reader = csv.DictReader(file, delimiter=';')
            reminders = list(reader)

        changed = False

        for reminder in reminders:
            if (
                    int(reminder['user_id']) == user_id
                    and int(reminder['id']) == reminder_id
                    and reminder['is_sent'] == '0'
            ):
                reminder['text'] = text
                reminder['remind_at'] = remind_at
                changed = True
                break

        if changed:
            write_reminders(reminders)

        return changed



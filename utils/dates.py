from datetime import datetime


DATE_FORMATS = (
    "%d.%m.%Y %H:%M",
    "%d.%m.%y %H:%M",
    "%d-%m-%Y %H:%M",
    "%d-%m-%y %H:%M",
)


def parse_date(date_text: str):
    for date_format in DATE_FORMATS:
        try:
            return datetime.strptime(date_text, date_format)
        except ValueError:
            continue

    return None


def format_date(date: datetime) -> str:
    return date.strftime("%d.%m.%Y %H:%M")

# Новая структура бота-напоминалки

```text
reminder_bot_refactor/
├── main.py
├── states.py
├── storage.py                 # скопируйте свой существующий файл
├── reminders.csv             # скопируйте свой существующий файл
├── .env
├── handlers/
│   ├── __init__.py
│   ├── start.py
│   └── reminders.py
├── services/
│   ├── __init__.py
│   └── reminder_worker.py
└── utils/
    ├── __init__.py
    └── dates.py
```

## Что где находится

- `main.py` только создаёт бота, подключает обработчики и запускает проект.
- `handlers/start.py` содержит команды `/start` и `/about`.
- `handlers/reminders.py` содержит команды и состояния для напоминаний.
- `states.py` содержит FSM-состояния.
- `services/reminder_worker.py` проверяет и отправляет наступившие напоминания.
- `utils/dates.py` отвечает за разбор и единый формат даты.
- `storage.py` продолжает отвечать за CSV. Его код на этом этапе менять не нужно.

## Как запустить

1. Скопируйте в эту папку свои `storage.py` и `reminders.csv`.
2. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

3. Создайте рядом с `main.py` файл `.env` и добавьте в него новый токен:

   ```env
   BOT_TOKEN=новый_токен_из_BotFather
   ```

4. Запустите:

   ```bash
   python main.py
   ```

## Важно про токен

Токен из старого файла уже был показан открытым текстом. В BotFather выполните
`/revoke`, выберите бота и используйте новый токен только в `.env`.

## Требования к существующему storage.py

Новая структура вызывает те же функции, которые уже использовались в старом
файле:

- `read_reminders`
- `read_sent_reminders`
- `add_reminder`
- `change_reminder`
- `get_unsent_reminders`
- `mark_as_sent`

Лучше, чтобы `read_reminders` всегда возвращала список. Пока оставлена
совместимость со старым вариантом, который мог вернуть строку
`"Нет напоминаний."`.

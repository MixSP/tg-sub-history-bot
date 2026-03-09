# tg-sub-history-bot

![Python](https://img.shields.io/badge/python-3.11+-blue)
![aiogram](https://img.shields.io/badge/aiogram-3.x-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Simple and lightweight Telegram bot that records channel and chat subscriber join/leave events to SQLite. Add the bot as an administrator to a channel or group to start logging.

## Why

Telegram does not provide built-in history of subscriber changes.
This bot records join and leave events so administrators can analyze
channel growth and churn over time.

**Stack:** Python 3.11+, [aiogram](https://github.com/aiogram/aiogram) 3.x, SQLite, [Poetry](https://python-poetry.org/) for dependencies.

## Features

- Listens for `chat_member` updates (join, leave, kick).
- Writes each event to SQLite: `user_id`, `username`, `channel_id`, `event_type` (`joined` / `left`), `timestamp`.
- Deduplicates by `(user_id, channel_id, event_type, timestamp)`.

## Project structure

- **bot.py** — entry point, `/start` and `chat_member` handlers, logging, polling
- **db.py** — SQLite connection, init, event insert/deduplication
- **config.py** — `BOT_TOKEN`, `DB_PATH`, `LOG_FILE` (set token before run)
- **schema.py** — `events` table definition
- **pyproject.toml** — Poetry deps (Python 3.11+, aiogram)
- **.gitignore** — venv, `.env`, logs, `*.db`

Secrets can live in `.env` and be loaded in code; the bot does not read `.env` by default.

## Database

Table `events`; full schema is in `schema.py`. Columns:

- `id` — auto-increment primary key
- `user_id` — Telegram user id
- `username` — Telegram @username (optional; may be empty)
- `channel_id` — chat/channel id
- `event_type` — `joined` or `left`
- `timestamp` — UTC

**Example rows:**

| id | user_id | username | channel_id | event_type | timestamp |
|----|---------|----------|------------|------------|-----------|
| 1 | 123456789 | johndoe | -1001234567890 | joined | 2025-03-09 12:00:00 |
| 2 | 123456789 | johndoe | -1001234567890 | left | 2025-03-09 14:30:00 |

## Setup

**Prerequisites**

- Python 3.11+
- [Poetry](https://python-poetry.org/docs/#installation) (`pip install poetry` or official installer)

**Steps**

1. Clone the repository.
2. Install dependencies: `poetry install`.
3. Configure: edit `config.py` and set `BOT_TOKEN` (from [@BotFather](https://t.me/BotFather)). Optionally set `DB_PATH` and `LOG_FILE`.
4. Run: `poetry run python bot.py` (or `poetry shell` then `python bot.py`).

## Running

Add the bot as an **administrator** to the desired Telegram channel or group (with permission to receive `chat_member` updates). It will log join/leave events to the database; no extra commands are required.

**Security:** Do not commit a real `BOT_TOKEN`. Keep it in `config.py` only on the server, or use `.env` and load it in code (if so, consider adding `config.py` to `.gitignore` when it holds secrets).

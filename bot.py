import asyncio
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime, timezone
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.enums import ChatMemberStatus
from aiogram.filters import CommandStart
from aiogram.types import ChatMemberUpdated, Message

from config import BOT_TOKEN, LOG_FILE, POLLING_TIMEOUT
import db

Path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def _ts(date) -> str:
    if isinstance(date, datetime):
        dt = date if date.tzinfo else date.replace(tzinfo=timezone.utc)
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    return datetime.fromtimestamp(date, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Бот записывает подписки/отписки в каналах и чатах. Добавьте его администратором.")


@dp.chat_member()
async def on_chat_member(event: ChatMemberUpdated):
    new = event.new_chat_member
    status = new.status

    if status == ChatMemberStatus.MEMBER:
        event_type = "joined"
    elif status in (ChatMemberStatus.LEFT, ChatMemberStatus.KICKED):
        event_type = "left"
    else:
        return

    user_id = new.user.id
    username = new.user.username
    channel_id = event.chat.id
    timestamp = _ts(event.date)

    conn = db.get_connection()

    try:
        if db.event_exists(conn, user_id, channel_id, event_type, timestamp):
            return

        db.insert_event(conn, user_id, username, channel_id, event_type, timestamp)
        conn.commit()

        logger.info(
            "channel_id=%s | user_id=%s | username=%s | event_type=%s | recorded",
            channel_id, user_id, username or "-", event_type,
        )
    except Exception as e:
        logger.error(
            "channel_id=%s | user_id=%s | event_type=%s | error: %s",
            channel_id, user_id, event_type, e,
        )
    finally:
        conn.close()


async def main():
    db.init_db()

    try:
        await dp.start_polling(
            bot,
            polling_timeout=POLLING_TIMEOUT,
            allowed_updates=dp.resolve_used_update_types(),
        )
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())

import  os
import asyncio
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from handlers import customer
from database import db_manager

async def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    load_dotenv()

    db_manager.init_db()

    bot = Bot(token=os.getenv("BAKE_CAKE_TG_TOKEN"))
    db = Dispatcher()

    db.include_router(customer.router)

    logger.info("Запускаю бот...")
    await db.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Остановка бота...")


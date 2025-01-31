import asyncio
import logging

from aiogram import Bot, Dispatcher
from app.admin_handler import admin_router
from app.cart_handler import cart_router
from app.handlers import router
from app.find_product import order_router
from app.make_order import make_order_router
from app.reviews import make_review_router
from app.set_address import set_order_router
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    dp.include_router(router)
    dp.include_router(admin_router)
    dp.include_router(order_router)
    dp.include_router(set_order_router)
    dp.include_router(make_order_router)
    dp.include_router(cart_router)
    dp.include_router(make_review_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
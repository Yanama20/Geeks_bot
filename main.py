from aiogram import executor
import logging
from config import bot, Admins, dp
from db.main_db import fetch_all_products
from handlers import commands, echo, quiz, webapp, FSM_store, delete_products, send_products, edit_product
import buttons
from db import main_db
from handlers.send_products import send_all_products


async def on_startup(_):
    for admin in Admins:
        await bot.send_message(chat_id=admin, text='Бот включен!', reply_markup=buttons.start)

    await main_db.create_db()


commands.register_handlers(dp)
quiz.register_handlers(dp)
webapp.register_handlers(dp)
FSM_store.register_handlers_fsm_reg(dp)
send_products.register_handlers(dp)
delete_products.register_handlers(dp)
edit_product.register_handlers(dp)


echo.register_handlers(dp)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
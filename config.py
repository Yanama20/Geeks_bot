from aiogram.contrib.fsm_storage.memory import MemoryStorage
from decouple import config
from aiogram import Bot, Dispatcher

token = config('TOKEN')
bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

Admins = [455160831, ]
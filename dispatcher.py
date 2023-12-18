from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
TOKEN = '6523654290:AAFEkRW4YmyGqd_38tdi0l7H0AiBGVmVVXk'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

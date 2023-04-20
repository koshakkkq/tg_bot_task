from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils import parse_config, get_available_currencies
import motor.motor_asyncio

available_currencies = get_available_currencies()

config = parse_config()

api_token = config['tg_token']

mongo_db_conn_str = config['mongo_conn']

weather_token = config['weather_key']

exchange_token = config['exchange_rates_key']

picture_token = config['picture_search_key']

db_client = motor.motor_asyncio.AsyncIOMotorClient(mongo_db_conn_str)

db_tg_task = db_client.tg_task


bot = Bot(token=api_token)
dp = Dispatcher(bot, storage=MemoryStorage())

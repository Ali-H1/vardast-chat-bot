import logging
from aiogram.utils import executor
from src.telegram import dp

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)

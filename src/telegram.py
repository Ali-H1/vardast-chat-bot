from aiogram import Bot, Dispatcher, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from src import environments as env
from src.DB import db_collection
from src.model import chat_with_gpt, get_last_index

bot = Bot(token=env.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    """Handle /start command."""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Delete History"))
    keyboard.add(KeyboardButton("Enable History"))
    await bot.send_message(
        message.chat.id,
        "Hello! I'm your AI assistant. Chat with me!",
        reply_markup=keyboard,
    )


@dp.message_handler(lambda message: message.text == "Delete History")
async def delete_history(message: types.Message):
    """Disable history for the user (without deleting from database)."""
    user_id = str(message.chat.id)
    db_collection.update_one({"user_id": user_id}, {"$set": {"history_index": -1}})
    await bot.send_message(
        user_id,
        "Your chat history has been disabled. Future messages won't be remembered.",
    )


@dp.message_handler(lambda message: message.text == "Enable History")
async def enable_history(message: types.Message):
    """Enable history for the user from this point onward."""
    user_id = str(message.chat.id)
    db_collection.update_one(
        {"user_id": user_id}, {"$set": {"history_index": get_last_index(user_id)}}
    )
    await bot.send_message(
        user_id,
        "Your chat history has been enabled. Future messages will be remembered.",
    )


@dp.message_handler()
async def handle_message(message: types.Message):
    """Handle user messages."""
    user_id = str(message.chat.id)
    response = chat_with_gpt(user_id, message.text)
    await bot.send_message(
        user_id,
        response,
        reply_markup=ReplyKeyboardMarkup(resize_keyboard=True)
        .add(KeyboardButton("Delete History"))
        .add(KeyboardButton("Enable History")),
    )

from pymongo import MongoClient

from src import environments as env

client = MongoClient(env.MONGO_URI)
db = client.chatbot
db_collection = db.chat_history

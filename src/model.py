from openai import OpenAI
from scipy.spatial.distance import cosine

import environments as env
from DB import db_collection

openAI_client = OpenAI(api_key=env.openAI_client_API_KEY)


def get_last_index(user_id):
    """Get the last index of the chat history for a user."""
    record = db_collection.find_one({"user_id": user_id}, {"history": 1})
    if record and "history" in record:
        return len(record["history"]) - 1
    return -1


def get_chat_history(user_id):
    """Retrieve the chat history from MongoDB."""
    record = db_collection.find_one({"user_id": user_id})
    return record["history"] if record else []


def get_embedding(text):
    """Generate an embedding vector for text."""
    response = openAI_client.embeddings.create(
        model="text-embedding-ada-002", input=text
    )
    return response.data[0].embedding


def save_message(user_id, role, content):
    """Save chat messages with their embeddings in MongoDB."""
    embedding = get_embedding(content) if role == "user" else None
    message_data = {"role": role, "content": content}
    if embedding:
        message_data["embedding"] = embedding

    db_collection.update_one(
        {"user_id": user_id},
        {"$push": {"history": message_data}, "$setOnInsert": {"history_index": 0}},
        upsert=True,
    )


def get_relevant_messages(user_id, query, top_n=5):
    """Find the most relevant past messages based on embeddings if history is enabled."""
    record = db_collection.find_one({"user_id": user_id})
    if record and record.get("history_index", -1) == -1:
        return []

    query_embedding = get_embedding(query)
    history = record["history"] if record else []

    scored_messages = []
    for message in history:
        if "embedding" in message:
            similarity = 1 - cosine(query_embedding, message["embedding"])
            scored_messages.append((similarity, message))

    scored_messages.sort(reverse=True, key=lambda x: x[0])
    return [msg[1] for msg in scored_messages[:top_n]]


def chat_with_gpt(user_id, message):
    """Interact with openAI_client GPT model while maintaining relevant context."""
    relevant_history = get_relevant_messages(user_id, message)

    messages = [
        {
            "role": "system",
            "content": "This is a continuation of the user's past conversation.",
        }
    ]
    messages.extend(relevant_history)
    messages.append({"role": "user", "content": message})
    response = openAI_client.chat.completions.create(model="gpt-4o", messages=messages)
    bot_reply = response.choices[0].message.content

    save_message(user_id, "user", message)
    save_message(user_id, "assistant", bot_reply)

    return bot_reply

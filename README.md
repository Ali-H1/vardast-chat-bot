# Telegram ChatGPT Bot with MongoDB History


## Features
- **ChatGPT Integration**: Uses OpenAI's GPT-4o to generate responses.
- **MongoDB Storage**: Stores all user messages and responses in a local MongoDB database.
- **Context Awareness**: Retrieves past conversations based on similarity using cosine distance.
- **Delete History Mode**: Stops sending previous messages to the model (but keeps them in the database).
- **Enable History Mode**: Resumes sending stored history to improve responses.
- **Embedding-Based Search**: Uses OpenAI's Embeddings API to find the most relevant past messages.
- **Asynchronous Processing**: Built with `aiogram` for efficient message handling.

## Installation
### 1. Clone the Repository
```bash
git clone https://github.com/your-repo/telegram-chatgpt-bot.git
cd telegram-chatgpt-bot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

Create `/src/environments.py` file and set `TOKEN` and `OPENAI_API_KEY` in the script:
```python
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
MONGO_URI = "mongodb://localhost:27017"
```

### 4. Run the Bot
```bash
python main.py
```

## Usage
- **Start the bot**: `/start`
- **Chat with the bot**: Just send a message!
- **Disable chat history**: Click **"Delete History"** (history is not sent to OpenAI, but remains stored in MongoDB).
- **Enable chat history**: Click **"Enable History"** (new messages will be remembered and sent to OpenAI for context).

## How It Works
1. **User sends a message** → Bot processes it.
2. **Finds relevant past messages** using [**cosine similarity**](https://en.wikipedia.org/wiki/Cosine_similarity) of embeddings.
3. **Sends query + relevant history** to GPT-4o.
4. **GPT-4o generates a response**, which is saved in MongoDB.
5. **User can disable or enable history** anytime.



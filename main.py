import os
from flask import Flask, request, jsonify
from PyCharacterAI import get_client
from PyCharacterAI import Client
from dotenv import load_dotenv
import asyncio

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Initialize the CharacterAI client
client = None

async def init_client():
    global client
    auth_token = os.getenv('CHARACTERAI_AUTH_TOKEN')
    if not auth_token:
        raise Exception("CHARACTERAI_AUTH_TOKEN is not set in the .env file")
    client = await get_client(token=auth_token)

# Initialize the client asynchronously
loop = asyncio.get_event_loop()
loop.run_until_complete(init_client())

@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    data = request.json

    # Extract the character ID and user message
    character_id = data.get('model')
    messages = data.get('messages')

    # Validate input
    if not character_id or not messages:
        return jsonify({"error": "Missing 'model' or 'messages'"}), 400

    # Use the last message from the user
    user_message = messages[-1]['content']

    # Send the message to Character.AI
    response = loop.run_until_complete(client.chat.send_message(character_id, user_message))

    # Structure the response to mimic OpenAI's format
    return jsonify({
        "id": response['conversation_id'],
        "object": "chat.completion",
        "created": response['created_at'],
        "model": character_id,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": response['text']
                },
                "finish_reason": "stop"
            }
        ]
    })

if __name__ == '__main__':
    app.run(port=5000)

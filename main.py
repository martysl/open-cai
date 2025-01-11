import os
import asyncio
from flask import Flask, request, jsonify
from PyCharacterAI import get_client
from PyCharacterAI.exceptions import SessionClosedError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Store session client and chat data
clients = {}
chats = {}

# Initialize the CharacterAI client
async def init_client(token):
    return await get_client(token=token)

@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    data = request.json
    token = os.getenv('CHARACTERAI_AUTH_TOKEN')
    
    if not token:
        return jsonify({"error": "CHARACTERAI_AUTH_TOKEN is missing from environment."}), 400

    # Get CharacterID and messages
    character_id = data.get('model')
    messages = data.get('messages')

    if not character_id or not messages:
        return jsonify({"error": "Missing 'model' or 'messages'"}), 400

    # Retrieve session or create a new one
    if character_id not in clients:
        client = asyncio.run(init_client(token))  # Use asyncio.run() here for a new loop
        clients[character_id] = client
        chat, greeting_message = asyncio.run(client.chat.create_chat(character_id))  # Run async functions
        chats[character_id] = chat

        # Send the initial greeting message
        greeting = greeting_message.get_primary_candidate().text
        return jsonify({
            "id": chat.chat_id,
            "model": character_id,
            "message": greeting
        })

    client = clients[character_id]
    chat = chats[character_id]

    # Send user message to the character
    try:
        user_message = messages[-1]['content']
        answer = asyncio.run(client.chat.send_message(character_id, chat.chat_id, user_message))  # Use asyncio.run() here
        response_text = answer.get_primary_candidate().text

        return jsonify({
            "id": chat.chat_id,
            "model": character_id,
            "message": response_text
        })

    except SessionClosedError:
        return jsonify({"error": "Session closed. Please start a new chat."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(port=5000)

import os
from flask import Flask, request, jsonify
from PyCharacterAI import Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
client = PyCAI()

# Get the auth token from the environment variable
auth_token = os.getenv('CHARACTERAI_AUTH_TOKEN')

# Ensure the token is set
if not auth_token:
    raise Exception("CHARACTERAI_AUTH_TOKEN is not set in the .env file")

# Login to Character AI
client.start_jwt_session(auth_token=auth_token)

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
    response = client.chat.send_message(character_id, user_message)

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

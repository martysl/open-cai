from flask import Flask, request, jsonify, render_template_string
import os
import asyncio
from PyCharacterAI import get_client
from PyCharacterAI.exceptions import SessionClosedError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# HTML for the index page
INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Open-cai</title>
    <style>
        body {
            margin: 0;
            background-color: #000;
            color: #fff;
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
        }
        .container {
            text-align: center;
        }
        h1 {
            font-size: 60px;
            margin: 0;
            color: #ff4444;
        }
        p {
            font-size: 18px;
            color: #aaa;
            margin-top: 10px;
        }
        p span {
            color: #ff4444;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Open-cai</h1>
        <p>by Marty with <span>♥</span> and little TasiaGpt</p>
    </div>
</body>
</html>
"""

# Serve the index page
@app.route('/')
def index():
    return render_template_string(INDEX_HTML)

# Existing chat completions route
@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    data = request.json
    token = os.getenv('CHARACTERAI_AUTH_TOKEN')

    if not token:
        return jsonify({"error": "CHARACTERAI_AUTH_TOKEN is missing from environment."}), 400

    character_id = data.get('model')
    messages = data.get('messages')

    if not character_id or not messages:
        return jsonify({"error": "Missing 'model' or 'messages'"}), 400

    if character_id not in clients:
        client = asyncio.run(get_client(token=token))
        clients[character_id] = client
        chat, greeting_message = asyncio.run(client.chat.create_chat(character_id))
        chats[character_id] = chat
        greeting = greeting_message.get_primary_candidate().text
        return jsonify({"id": chat.chat_id, "model": character_id, "message": greeting})

    client = clients[character_id]
    chat = chats[character_id]

    try:
        user_message = messages[-1]['content']
        answer = asyncio.run(client.chat.send_message(character_id, chat.chat_id, user_message))
        response_text = answer.get_primary_candidate().text
        return jsonify({"id": chat.chat_id, "model": character_id, "message": response_text})
    except SessionClosedError:
        return jsonify({"error": "Session closed. Please start a new chat."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)

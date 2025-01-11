import os
from flask import Flask, request, jsonify, render_template_string
from PyCharacterAI import get_client
from PyCharacterAI.exceptions import SessionClosedError, RequestError

app = Flask(__name__)

INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Open-cai</title>
    <style>
        body {
            background-color: black;
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            font-family: Arial, sans-serif;
        }
        .container {
            text-align: center;
        }
        h1 {
            font-size: 48px;
            margin: 0;
        }
        p {
            font-size: 18px;
            color: gray;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 style="color: red">Open-cai</h1>
        <p><small>Made by TasiaGPT and Marty with ♥ </small></p>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(INDEX_HTML)

@app.route('/v1/chat/completions', methods=['POST'])
async def chat_completions():
    data = request.json  # Removed the 'await' here
    print(f"Received data: {data}")  # Debugging incoming data

    if not data or 'prompt' not in data or 'character_id' not in data:
        return jsonify({"error": "Invalid request"}), 400

    character_id = data['character_id']
    prompt = data['prompt']
    
    # Get token from the environment variable
    token = os.getenv('CHARACTERAI_AUTH_TOKEN')
    if not token:
        return jsonify({"error": "API token not found"}), 400

    try:
        print("Initializing client...")
        client = await get_client(token=token)
        print("Client initialized successfully.")

        # Check if character_id is valid
        print(f"Character ID: {character_id}")

        chat, greeting_message = await client.chat.create_chat(character_id)
        print(f"Chat created: {chat.chat_id}")

        response_message = await safe_send_message(client, character_id, chat.chat_id, prompt)
        await client.close_session()
        return jsonify({"response": response_message}), 200

    except SessionClosedError as e:
        return jsonify({"error": f"Session closed: {str(e)}"}), 500
    except RequestError as e:
        return jsonify({"error": f"Request error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unknown error: {str(e)}"}), 500

async def safe_send_message(client, character_id, chat_id, message, max_retries=5):
    retries = 0
    while retries < max_retries:
        try:
            answer = await client.chat.send_message(character_id, chat_id, message)
            return answer.get_primary_candidate().text
        except (RequestError, ConnectionResetError):
            retries += 1
            await asyncio.sleep(2 ** retries)  # Exponential backoff
    raise RequestError("Failed to send message after multiple retries")

@app.route('/v1/images/generations', methods=['POST'])
async def image_generation():
    data = await request.get_json()
    if not data or 'prompt' not in data:
        return jsonify({"error": "Invalid request"}), 400

    prompt = data['prompt']
    token = os.getenv('CHARACTERAI_AUTH_TOKEN')

    try:
        client = await get_client(token=token)
        images = await client.utils.generate_image(prompt)

        # Print each URL (for debugging/logging)
        for image_url in images:
            print(image_url)

        await client.close_session()

        # Return all image URLs as JSON
        return jsonify({"images": images}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="1112")

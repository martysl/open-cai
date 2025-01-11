# AI API Endpoint (OpenAI-style) using PyCharacterAI

**This project provides an OpenAI-style API endpoint to interact with Character.AI using the PyCharacterAI library. The API mimics OpenAI’s /v1/chat/completions endpoint, allowing developers to send and receive messages from Character.AI bots**.

>[!NOTE]
>We not provide auth token you need got your own see how [here](https://github.com/Xtr4F/PyCharacterAI)  

## Features:  
- [x] OpenAI-style endpoint (/v1/chat/completions)
- [x] Supports Character.AI characters
- [x] Easy to deploy on Vercel
- [x] Environment variable support for secure token management

## Getting Started (localy)
📦 1. Clone the Repository:  
```
git clone https://github.com/martysl/open-cai  
cd cai
```
📋 2. Requirements
Install the necessary packages:
```
pip install -r requirements.txt
```

⚙️ 3. Create a .env File
Create a .env file in the project root to store your Character.AI authentication token:
```
CHARACTERAI_AUTH_TOKEN=your_auth_token_here
```
▶️ 4. Run the API Locally
Start the Flask server:
python main.py
Your API will be running at:
```
http://localhost:5000/v1/chat/completions
```
## 📡 Deploy on Vercel
🔧 1. Use Webpage interface add project using repo: https://github.com/martysl/cai  
🚀 2. Deploy to Vercel  
🔐 3. Set Environment Variables on Vercel  
- Go to your Vercel Dashboard.  
- Navigate to Settings > Environment Variables.  
- Add the following variable:  
```
your_auth_token_here ad CHARACTERAI_AUTH_TOKEN
```
📥 API Endpoint Usage  
Send a POST request to the following endpoint:  
```
POST https://your-project-name.vercel.app/v1/chat/completions
```

## 🔧 Example Usage:

Request:
```
{
  "model": "CHARACTER_ID",
  "messages": [
    {"role": "user", "content": "Hello, how are you?"}
  ]
}
```

Response:
```
{
  "id": "conversation12345",
  "object": "chat.completion",
  "created": 1700000000,
  "model": "CHARACTER_ID",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "I'm great, thank you! How can I help you today?"
      },
      "finish_reason": "stop"
    }
  ]
}
```

## 🛠 Project Structure  
📁 ai-endpoint  
 ┣ 📄 main.py  
 ┣ 📄 requirements.txt  
 ┣ 📄 vercel.json  
 ┣ 📄 .env (example included in GitHub)  
 ┗ 📄 README.md  
  
## 🤝 Contributing
Feel free to submit issues or pull requests. Contributions are welcome!

## 📄 License
This project is licensed under the MIT License.

## Credits
👨‍💻 Made by Marty with Help from TasiaGPT(our ai)  
Website: [easierit.org](https://main.easierit.org)  
Aditional Thx to: [PyCharacterAI](https://github.com/Xtr4F/PyCharacterAI) 


import os
import openai

import httpx
from fastapi import FastAPI, Request


TOKEN = str(os.getenv("TELEGRAM_BOT_TOKEN"))
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"





openai.api_key = os.getenv("OPENAI_API_KEY")
conversation = []

class ChatGPT:  
    

    def __init__(self):
        
        self.messages = conversation
        self.model = os.getenv("OPENAI_MODEL", default = "gpt-3.5-turbo")



    def get_response(self, user_input):
        conversation.append({"role": "user", "content": user_input})
        

        response = openai.ChatCompletion.create(
	            model=self.model,
                messages = self.messages

                )

        conversation.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
        
        print("AI回答內容：")        
        print(response['choices'][0]['message']['content'].strip())


        
        return response['choices'][0]['message']['content'].strip()

client = httpx.AsyncClient()
app = FastAPI()
chatgpt = ChatGPT()

@app.get("/") # 指定 api 路徑 (get方法)
async def hello():
	return "Hello World from Flask in a uWSGI Nginx Docker container with \
	     Python 3.8 (from the example template)"
    
@app.post("/callback")
async def callback(req: Request):
    data = await req.json()
    chat_id = data['message']['chat']['id']
    text = data['message']['text']
    ai_reply_response = chatgpt.get_response(text)  

    await client.get(f"{BASE_URL}/sendMessage?chat_id={chat_id}&text={ai_reply_response}")

    return data

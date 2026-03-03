from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os
from langchain_openai import ChatOpenAI

app = FastAPI()

# Initialize the LLM
llm = ChatOpenAI(
    model="gpt-4.1-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)

# Set up templates
templates = Jinja2Templates(directory="templates")

class ChatMessage(BaseModel):
    message: str

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(chat_message: ChatMessage):
    try:
        response = llm.invoke(f"in 1 sentence: {chat_message.message}")
        responseaichat = response.content        
        return {"responseaichat": str(responseaichat)}
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
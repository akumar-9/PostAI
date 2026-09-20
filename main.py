from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Enable CORS for your React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Change this to your frontend URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)
output_parser = StrOutputParser()

# We instruct the model to avoid markdown for clean copy-pasting
system_instruction = "Do not use markdown formatting like asterisks, bolding, or headers. Provide plain text with appropriate emojis."

templates = {
    "linkedin": ChatPromptTemplate.from_messages([("system", f"{system_instruction} Write a formal LinkedIn post. Tone: {{tone}}. Audience: {{audience}}."), ("user", "{content}")]),
    "twitter": ChatPromptTemplate.from_messages([("system", f"{system_instruction} Write a concise Twitter post under 280 characters. Tone: {{tone}}. Audience: {{audience}}."), ("user", "{content}")]),
    "facebook": ChatPromptTemplate.from_messages([("system", f"{system_instruction} Write a friendly Facebook post. Tone: {{tone}}. Audience: {{audience}}."), ("user", "{content}")]),
}

chains = {key: template | llm | output_parser for key, template in templates.items()}
all_chains = RunnableParallel(**chains)

class PostRequest(BaseModel):
    content: str
    tone: str = "Professional"
    audience: str = "General"

@app.post("/generate")
async def generate_posts(request: PostRequest):
    try:
        # Run LangChain concurrently
        results = await all_chains.ainvoke({
            "content": request.content,
            "tone": request.tone,
            "audience": request.audience
        })
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

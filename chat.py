from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from agent.llm_agent import LLMAgent

router = APIRouter()
agent  = LLMAgent()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[Message]] = []

@router.post("/chat")
async def chat(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")
    try:
        history = [{"role": m.role, "content": m.content}
                   for m in (request.conversation_history or [])]
        result = agent.chat(user_message=request.message, conversation_history=history)
        return {**result, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health():
    return agent.health_check()
"""
FastAPI backend for a simple AI chatbot.

Run with:
    uvicorn main:app --reload
"""

import os
from typing import Optional

import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


# A system prompt that gives the AI assistant context about the business.
SYSTEM_PROMPT = (
    "You are a helpful assistant for a web development agency called WebAura. "
    "Help users understand services, pricing, and encourage them to contact."
)


class ChatRequest(BaseModel):
    """Expected JSON request body for /chat."""

    message: str


class ChatResponse(BaseModel):
    """JSON response returned by /chat."""

    reply: str


# Initialize FastAPI app.
app = FastAPI(title="WebAura Chatbot API")

# Allow frontend apps to call this backend from different origins.
# For local development, allowing all origins is the simplest option.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve files from the static folder.
app.mount("/static", StaticFiles(directory="static"), name="static")


def generate_placeholder_reply(user_message: str) -> str:
    """Fallback chatbot response when NVIDIA API is not available."""

    return (
        "Thanks for your message! (Placeholder mode) "
        "WebAura offers website design, web app development, and ongoing support. "
        "For exact pricing, please share your project goals and timeline. "
        f"You said: '{user_message}'"
    )


def generate_nvidia_reply(user_message: str) -> Optional[str]:
    """Return an AI response from NVIDIA API, or None if key/client is unavailable."""

    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        return None

    invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "qwen/qwen3.5-122b-a10b",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        "max_tokens": 2048,
        "temperature": 0.60,
        "top_p": 0.95,
        "stream": False,
        "chat_template_kwargs": {"enable_thinking": True},
    }

    response = requests.post(invoke_url, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()

    choices = data.get("choices", [])
    if not choices:
        return None

    content = choices[0].get("message", {}).get("content")
    return content.strip() if content else None


@app.get("/")
def serve_frontend() -> FileResponse:
    """Serve the chat web page."""

    return FileResponse("static/index.html")


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """
    Receive a user message and return an AI-generated reply.

    Input JSON:
        {"message": "Hello"}

    Output JSON:
        {"reply": "Hi!"}
    """

    user_message = request.message.strip()
    if not user_message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    try:
        ai_reply = generate_nvidia_reply(user_message)
        if not ai_reply:
            ai_reply = generate_placeholder_reply(user_message)
        return ChatResponse(reply=ai_reply)
    except Exception as exc:
        # Keep error messages friendly for frontend users.
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {exc}") from exc

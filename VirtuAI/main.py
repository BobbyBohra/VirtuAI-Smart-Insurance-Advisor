from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
from groq import Groq, AuthenticationError, RateLimitError
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="VirtuAI Insurance Advisor API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SYSTEM_PROMPT = """You are VirtuAI  — a Smart Insurance Advisor AI with deep expertise in all types of insurance: Health, Life, Motor/Car, Home, Travel, Term Life, ULIP, and Endowment Plans.

Your role:
- Help users understand insurance products in simple, clear language (Hindi/English/Hinglish all welcome)
- Recommend suitable insurance plans based on age, income, family size, and needs
- Explain premiums, coverage, exclusions, claim processes, and policy terms
- Compare plans from real insurers: LIC, HDFC Life, SBI Life, ICICI Prudential, Star Health, Bajaj Allianz, ICICI Lombard, New India Assurance, Tata AIG
- Explain tax benefits under Section 80C (life insurance) and Section 80D (health insurance)
- Help users understand what is covered and what is NOT covered
- Assist with claim-related queries
- Explain IRDAI regulations when relevant

Response format:
- Use bullet points and structured responses for clarity
- Use plain text only — do not use **asterisks** or any markdown formatting for bold or italics
- For premium estimates, always give a range with a note that exact quotes need personal details
- End serious recommendations with a short disclaimer

Important: You cover the Indian insurance market primarily. Be empathetic — insurance is confusing for most people.

Always add this disclaimer when making specific recommendations:
⚠️ Disclaimer: Yeh general guidance hai. Final decision se pehle IRDAI-registered advisor se milein."""

class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


class ChatResponse(BaseModel):
    reply: str
    tokens_used: int


@app.get("/")
async def root():
    """Serve the frontend index.html if it exists, otherwise show API status."""
    index_path = "static/index.html"
    if not os.path.exists(index_path):
        return HTMLResponse(
            "<h1>ShieldSense API is running</h1><p>Frontend not yet deployed. Please add static/index.html</p>",
            status_code=200
        )
    return FileResponse(index_path)


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="GROQ_API_KEY not set. Please set it in your .env file."
        )

    client = Groq(api_key=api_key)

    try:
        messages = [{"role": m.role, "content": m.content} for m in request.messages]

        # ✅ Updated to a currently supported model
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",   # Changed from decommissioned model
            max_tokens=1024,
            temperature=0.7,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *messages
            ],
        )

        reply_text = response.choices[0].message.content
        tokens = response.usage.total_tokens

        return ChatResponse(reply=reply_text, tokens_used=tokens)

    except AuthenticationError:
        raise HTTPException(status_code=401, detail="Invalid Groq API key.")
    except RateLimitError:
        raise HTTPException(status_code=429, detail="Rate limit hit. Please wait a moment.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "model": "llama-3.3-70b-versatile",   # Updated
        "service": "VirtuAI Insurance Advisor"
    }


# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")
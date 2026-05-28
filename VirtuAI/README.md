# 🛡️ VirtuAI — Smart Insurance Advisor Chatbot

Full-stack AI chatbot | **Python (FastAPI) backend** + **HTML/CSS/JS frontend**

---

## 📁 Project Structure

```
insurance_advisor/
├── main.py              ← Python FastAPI backend
├── requirements.txt     ← Python dependencies
├── .env.example         ← Environment variables template
└── static/
    └── index.html       ← Frontend (HTML + CSS + JS)
```

---

## ⚡ Quick Start

### Step 1 — Clone & Install

```bash
pip install -r requirements.txt
```

### Step 2 — Set API Key

```bash
cp .env.example .env
# Edit .env and add your Groq API key
```

Or set directly:
```bash
export GROQ_API_KEY=sk-ant-...
```

### Step 3 — Run Server

```bash
uvicorn main:app --reload --port 8000
```

### Step 4 — Open Browser

```
http://localhost:8000
```

---

## 🔌 API Endpoints

| Method | Endpoint  | Description              |
|--------|-----------|--------------------------|
| GET    | `/`       | Serve frontend HTML      |
| POST   | `/chat`   | Send message, get reply  |
| GET    | `/health` | Server health check      |

### POST /chat — Request Body

```json
{
  "messages": [
    { "role": "user", "content": "Health insurance ke liye kya dekhna chahiye?" }
  ]
}
```

### POST /chat — Response

```json
{
  "reply": "Health insurance chunte waqt in baaton ka dhyan rakhein...",
  "tokens_used": 342
}
```

---

## 🧠 Tech Stack

| Layer     | Technology                        |
|-----------|---------------------------------- |
| Backend   | Python 3.10+ / FastAPI            |
| AI Model  |  Groq (`llama-3.3-70b-versatile`) |
| Frontend  | Vanilla HTML/CSS/JS               |
| Server    | Uvicorn (ASGI)                    |

---

## 💡 Features

- Multi-turn conversation memory
- Insurance-specific system prompt (India market)
- LIC, HDFC Life, Star Health, Bajaj Allianz etc.
- Tax benefit guidance (80C, 80D)
- Token usage tracking
- Sidebar with quick insurance categories

---

## 🚀 Interview Talking Points

1. **REST API design** — FastAPI with Pydantic models
2. **LLM integration** — Anthropic SDK, system prompts
3. **Conversational AI** — full message history for context
4. **Domain AI** — specialized prompt for insurance advisory
5. **CORS + Static file serving** — production-ready setup

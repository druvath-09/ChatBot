# WebAura AI Chatbot 🤖

A full-stack AI-powered chatbot for **WebAura**, a web development agency. The chatbot helps customers learn about services, pricing, and how to get in touch — all through a sleek, modern chat interface.

---

## ✨ Features

- 💬 Real-time chat interface with message history
- 🧠 AI-powered responses via NVIDIA's Qwen 3.5-122B model
- 🔄 Graceful fallback to placeholder responses when the API is unavailable
- 🎨 Modern, responsive UI with animations and glassmorphism styling
- 📱 Mobile-friendly design

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python · FastAPI · Uvicorn |
| Frontend | HTML5 · CSS3 · Vanilla JavaScript |
| AI / LLM | NVIDIA AI Foundation API (Qwen 3.5-122B) |
| Validation | Pydantic v2 |

---

## 📂 Project Structure

```
ChatBot/
├── main.py           # FastAPI backend — chat endpoint & NVIDIA API integration
├── requirements.txt  # Python dependencies
├── .gitignore        # Ignored files (venv, .env, __pycache__, etc.)
└── static/
    └── index.html    # Frontend — HTML, CSS, and JavaScript (all-in-one)
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or later
- A free [NVIDIA AI Foundation API key](https://build.nvidia.com/)

### 1. Clone the repository

```bash
git clone https://github.com/druvath-09/ChatBot.git
cd ChatBot
```

### 2. Create and activate a virtual environment

```bash
# Linux / macOS
python -m venv venv
source venv/bin/activate

# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your NVIDIA API key

The application requires an `NVIDIA_API_KEY` environment variable to call the AI model.

```bash
# Linux / macOS
export NVIDIA_API_KEY="nvapi-xxxxxxxxxxxxxxxxxxxx"

# Windows (PowerShell)
$env:NVIDIA_API_KEY = "nvapi-xxxxxxxxxxxxxxxxxxxx"
```

> **Tip:** You can also create a `.env` file in the project root (already excluded by `.gitignore`):
> ```
> NVIDIA_API_KEY=nvapi-xxxxxxxxxxxxxxxxxxxx
> ```

> **Note:** If the API key is not set, the app still starts — it will return placeholder responses instead of AI-generated ones.

### 5. Run the server

```bash
uvicorn main:app --reload
```

Then open your browser and go to **[http://localhost:8000](http://localhost:8000)**.

---

## 🔌 API Endpoints

### `GET /`
Serves the chat interface (HTML frontend).

### `POST /chat`
Accepts a user message and returns an AI-generated reply.

**Request body:**
```json
{
  "message": "What services do you offer?"
}
```

**Response:**
```json
{
  "reply": "WebAura offers website design, web app development, and ongoing support..."
}
```

**Error responses:**

| Status | Reason |
|--------|--------|
| `400` | Empty or missing message |
| `500` | Internal server or API error |

---

## 🌐 Deployment

For production deployments, remove the `--reload` flag and bind to all interfaces:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## 📄 License

This project is open source. Feel free to use and adapt it for your own projects.

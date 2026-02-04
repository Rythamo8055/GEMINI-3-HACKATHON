# ARTHIV AI Interview Platform 🎙️

> **Gemini 3 Hackathon Submission** - AI-Powered Interview Platform with Secure Rate Limiting

[![Made with Gemini](https://img.shields.io/badge/Made%20with-Gemini%203-blue)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)

## 🚀 Overview

ARTHIV is an AI-powered interview platform that conducts realistic, adaptive interviews using **Gemini 3** multimodal capabilities. The platform features real-time voice conversations, resume analysis, and comprehensive session reports.

## ✨ Gemini 3 Features Used

### Backend (Python + Google ADK)
- **Gemini 3 Flash Native Audio** - Real-time bidirectional voice streaming
- **Proactive Audio Mode** - AI can speak without waiting for user input
- **Affective Dialog** - Emotionally aware conversation responses
- **Multimodal Input** - Analyzes resumes (PDF/images) and video frames
- **Context Window Compression** - Sliding window for long interview sessions

### Frontend (Next.js + TypeScript)
- **Real-time WebSocket Communication** - Low-latency audio streaming
- **Device Proctoring** - Camera/microphone permission handling
- **Session Persistence** - IndexedDB for offline-first experience

## 🛡️ Security Features

### Rate Limiting (8 Sessions per Device)
- Device fingerprinting using IP + User-Agent hash
- Maximum 8 concurrent sessions per device
- Automatic session cleanup on disconnect

## 📦 Project Structure

```
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application with rate limiting
│   │   ├── rate_limiter.py      # Secure session rate limiting
│   │   ├── agents/              # AI agent implementations
│   │   │   ├── review_agent.py  # Resume analyzer
│   │   │   └── vigilance_agent.py
│   │   └── google_search_agent/ # Core interview agent
│   ├── Dockerfile
│   └── pyproject.toml
│
├── frontend/
│   ├── app/                     # Next.js app router
│   ├── components/              # React components
│   ├── hooks/                   # Custom React hooks
│   ├── lib/                     # Utility libraries
│   └── Dockerfile
│
└── deploy_hackathon.sh          # GCP Cloud Run deployment
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- Google API Key with Gemini access

### Backend Setup
```bash
cd backend
pip install uv
uv sync
echo "GOOGLE_API_KEY=your_key_here" > app/.env
uv run uvicorn app.main:app --host 0.0.0.0 --port 8080
```

### Frontend Setup
```bash
cd frontend
npm install
echo "NEXT_PUBLIC_API_URL=http://localhost:8080" > .env.local
npm run dev
```

## 🐳 Docker Deployment

```bash
# Local development
docker-compose up --build

# GCP Cloud Run
./deploy_hackathon.sh
```

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/ws/{user_id}/{session_id}` | WebSocket | Main interview session |
| `/api/interview/plan` | POST | Generate interview plan |
| `/api/interview/plan-with-resume` | POST | Plan with resume upload |
| `/api/session/report` | POST | Generate session report |
| `/api/rate-limit/stats` | GET | Rate limiter statistics |

## 🔒 Rate Limiting

Each device is limited to **8 concurrent sessions** to prevent abuse:

```python
# Device fingerprint = SHA256(IP + User-Agent)
# Sessions tracked per device
# Automatic cleanup on disconnect
```

## 📄 License

Apache License 2.0 - See [LICENSE](LICENSE) for details.

---

**Built for the Gemini 3 Hackathon** 🏆

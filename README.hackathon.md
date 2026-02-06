# ARTHIV AI Interview Platform 🎙️

> **Gemini 3 Hackathon Submission** - Powered by **Google Gemini 3** & **Google Agent Development Kit (ADK)**

[![Made with Gemini](https://img.shields.io/badge/Made%20with-Gemini%203-blue?style=for-the-badge&logo=google-gemini)](https://ai.google.dev/)
[![Built with ADK](https://img.shields.io/badge/Built%20with-Google%20ADK-green?style=for-the-badge&logo=google)](https://github.com/google/generative-ai-python)
[![License](https://img.shields.io/badge/License-Apache%202.0-orange.svg?style=for-the-badge)](LICENSE)

## 🚀 Overview

**ARTHIV** leverages the cutting-edge capabilities of **Google's Gemini 3 Multimodal Live API** to deliver a seamless, real-time, and human-like interview experience. Built on the **Google Agent Development Kit (ADK)**, it redefines recruitment with proactive, emotionally intelligent AI agents.

## 🎮 Live Demo & Testing

| Service | Link | Description |
|---------|------|-------------|
| **Frontend App** | [**Launch Demo** 🚀](https://gemini3-hackathon-frontend-851412038318.us-central1.run.app) | Live interview interface |
| **Backend API** | [**API Docs**](https://gemini3-hackathon-backend-851412038318.us-central1.run.app/docs) | Swagger UI / ReDocs |
| **Judges Guide** | [**Testing Instructions**](JUDGES_GUIDE.md) | Step-by-step verification guide |

> **Note**: This hacked deployment uses a secure rate limiter (Max 8 sessions/device) to prevent abuse.

## 💎 Gemini 3 & Google ADK Features

### 🗣️ Native Audio & Voice (Gemini 3 Flash)
- **Zero-Latency Conversations**: Uses Gemini's native audio-in/audio-out capabilities for natural, real-time dialogue.
- **No External STT/TTS**: Direct end-to-end voice processing models for superior intonation and speed.

### 🧠 Proactive Intelligence (Google ADK)
- **Agentic Workflow**: The interviewer doesn't just wait for answers; it proactively guides the conversation.
- **Dynamic Questioning**: Generates follow-up questions based on real-time context, not static scripts.

### 🎭 Affective Dialog & Multimodal Analysis
- **Emotional Intelligence**: Detects user sentiment and adjusts voice tone (empathetic, professional, encouraging).
- **Vision Proctoring**: Real-time analysis of video frames to ensure integrity (detecting multiple faces, tab switching).
- **Resume Analysis**: Multimodal understanding of PDF/Image resumes to tailor technical questions.

### 💾 Efficient Context Management
- **Context Window Compression**: ADK-driven sliding window memory to handle long interview sessions without losing critical context.

## 🛡️ Security Features (Hackathon Special)

### Secure Rate Limiting
To ensure fair usage during the hackathon, we implemented a custom rate limiter:
- **Max 8 Concurrent Sessions** per device.
- **Device Fingerprinting**: SHA-256 hash of `IP Address` + `User-Agent`.
- **Automatic Cleanup**: Stale sessions are removed instantly upon WebSocket disconnect.
- **Stats API**: Public endpoint `/api/rate-limit/stats` to verify system load.

## 📦 Project Structure

```
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app with Google ADK integration
│   │   ├── rate_limiter.py      # Custom rate limiting middleware
│   │   ├── agents/              # ADK Agent definitions
│   │   │   ├── review_agent.py  # Gemini Resume Analyzer
│   │   │   └── google_search_agent/ # Gemini Interviewer Agent
│   ├── Dockerfile
│   └── pyproject.toml
│
├── frontend/
│   ├── app/                     # Next.js 14 App Router
│   ├── components/              # React components (Shadcn UI)
│   ├── lib/                     # Audio processing utilities
│   └── deploy_hackathon.sh      # Cloud Run deployment script
```

## 🚀 Quick Start

### Backend (Python + ADK)
```bash
cd backend
pip install uv
uv sync
echo "GOOGLE_API_KEY=your_gemini_key_here" > app/.env
uv run uvicorn app.main:app --host 0.0.0.0 --port 8080
```

### Frontend (Next.js)
```bash
cd frontend
npm install
echo "NEXT_PUBLIC_API_URL=http://localhost:8080" > .env.local
npm run dev
```

## 🐳 Deployment (Google Cloud Run)

We use a separate deployment pipeline for the hackathon to ensure stability and security.

```bash
# Deploy both services to Cloud Run
./deploy_hackathon.sh
```

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/ws/{user_id}/{session_id}` | WebSocket | **Gemini Live Session** |
| `/api/rate-limit/stats` | GET | View active session counts |
| `/api/interview/plan-with-resume` | POST | Analyze resume with Gemini Vision |

## 📄 License

Apache License 2.0 - See [LICENSE](LICENSE) for details.

---

**Built with ❤️ using Google Gemini 3** 🏆

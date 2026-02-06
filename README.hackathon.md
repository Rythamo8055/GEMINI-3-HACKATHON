# ARTHIV: The Future of AI Recruitment 🎙️

> **Gemini 3 Hackathon Submission** - Powered by **Google Gemini 3** & **Google Agent Development Kit (ADK)**

[![Made with Gemini](https://img.shields.io/badge/Made%20with-Gemini%203-blue?style=for-the-badge&logo=google-gemini)](https://ai.google.dev/)
[![Built with ADK](https://img.shields.io/badge/Built%20with-Google%20ADK-green?style=for-the-badge&logo=google)](https://github.com/google/generative-ai-python)
[![License](https://img.shields.io/badge/License-Apache%202.0-orange.svg?style=for-the-badge)](LICENSE)

---

## 📖 The Story

Hiring is broken. Candidates are anxious, recruiters are overwhelmed, and traditional "AI interviews" feel robotic and scripted.

**Enter ARTHIV.**

We questioned: *What if an AI interviewer could actually "feel" the conversation? What if it could see your resume, understand your hesitation, and guide you like a real mentor?*

Built on the groundbreaking **Google Gemini 3 Multimodal Live API**, ARTHIV isn't just a chatbot. It's a proactive, emotionally intelligent recruiter that conducts real-time, human-like voice interviews. It laughs, it listens, it probes deeper when you're vague, and it encourages you when you're stuck.

This isn't just an interview; it's a conversation.

---

## 🎯 Use Cases

### 1. The Empathetic Technical Screen
Imagine a candidate struggling to explain a complex algorithm. Instead of failing them, ARTHIV notices their anxiety (via **Affective Dialog**) and says, *"Take a breath using the STAR method. Let's break it down together."*

### 2. Fraud-Proof Remote Hiring
With **Vision Proctoring**, ARTHIV "sees" the candidate's environment. If a candidate is constantly looking off-screen or multiple faces appear, ARTHIV flags it in real-time—ensuring integrity without invasive software.

### 3. Personalized Deep Dives
Upload a resume, and ARTHIV reads it instantly (**Multimodal Analysis**). It won't ask generic questions. It sees "Built an LLM agent" on your CV and asks, *"Tell me about the context window challenges you faced with that specific agent."*

---

## 🚀 Usage Guide

1.  **Enter the Lobby**: Choose your target role (e.g., "Senior Python Dev") and a technical topic.
2.  **Upload Context (Optional)**: Drop your resume (PDF/Image) for a tailored session.
3.  **Start the Interview**:
    *   **Speak Naturally**: No push-to-talk. Just talk. Interrupt it. It handles it.
    *   **Get Feedback**: Receive specific, actionable feedback on your answers instantly.

---

## 🔗 Access The Live Demo

Experience the future of hiring right now. No sign-up required (Open Access for Hackathon Judges & Testers).

| Service | Link | Description |
|---------|------|-------------|
| **🎙️ Launch App** | [**👉 Click Here to Start Interview**](https://gemini3-hackathon-frontend-851412038318.us-central1.run.app) | The full frontend experience |
| **🧪 Testers Guide** | [**Read Testing Instructions**](JUDGES_GUIDE.md) | Step-by-step guide for Judges |
| **📡 API Docs** | [**View Backend Swagger**](https://gemini3-hackathon-backend-851412038318.us-central1.run.app/docs) | For developers verifying endpoints |

> **⚠️ Hackathon Note**: To prevent abuse, we have implemented a **Rate Limiter**.
> *   **Max Sessions**: 8 concurrent sessions per device/IP.
> *   **Security**: Device fingerprinting is active.

---

## 🧪 Testers & Judges Guide (In-App)

For the best evaluation experience, try these "Secret" interactions:

1.  **The "Interruption" Test**: While ARTHIV is speaking, interrupt it mid-sentence with *"Wait, let me correct that."* -> Watch how seamlessly it stops and listens (Gemini 3 Native Audio).
2.  **The "Visual" Test**: Turn on your camera. Hold up a phone or pen. Ask *"What am I holding?"* or just verify that it alerts on distraction.
3.  **The "Stress" Test**: Sound confused or stressed in your voice. Listen to how ARTHIV shifts its tone to be more comforting.

*For full step-by-step test cases, see the [**JUDGES_GUIDE.md**](JUDGES_GUIDE.md).*

---

## 💎 Under The Hood: Google Tech Stack

We pushed the **Google Agent Development Kit (ADK)** to its limits:

### 🗣️ Gemini 3 Flash (Native Audio)
*   **Why**: We needed sub-500ms latency.
*   **How**: Direct Audio-to-Audio streaming. No more Text-to-Speech lag.

### 🧠 Google ADK (The Brain)
*   **State Management**: Complex interview states (Introduction -> Technical -> Behavioral -> Closing) managed via ADK's robust state machine.
*   **Tool Calling**: The agent autonomously decides when to "search" for a fact or "log" a proctoring violation.

### 🛡️ Security Architecture
*   **Custom Middleware**: Python FastAPI backend with a custom `rate_limiter.py` module using SHA-256 fingerprinting for secure, login-free access control.

---

## 📦 Project Structure

```bash
├── backend/ # Python FastAPI + Google ADK
│   ├── agents/ # Gemini Interviewer & Resume Agents
│   └── rate_limiter.py # Custom Security Middleware
├── frontend/ # Next.js 14 + Shadcn UI
│   ├── components/ # Reactive UI Components
│   └── lib/audio/ # Audio Worklets for Low-Latency Streaming
└── deploy_hackathon.sh # Cloud Run Deployment Pipeline
```

---

## 📄 License & Credits

*   **License**: Apache 2.0
*   **Built for**: Google Gemini 3 Hackathon 2025

**Made with ❤️ by Rythamo**

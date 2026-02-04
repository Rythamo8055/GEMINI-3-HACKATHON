# 👨‍⚖️ Judges' Testing Guide - ARTHIV (Gemini 3 Hackathon)

Welcome to **ARTHIV**, an AI-powered recruiter agent built with **Google Gemini 3** and the **Google Agent Development Kit (ADK)**. 

This guide will help you verify the core capabilities of our submission.

---

## 🚀 Quick Access

- **Frontend App**: [Launch Demo](https://gemini3-hackathon-frontend-851412038318.us-central1.run.app) (Use Chrome/Edge/Arc)
- **Repo**: [GitHub](https://github.com/Rythamo8055/GEMINI-3-HACKATHON)
- **API Docs**: [Swagger UI](https://gemini3-hackathon-backend-851412038318.us-central1.run.app/docs)

---

## 🧪 Test Case 1: The "Gemini Live" Experience (Native Audio)
*Objective: Verify real-time, low-latency voice interaction and affective dialog.*

1. **Open the App**: Go to the [Frontend URL](https://gemini3-hackathon-frontend-851412038318.us-central1.run.app).
2. **Start Session**:
   - Enter a Role: e.g., "Senior Python Developer" or "Product Manager".
   - Enter a Topic: e.g., "System Design" or "Agile Methodologies".
   - Click **"Start Interview"**.
3. **Interact**:
   - Allow microphone permissions.
   - **Speak naturally**: Interrupt the agent, change topics slightly, or ask for clarification.
   - **Verify**:
     - ✅ **Zero Latency**: Notice the immediate response (powered by Gemini 3 Native Audio).
     - ✅ **Emotion**: If you sound confused, the agent should sound helpful. If you answer well, it should sound encouraging.
     - ✅ **Proactivity**: Stop speaking for a few seconds. The agent should proactively nudge you ("Are you still there?" or "Would you like me to rephrase that?").

---

## 🧪 Test Case 2: Multimodal Capabilities (Vision & Resume)
*Objective: Verify Gemini's ability to "see" and understand documents.*

1. **Resume Analysis**:
   - Refresh the page.
   - Click **"Upload Resume"** (PDF or Image).
   - Start the interview.
   - **Verify**: The agent will ask specific questions based on *your* uploaded resume content, not generic questions.
   
2. **Visual Proctoring** (Optional):
   - Enable "Camera" when starting.
   - **Action**: Look away from the screen or hold up a phone.
   - **Verify**: The system logs "Vigilance Alerts" (visible in Dev Mode or console) detecting your distraction.

---

## 🧪 Test Case 3: Hackathon Security (Rate Limiting)
*Objective: Verify the custom device-fingerprinting rate limiter.*

1. **Dashboard Check**: 
   - Open [Rate Limit Stats](https://gemini3-hackathon-backend-851412038318.us-central1.run.app/api/rate-limit/stats).
   - Note the `current_sessions` count.

2. **Trigger Limit**:
   - Open the [Frontend](https://gemini3-hackathon-frontend-851412038318.us-central1.run.app) in **9 separate tabs**.
   - Start an interview in each tab.
   - **Verify**: The 9th tab will fail to connect with a `Session limit reached (Max 8)` error.
   
3. **Cleanup**:
   - Close all tabs.
   - Refresh the [Stats Page](https://gemini3-hackathon-backend-851412038318.us-central1.run.app/api/rate-limit/stats).
   - **Verify**: `total_sessions` should drop back to 0 immediately.

---

## 💎 Key Technologies to Look For

| Feature | Tech Used | Why it matters |
|---------|-----------|----------------|
| **Voice** | **Gemini 3 Flash** | No transcription delay; end-to-end speech-to-speech. |
| **Reasoning** | **Google ADK** | State management, tool calling, and structured conversation flow. |
| **Security** | **Python/FastAPI** | Custom middleware for device fingerprinting without login. |

---

*Thank you for testing ARTHIV!* 🏆

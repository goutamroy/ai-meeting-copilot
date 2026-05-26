# AI Meeting Copilot – Backend

AI Meeting Copilot Backend is a production-oriented AI-powered meeting intelligence API built with FastAPI. It processes uploaded meeting audio, generates transcripts, summarizes discussions, extracts action items and key decisions, stores meeting history, and enables AI-driven Q&A over meeting content.

This backend is designed with cloud deployment, fault tolerance, and scalable API architecture in mind.

---

# Project Overview

The backend acts as the intelligence engine for the AI Meeting Copilot application.

It handles:

- Audio upload and processing
- Cloud storage integration
- Speech-to-text transcription
- AI-powered summarization
- Action item extraction
- Key decision extraction
- Meeting persistence
- AI chat over meeting context
- Meeting history retrieval
- Health monitoring
- Cloud deployment support

---

# Core Features

## 1. Audio Upload Pipeline
Users upload meeting audio files from the iOS app or API.

The backend:
- Validates file type
- Stores audio
- Uploads to Azure Blob Storage
- Triggers processing pipeline

Supported formats:
- `.wav`
- `.m4a`
- `.mp3`

---

## 2. Speech-to-Text Transcription
Meeting audio is transcribed using AI speech recognition.

Purpose:
- Convert spoken discussions into text
- Enable downstream NLP processing

Output:
- Transcript text

---

## 3. AI Meeting Summarization
The backend generates structured meeting summaries.

Extracts:
- Summary
- Action items
- Key decisions

This helps convert raw conversations into usable business insights.

---

## 4. AI Chat Over Meeting Context
Users can ask contextual questions about uploaded meetings.

Examples:
- What was discussed in the meeting?
- What were the next steps?
- What decisions were taken?
- What blockers were identified?

This creates a lightweight Retrieval-Augmented AI interaction.

---

## 5. Meeting History & Retrieval
Supports:
- Fetch all meetings
- Fetch meeting by ID
- Retrieve stored summaries
- Retrieve transcripts

---

## 6. Database Safe Fallback
If PostgreSQL becomes unavailable:

The application:
- Logs DB failure
- Prevents crash
- Returns controlled responses
- Continues processing where possible

This improves resiliency.

---

## 7. Cloud Deployment Ready
Backend is containerized and deployed for production testing.

Supports:
- AWS Elastic Beanstalk
- Docker deployment
- Azure integration

---

# Tech Stack

## Backend Framework
- FastAPI
- Uvicorn

## Language
- Python 3.11

## Database
- PostgreSQL
- SQLAlchemy ORM

## AI / NLP
- Whisper transcription
- LLM-based summarization
- Context-aware AI chat

## Vector Storage
- Pinecone

## Cloud & Storage
- Azure Blob Storage
- AWS Elastic Beanstalk

## Containerization
- Docker

---

# Architecture Flow

```text
Client / iOS App
      ↓
Audio Upload API
      ↓
Validation Layer
      ↓
Azure Blob Storage Upload
      ↓
Speech-to-Text (Whisper)
      ↓
Summarization Pipeline
      ↓
Action Item Extraction
      ↓
Decision Extraction
      ↓
Pinecone Embedding Storage
      ↓
PostgreSQL Persistence
      ↓
Chat / Retrieval APIs
API Endpoints
Health Check
GET /health

Checks backend health.

API Documentation
GET /docs

Swagger UI for testing APIs.

Upload Meeting Audio
POST /upload

Processes uploaded audio and stores meeting intelligence.

Returns:

Transcript
Summary
Action items
Key decisions
Meeting ID
Chat With Meeting
POST /chat

Allows AI-based Q&A using meeting context.

Input:

meeting_id
question

Output:

AI response
Fetch All Meetings
GET /meetings

Returns all stored meetings.

Fetch Single Meeting
GET /meetings/{meeting_id}

Returns detailed meeting data.

Chat History
GET /chat-history/{meeting_id}

Returns historical chat interactions.

Project Structure
backend/
│
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── upload.py
│   │       ├── chat.py
│   │
│   ├── services/
│   │   ├── meeting_pipeline.py
│   │   ├── summary.py
│   │   ├── pinecone_service.py
│   │
│   ├── core/
│   │   ├── settings.py
│   │   ├── logger.py
│   │   ├── exceptions.py
│   │
│   ├── database.py
│   ├── models.py
│   └── main.py
│
├── Dockerfile
├── requirements.txt
└── Dockerrun.aws.json
Environment Variables

Example configuration:

DATABASE_URL=
AZURE_STORAGE_CONNECTION_STRING=
AZURE_CONTAINER_NAME=
OPENAI_API_KEY=
PINECONE_API_KEY=
PINECONE_INDEX_NAME=
Local Setup
Clone
git clone https://github.com/goutamroy/ai-meeting-copilot.git
Create Virtual Environment
python3 -m venv venv
source venv/bin/activate
Install Dependencies
pip install -r requirements.txt
Run Server
uvicorn app.main:app --reload

Local Swagger:

http://127.0.0.1:8000/docs
Docker Deployment

Build:

docker build -t ai-meeting-backend .

Run:

docker run -p 8000:8000 ai-meeting-backend
AWS Deployment

Deployed using:

Docker image
Elastic Beanstalk
Dockerrun.aws.json
Environment variable configuration
Reliability & Engineering Practices

Implemented:

Modular service-based architecture
Exception handling
DB fallback handling
Cloud-first design
API validation
Structured logging
Containerized deployment
Separation of concerns
Use Cases

This system can be extended for:

Meeting assistants
Enterprise meeting intelligence
Voice note summarization
AI note generation
Team productivity tools
Customer support transcript analysis
Future Enhancements

Planned improvements:

Authentication / JWT
Role-based access
Multi-user meeting ownership
Advanced semantic retrieval
Real-time streaming transcription
Sentiment analysis
Speaker diarization
Dashboard analytics
Author

Goutam Roy
Senior iOS Engineer | AI/ML Enthusiast | Backend Integration | Cloud Deployment | FastAPI | SwiftUI | AWS | Azure

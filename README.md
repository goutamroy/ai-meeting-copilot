# AI Meeting Copilot – Backend

AI Meeting Copilot Backend is a production-oriented AI-powered meeting intelligence API built with FastAPI. It processes uploaded meeting audio, generates transcripts, summarizes discussions, extracts action items and key decisions, stores meeting history, and enables AI-driven Q&A over meeting content.

The backend is designed with cloud deployment, scalable API architecture, modular services, and production-style engineering practices.

---

# Project Overview

The backend acts as the intelligence engine for the AI Meeting Copilot platform.

It handles:

* Audio upload and processing
* Cloud storage integration
* Speech-to-text transcription
* AI-powered summarization
* Action item extraction
* Key decision extraction
* Meeting persistence
* AI chat over meeting context
* Meeting history retrieval
* Health monitoring
* Cloud deployment support

---

# Core Features

## 1. Audio Upload Pipeline

Users upload meeting audio files from the iOS application or API clients.

The backend:

* Validates file type
* Stores audio
* Uploads files to Azure Blob Storage
* Triggers AI processing pipeline

Supported formats:

* `.wav`
* `.m4a`
* `.mp3`

---

## 2. Speech-to-Text Transcription

Meeting audio is transcribed using AI speech recognition.

Purpose:

* Convert spoken discussions into text
* Enable downstream NLP processing

Output:

* Transcript text

---

## 3. AI Meeting Summarization

The backend generates structured meeting intelligence.

Extracts:

* Summary
* Action items
* Key decisions

This converts raw conversations into usable business insights.

---

## 4. AI Chat Over Meeting Context

Users can ask contextual questions about uploaded meetings.

Example questions:

* What was discussed in the meeting?
* What were the next steps?
* What decisions were taken?
* Were blockers identified?

This creates a lightweight Retrieval-Augmented AI interaction experience.

---

## 5. Meeting History & Retrieval

Supports:

* Fetch all meetings
* Fetch meeting by ID
* Retrieve summaries
* Retrieve transcripts
* Retrieve chat history

---

## 6. Database Safe Fallback

If PostgreSQL becomes unavailable:

The application:

* Logs DB failures
* Prevents application crashes
* Returns controlled responses
* Continues processing where possible

This improves backend resiliency.

---

## 7. Cloud Deployment Ready

The backend is containerized and deployed for production-style testing.

Supports:

* AWS Elastic Beanstalk
* Docker deployment
* Azure integration

---

# Tech Stack

## Backend Framework

* FastAPI
* Uvicorn

## Language

* Python 3.11

## Database

* PostgreSQL
* SQLAlchemy ORM

## AI / NLP

* Whisper transcription
* LLM-based summarization
* Context-aware AI chat

## Vector Storage

* Pinecone

## Cloud & Storage

* Azure Blob Storage
* AWS Elastic Beanstalk

## Containerization

* Docker

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
```

---

# API Endpoints

## Health Check

```http
GET /health
```

Checks backend health.

---

## API Documentation

```http
GET /docs
```

Swagger UI for API testing.

---

## Upload Meeting Audio

```http
POST /upload
```

Processes uploaded audio and stores meeting intelligence.

Returns:

* Transcript
* Summary
* Action items
* Key decisions
* Meeting ID

---

## Chat With Meeting

```http
POST /chat
```

Allows AI-based Q&A using meeting context.

Input:

* `meeting_id`
* `question`

Output:

* AI response

---

## Fetch All Meetings

```http
GET /meetings
```

Returns all stored meetings.

---

## Fetch Single Meeting

```http
GET /meetings/{meeting_id}
```

Returns detailed meeting data.

---

## Chat History

```http
GET /chat-history/{meeting_id}
```

Returns historical chat interactions.

---

# Project Structure

```text
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
```

---

# Environment Variables

Example configuration:

```env
DATABASE_URL=
AZURE_STORAGE_CONNECTION_STRING=
AZURE_CONTAINER_NAME=
OPENAI_API_KEY=
PINECONE_API_KEY=
PINECONE_INDEX_NAME=
```

---

# Local Setup

## Clone Repository

```bash
git clone https://github.com/goutamroy/ai-meeting-copilot.git
```

---

## Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Server

```bash
uvicorn app.main:app --reload
```

---

## Local Swagger

```text
http://127.0.0.1:8000/docs
```

---

# Docker Deployment

## Build Docker Image

```bash
docker build -t ai-meeting-backend .
```

---

## Run Docker Container

```bash
docker run -p 8000:8000 ai-meeting-backend
```

---

# AWS Deployment

Deployed using:

* Docker image
* AWS Elastic Beanstalk
* Dockerrun.aws.json
* Environment variable configuration

---

# Live Backend Deployment

Production Backend:

http://ai-meeting-copilot-env.eba-4m9cjwwy.eu-north-1.elasticbeanstalk.com

Swagger API Docs:

http://ai-meeting-copilot-env.eba-4m9cjwwy.eu-north-1.elasticbeanstalk.com/docs

---

# iOS Application Repository

https://github.com/goutamroy/ai-meeting-copilot-ios

---

# Reliability & Engineering Practices

Implemented:

* Modular service-based architecture
* Exception handling
* DB fallback handling
* Cloud-first design
* API validation
* Structured logging
* Containerized deployment
* Separation of concerns

---

# Use Cases

This system can be extended for:

* Meeting assistants
* Enterprise meeting intelligence
* Voice note summarization
* AI note generation
* Team productivity tools
* Customer support transcript analysis

---

# Future Enhancements

Planned improvements:

* Authentication / JWT
* Role-based access
* Multi-user meeting ownership
* Advanced semantic retrieval
* Real-time streaming transcription
* Sentiment analysis
* Speaker diarization
* Dashboard analytics

---

# Author

Goutam Roy

Senior iOS Engineer | AI/ML Enthusiast | Backend Integration | Cloud Deployment | FastAPI | SwiftUI | AWS | Azure

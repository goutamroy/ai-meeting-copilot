# AI Meeting Copilot – Backend

AI Meeting Copilot Backend is a production-oriented AI-powered meeting intelligence API built with FastAPI, Generative AI, and Retrieval-Augmented Generation (RAG). The platform processes uploaded meeting audio, generates transcripts, summarizes discussions, extracts action items and key decisions, stores meeting history, and enables contextual AI-powered Q&A over meeting conversations using semantic retrieval workflows.

The backend is designed with modular API architecture, AI orchestration workflows, vector embeddings, cloud deployment support, and production-style engineering practices.

---

# Project Overview

The backend acts as the AI intelligence and Retrieval-Augmented Generation (RAG) engine for the AI Meeting Copilot platform.

It handles:

* Audio upload and processing
* Cloud storage integration
* Speech-to-text transcription
* AI-powered summarization
* Action item extraction
* Key decision extraction
* Meeting persistence
* AI chat over meeting context
* Semantic retrieval workflows
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

Meeting audio is transcribed using AI speech recognition powered by Whisper.

Purpose:

* Convert spoken discussions into text
* Enable downstream NLP and Generative AI processing

Output:

* Transcript text

---

## 3. AI Meeting Summarization

The backend generates structured meeting intelligence using Generative AI workflows.

Extracts:

* Summary
* Action items
* Key decisions

This converts raw conversations into actionable business insights.

---

## 4. AI Chat Over Meeting Context (Generative AI + RAG)

Users can ask contextual questions about uploaded meetings using Generative AI and Retrieval-Augmented Generation (RAG) workflows.

The backend:

* Converts meeting transcripts into semantic embeddings
* Stores embeddings in Pinecone vector database
* Retrieves relevant meeting context using semantic similarity search
* Sends contextual prompts to the LLM for grounded AI responses

Example questions:

* What was discussed in the meeting?
* What were the next steps?
* What decisions were taken?
* Were blockers identified?

This creates a lightweight contextual AI assistant capable of semantic meeting retrieval and intelligent conversational interactions.

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

This improves backend reliability and fault tolerance.

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

## AI / Generative AI / NLP

* Whisper speech-to-text transcription
* LLM-based summarization
* Retrieval-Augmented Generation (RAG)
* Semantic embeddings
* Context-aware AI chat
* Prompt orchestration workflows

## Vector Database & Semantic Retrieval

* Pinecone vector database
* Semantic similarity search
* Contextual retrieval workflows

## Cloud & Storage

* Azure Blob Storage
* AWS Elastic Beanstalk

## Containerization

* Docker

---

# Architecture Flow

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
Semantic Embedding Generation
      ↓
Pinecone Vector Storage
      ↓
Retrieval-Augmented Generation (RAG)
      ↓
PostgreSQL Persistence
      ↓
Chat / Retrieval APIs
      ↓
Contextual AI Responses

---

# API Endpoints

## Health Check

GET `/health`

Checks backend health.

---

## API Documentation

GET `/docs`

Swagger UI for API testing.

---

## Upload Meeting Audio

POST `/upload`

Processes uploaded audio and stores meeting intelligence.

Returns:

* Transcript
* Summary
* Action items
* Key decisions
* Meeting ID

---

## Chat With Meeting

POST `/chat`

Allows AI-based Q&A using contextual meeting retrieval.

Input:

* meeting_id
* question

Output:

* AI response

---

## Fetch All Meetings

GET `/meetings`

Returns all stored meetings.

---

## Fetch Single Meeting

GET `/meetings/{meeting_id}`

Returns detailed meeting data.

---

## Chat History

GET `/chat-history/{meeting_id}`

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

DATABASE_URL=
AZURE_STORAGE_CONNECTION_STRING=
AZURE_CONTAINER_NAME=
OPENAI_API_KEY=
PINECONE_API_KEY=
PINECONE_INDEX_NAME=

---

# Local Setup

## Clone Repository

```bash
git clone https://github.com/goutamroy/ai-meeting-copilot.git
```

## Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Server

```bash
uvicorn app.main:app --reload
```

## Local Swagger

```bash
http://127.0.0.1:8000/docs
```

---

# Docker Deployment

## Build Docker Image

```bash
docker build -t ai-meeting-backend .
```

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

## Production Backend

http://ai-meeting-copilot-env.eba-4m9cjwwy.eu-north-1.elasticbeanstalk.com

## Swagger API Docs

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
* API validation
* Structured logging
* Containerized deployment
* Separation of concerns
* Structured backend processing workflows

---

# AI Architecture Highlights

* Generative AI-powered meeting intelligence workflows
* Retrieval-Augmented Generation (RAG) implementation
* Pinecone vector search integration
* Semantic embedding-based contextual retrieval
* Context-aware conversational AI interactions
* Modular FastAPI AI orchestration pipeline

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

Senior iOS Engineer | AI/ML Enthusiast | Backend Integration | FastAPI | SwiftUI | AWS | Azure

---

# About

FastAPI-based AI Meeting Copilot backend integrating Generative AI, RAG workflows, Whisper transcription, Pinecone vector search, PostgreSQL, Docker, Azure Blob Storage, and AWS Elastic Beanstalk deployment.

---

# Topics

python fastapi generative-ai rag llm pinecone vector-search semantic-search whisper postgresql docker aws azure backend ai

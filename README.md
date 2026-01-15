# 📞 ConvoxAI — AI-Powered Call Summarization using RAG

## 📌 Overview

**ConvoxAI** is an end-to-end **AI-based Call Summarization system** built using a **Retrieval-Augmented Generation (RAG)** pipeline. The system converts recorded customer calls into structured, accurate, and actionable summaries by combining **speech-to-text**, **vector-based retrieval**, **large language models**, and **sentiment analysis**.

ConvoxAI is designed for real-world applications such as **customer support analytics, CRM automation, quality assurance, and executive reporting**.

---

## 🧠 Key Features

- 🎙️ Speech-to-text conversion from call recordings  
- 📄 Context-aware call summarization  
- 🧠 Retrieval-Augmented Generation (RAG)  
- 📦 Vector storage and semantic search using Pinecone  
- 😊 Customer sentiment analysis  
- 📋 Action item and risk identification  
- 🔒 Hallucination-controlled summaries  
- 🚀 Scalable and modular pipeline  

---

## 📁 Project Structure

ConvoxAI follows a **production-level package structure** with clear separation of concerns:

```
Backend/
├── convoxai/                      # Main application package
│   ├── __init__.py               # Package initialization
│   ├── config.py                 # Centralized configuration
│   │
│   ├── api/                      # API layer (FastAPI)
│   │   ├── __init__.py
│   │   └── app.py                # FastAPI application & endpoints
│   │
│   ├── core/                     # Core business logic
│   │   ├── __init__.py
│   │   ├── models.py             # Pydantic data models
│   │   └── summarizer.py         # Summarization engine
│   │
│   ├── prompts/                  # LLM prompt templates
│   │   ├── __init__.py
│   │   └── templates.py          # Prompt templates
│   │
│   └── utils/                    # Utility modules
│       ├── __init__.py
│       ├── audio.py              # Audio processing (Whisper)
│       ├── embeddings.py         # Embedding generation
│       ├── text_processing.py    # Text chunking & splitting
│       └── vector_store.py       # Pinecone vector operations
│
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── test_api.py               # API endpoint tests
│   ├── test_audio.py             # Audio processing tests
│   └── test_summarizer.py        # Summarization tests
│
├── data/                         # Data directory
│   └── sample_testing.wav        # Sample audio files
│
├── scripts/                      # Utility scripts
│   └── run_dev.py                # Development server runner
│
├── .env                          # Environment variables (API keys)
├── .gitignore                    # Git ignore patterns
├── requirements.txt              # Python dependencies
├── setup.py                      # Package installation config
├── LICENSE                       # Apache 2.0 License
└── README.md                     # This file
```

### 📦 Package Organization

| Directory | Purpose | Key Files |
|-----------|---------|-----------|
| **`convoxai/api/`** | REST API endpoints and FastAPI application | `app.py` |
| **`convoxai/core/`** | Core summarization logic and data models | `summarizer.py`, `models.py` |
| **`convoxai/prompts/`** | LLM prompt templates and management | `templates.py` |
| **`convoxai/utils/`** | Reusable utilities (audio, embeddings, vector DB) | `audio.py`, `vector_store.py` |
| **`tests/`** | Unit and integration tests | `test_*.py` |
| **`data/`** | Sample audio files and test data | `*.wav` |
| **`scripts/`** | Development and deployment scripts | `run_dev.py` |

### 🔧 Key Configuration Files

- **`convoxai/config.py`** - Centralized configuration (API keys, model settings, chunk sizes)
- **`.env`** - Environment variables (Gemini API Key, Pinecone API Key)
- **`requirements.txt`** - Python package dependencies
- **`setup.py`** - Package installation and metadata
---


## 🧩 Technology Stack

| Component | Technology |
|--------|------------|
| Speech-to-Text | OpenAI Whisper |
| LLMs | Gemini API, Groq API |
| Embeddings | HuggingFace Transformers |
| Vector Database | Pinecone |
| RAG | Custom / LangChain-compatible |
| Language | Python |

---

## 🔄 Workflow Explanation

1. **Audio Input**  
   Customer call recordings are provided in `.wav` or `.mp3` format.

2. **Speech Recognition**  
   Whisper converts audio into text transcripts.

3. **Transcript Chunking**  
   Long transcripts are split into semantically meaningful chunks.

4. **Vector Embedding**  
   HuggingFace models generate dense embeddings from transcript chunks.

5. **Vector Storage & Retrieval**  
   Embeddings are stored in Pinecone and retrieved based on semantic similarity.

6. **RAG-based Summarization**  
   Gemini or Groq LLM generates summaries using transcript + retrieved context.

7. **Sentiment Analysis**  
   Overall customer sentiment is inferred from conversation tone and language.

---

## 📑 Output Structure

The generated output includes:

- **Call Summary** – High-level overview of the conversation  
- **Participants & Roles** – Agent / Customer (if identifiable)  
- **Customer Intent** – Primary and secondary objectives  
- **Key Resolutions** – Issues resolved during the call  
- **Action Items** – Next steps with ownership and deadlines  
- **Risks / Escalations** – Compliance or dissatisfaction signals  
- **Sentiment Analysis** – Positive / Neutral / Negative  
- **Insights & Recommendations** – Business and process-level insights  

---

## 😊 Sentiment Analysis

ConvoxAI performs **context-aware sentiment analysis** based on:
- Language tone and word choice  
- Expressions of satisfaction, frustration, or concern  
- Repeated complaints or positive affirmations  

Sentiment is classified as:
- **Positive**
- **Neutral**
- **Negative**

This helps organizations:
- Monitor customer satisfaction  
- Detect escalation risks early  
- Improve agent performance and service quality  

---

## 🔐 Hallucination Control

To ensure reliability and trustworthiness:
- The model uses **only the transcript and retrieved context**
- Missing or unclear information is explicitly stated
- No assumptions or fabricated details are generated

---

## ⚙️ Installation & Setup

```bash
git clone the repository 
cd ConvoxAI
pip install -r requirements.txt

# Video2Audio Summarizer

An AI-powered NLP pipeline for video transcription, semantic summarization, and question generation.

The system processes uploaded videos by extracting audio, transcribing speech using Whisper, semantically segmenting the transcript using embeddings, generating summaries, and creating question-answer pairs using a trained T5-based machine learning model.

---

# Features

- Video and audio upload support
- Audio extraction using FFmpeg
- Speech-to-text transcription with Whisper
- Audio chunking for long videos
- Transcript cleaning and overlap merging
- Semantic segmentation using embeddings
- AI-generated summaries
- ML-based question generation using T5
- SQLite database integration
- Export functionality
- Modular backend architecture

---

# Project Architecture

```text
S4/
│
├── backend/
│   ├── exports/
│   ├── models/
│   ├── uploads/
│   ├── database.py
│   ├── export.py
│   ├── main.py
│   ├── pipeline.py
│   ├── qa_generator.py
│   ├── summarizer.py
│   └── video2summary.db
│
├── src/
│   ├── transcription/
│   │   ├── semantic/
│   │   │   ├── embedder.py
│   │   │   ├── semantic_segmenter.py
│   │   │   ├── similarity.py
│   │   │   └── summarizer.py
│   │   │
│   │   ├── audio_handler.py
│   │   ├── audio_utils.py
│   │   ├── chunker.py
│   │   ├── cleaner.py
│   │   ├── input_handler.py
│   │   ├── merger.py
│   │   ├── segmenter.py
│   │   ├── transcription_service.py
│   │   └── whisper_model.py
│   │
│   ├── utils/
│   └── test_embedder.py
│
├── frontend/
│   └── index.html
│
├── tests/
│
├── Training_model/
│   └── video2qa_t5base.py
│
└── venv/
```

---

# System Workflow

```text
Video Upload
      ↓
Audio Extraction
      ↓
Audio Chunking
      ↓
Whisper Transcription
      ↓
Transcript Cleaning
      ↓
Overlap Merging
      ↓
Semantic Segmentation
      ↓
Summarization
      ↓
Question Generation (T5 Model)
      ↓
Export & Storage
```

---

# Technologies Used

## Backend
- Python
- FastAPI
- Uvicorn
- SQLite

## AI / NLP
- OpenAI Whisper
- Sentence Transformers
- Transformers
- T5
- NumPy

## Audio Processing
- FFmpeg

## Frontend
- HTML
- JavaScript

---

# Core Components

## Whisper Transcription

The system uses OpenAI Whisper for speech recognition and transcription. Long audio files are divided into chunks to improve memory efficiency and processing stability.

---

## Semantic Segmentation

The transcript is grouped according to semantic similarity instead of only timestamps or fixed sentence counts.

This improves:
- topic coherence
- contextual grouping
- summary quality

---

## Overlap Merging

Chunked transcription may create duplicated words between neighboring audio chunks.

The merger module removes duplicated overlap while preserving sentence continuity.

---

## ML-Based Question Generation

The system includes a trained T5-based machine learning model for automatic question generation.

The model was trained on datasets containing natural question-answer patterns, allowing it to generate context-aware educational questions from summarized content.

This makes the system useful for:
- educational platforms
- lecture summarization
- revision systems
- learning assistance
- content understanding

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/your-username/video2audio-summarizer.git
cd video2audio-summarizer
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

### Install FastAPI and Uvicorn

```bash
pip install fastapi uvicorn
```

### Install Additional Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Install FFmpeg

FFmpeg is required for audio extraction.

### Windows
Download FFmpeg and add it to the system PATH.

### Linux

```bash
sudo apt install ffmpeg
```

### macOS

```bash
brew install ffmpeg
```

---

# Running the Project

## Start Backend Server

From the `backend` directory:

```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

The API server will run at:

```text
http://127.0.0.1:8000
```

---

## Open Frontend

Open:

```text
frontend/index.html
```

in your browser.

---

# Example Output

## Input
- Lecture video (.mp4)

## Output
- Full transcript
- Semantic summary
- Generated questions
- Exported files

---

# Future Improvements

- Real-time transcription
- Speaker diarization
- Multi-language summarization
- Improved frontend interface
- Hosting

---

# Educational Purpose

This project was developed to explore:
- speech recognition systems
- NLP pipelines
- semantic text processing
- AI summarization techniques
- machine learning for question generation
- modular software architecture

---

# License

MIT License

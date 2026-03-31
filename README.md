# Video2Summary — Modular Transcription Pipeline

A modular pipeline that transforms video content into structured text through a sequence of well-defined processing stages.

---

## Project Overview

The system follows a clear processing flow:

```
VIDEO → AUDIO → CHUNKS → TRANSCRIPTION → FINAL TEXT
```

Each stage is implemented as an independent module to ensure:

- Separation of concerns
- Ease of testing and debugging
- Scalability for future features
- Maintainable and extensible architecture

The goal is to build the pipeline step by step, with a strong focus on correctness and understanding at each stage.

---

## System Architecture

```
S4/
│
├── src/
│   ├── transcription/
│   │   ├── __init__.py
│   │   ├── audio_extractor.py   # Video → Audio
│   │   ├── chunker.py           # Audio → Chunks
│   │   └── whisper_model.py     # (planned) Chunks → Text
│   │
│   └── main.py                  # Entry point
│
├── data/
│   ├── test.mp4                 # Input video
│   ├── test.wav                 # Extracted audio
│   └── chunks/                  # Generated chunks
│
├── venv/
├── requirements.txt
├── .env
└── config.py
```

---

## Pipeline Components

### Audio Extraction

**File:** `src/transcription/audio_extractor.py`

Converts a video file into a `.wav` audio file optimized for speech processing.

- Ensures mono audio (1 channel)
- Uses 16kHz sampling rate
- Handles file existence and FFmpeg errors

```python
extract_audio(video_path: str) -> str
```

---

### Audio Chunking

**File:** `src/transcription/chunker.py`

Splits audio into smaller overlapping segments.

**Purpose:**
- Improve processing reliability for long audio
- Reduce memory constraints
- Prepare data for transcription models

**Key features:**
- Configurable chunk duration
- Overlap between segments
- Sequential chunk generation

```python
split_audio(audio_path: str, chunk_duration=60, overlap=10) -> List[str]
```

---

### Transcription *(Planned)*

**File:** `src/transcription/whisper_model.py`

This module will:
- Load a speech-to-text model
- Process audio chunks independently
- Combine outputs into a final transcript

---

## How to Run

### 1. Create and activate environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Execute the pipeline

```bash
python src/main.py
```

---

## Entry Point

**File:** `src/main.py`

```python
from transcription.audio_extractor import extract_audio
from transcription.chunker import split_audio

if __name__ == "__main__":
    video_path = "data/test.mp4"

    audio_path = extract_audio(video_path)
    print("Audio:", audio_path)

    chunks = split_audio(audio_path)
    print("Chunks:")
    for c in chunks:
        print(c)
```

---

## Design Principles

- Modular structure with clear responsibilities
- Explicit and readable code
- Incremental development
- Focus on understanding before optimization

---

## Requirements

- Python 3.9+
- FFmpeg installed and available in `PATH`

---

> This project is under active development.  
> The architecture is designed to evolve while preserving clarity and modularity.

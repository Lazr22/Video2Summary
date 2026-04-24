# Video2Summary

A full-stack video summarization app with FastAPI backend and polished HTML frontend.

## Project Structure

```
Video2Summary/
├── backend/
│   ├── main.py          ← FastAPI app 
│   ├── pipeline.py      ← Video→Audio→Transcription (teammate 2)
│   ├── summarizer.py    ← Trained model (teammate 1)
│   ├── database.py      ← SQLite history
│   ├── export.py        ← TXT & PDF export
│   └── requirements.txt
└── frontend/
    └── index.html       ← Full UI (open in browser)
```

---

## Setup & Run

### 1. Install dependencies
```bash
cd backend
pip install -r requirements.txt
pip install yt-dlp      # for YouTube feature
```

### 2. Start the backend
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### 3. Open the frontend
Just open `frontend/index.html` in Chrome. Done!

---

## Features
- Upload video file (MP4, MOV, AVI, MKV, WEBM)
- Paste YouTube URL to auto-download and summarize
- Live progress steps (audio extract → chunk → transcribe → summarize)
- Side-by-side Summary + Transcript view
- Language detection badge, duration, word count, read time
- Export as TXT 
- Full history saved in SQLite (sidebar)
- Copy to clipboard buttons
- API health indicator

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | Check if API is running |
| POST | /upload | Upload video file |
| POST | /youtube | Process YouTube URL |
| GET | /history | Get all past results |
| GET | /export/txt/{id} | Download summary as TXT |


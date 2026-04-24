# Video2Summary
A full-stack video summarization app with FastAPI backend and polished HTML frontend.

## Model Setup
The trained model is not included in this repository due to file size.

1. Download the Final_model folder from: https://drive.google.com/drive/folders/16TCnvMI4HA_fQv9wJ9bUmRDkmlK8l-PC?usp=drive_link
2. Place it in: `backend/models/Final_model/`

The folder should look like this:

backend/
    models/
        Final_model/
            config.json
            model.safetensors
            tokenizer.json
            ...

## Project Structure
Video2Summary/
├── backend/
│   ├── exports/         ← Generated TXT files
│   ├── models/          ← Trained model files (download separately)
│   ├── uploads/         ← Temporary video storage
│   ├── main.py          ← FastAPI app
│   ├── pipeline.py      ← Video→Audio→Transcription (teammate 2)
│   ├── summarizer.py    ← Trained model (teammate 1)
│   ├── database.py      ← SQLite history
│   ├── export.py        ← TXT export
│   ├── qa_generator.py  ← Q&A generation (T5 model)
│   └── requirements.txt
└── frontend/
    └── index.html       ← Full UI (open in browser)

## Setup & Run

### 1. Install dependencies
```bash
cd backend
pip install -r requirements.txt
pip install yt-dlp
```

### 2. Start the backend
```bash
cd backend
python -m uvicorn main:app --reload --port 8000
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
- Q&A generation from summary using trained T5 model
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
| POST | /questions/{id} | Generate Q&A pairs |
| GET | /questions/{id} | Get saved Q&A pairs |

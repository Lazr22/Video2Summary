from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import shutil, os, time
from database import init_db, save_result, get_history, get_record, save_questions, get_questions
from pipeline import process_video
from summarizer import summarize_text
from export import export_to_txt, export_to_pdf
from qa_generator import generate_qa

app = FastAPI(title="Video2Summary API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/health")
def health():
    return {"status": "ok"}


def _run_pipeline(video_path: str, filename: str) -> dict:
    transcript, language, duration = process_video(video_path)
    summary = summarize_text(transcript)
    word_count = len(summary.split())
    read_time  = max(1, round(word_count / 200))
    record_id = save_result(
        filename=filename, transcript=transcript, summary=summary,
        language=language, duration=duration, word_count=word_count,
    )
    return {
        "id": record_id, "filename": filename, "transcript": transcript,
        "summary": summary, "language": language, "duration": duration,
        "word_count": word_count, "read_time": read_time,
    }


@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    allowed = [".mp4", ".mov", ".avi", ".mkv", ".webm"]
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    temp_path = os.path.join(UPLOAD_DIR, f"temp_{int(time.time())}_{file.filename}")
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return _run_pipeline(temp_path, file.filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


@app.post("/youtube")
async def process_youtube(data: dict):
    url = data.get("url", "").strip()
    if not url:
        raise HTTPException(status_code=400, detail="No URL provided")
    try:
        import yt_dlp
    except ImportError:
        raise HTTPException(status_code=500, detail="Run: pip install yt-dlp")
    output_path = os.path.join(UPLOAD_DIR, f"yt_{int(time.time())}.mp4")
    try:
        ydl_opts = {
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "outtmpl": output_path, "quiet": True, "merge_output_format": "mp4",
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = info.get("title", "YouTube Video")
        return _run_pipeline(output_path, filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(output_path):
            os.remove(output_path)


@app.get("/history")
def get_all_history():
    return get_history()


@app.post("/questions/{record_id}")
def generate_questions(record_id: int):
    """Generate Q&A pairs and save them to database."""
    record = get_record(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    try:
        pairs = generate_qa(record["summary"])
        save_questions(record_id, pairs)
        return {"id": record_id, "questions": pairs}
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/questions/{record_id}")
def get_saved_questions(record_id: int):
    """Get previously generated Q&A pairs from database."""
    record = get_record(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    pairs = get_questions(record_id)
    return {"id": record_id, "questions": pairs}


@app.get("/export/txt/{record_id}")
def export_txt(record_id: int):
    path = export_to_txt(record_id)
    if not path:
        raise HTTPException(status_code=404, detail="Record not found")
    return FileResponse(path, media_type="text/plain", filename=f"summary_{record_id}.txt")

import os
import shutil
import uuid
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

load_dotenv()

from core.detail_extractor import extract_text
from core.cleaning_data import clean_text
from core.vectore_db import chunk_text, vector_store, vector_load, retrivers
from core.user_description import user_input

app = FastAPI(title="Resume ATS Analyzer API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Resume ATS Analyzer is running"}


@app.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    # Validate file type
    allowed_extensions = {".pdf", ".png", ".jpg", ".jpeg"}
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Please upload a PDF or image (PNG, JPG, JPEG)."
        )

    if not job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty."
        )

    # Save uploaded file with unique name
    unique_name = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    try:
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Step 1: Extract text
        raw_text = extract_text(file_path)
        if not raw_text or not raw_text.strip():
            raise HTTPException(
                status_code=422,
                detail="Could not extract text from the uploaded file. Ensure the PDF has selectable text or the image is clear."
            )

        # Step 2: Clean text
        cleaned = clean_text(raw_text)

        # Step 3: Chunk and store in vector DB
        chunks = chunk_text(cleaned)
        vector_store(chunks)

        # Step 4: Run LLM analysis
        result = user_input(job_description)

        return JSONResponse(content={
            "success": True,
            "filename": file.filename,
            "analysis": result
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            os.remove(file_path)


@app.get("/")
def root():
    return {"message": "Resume ATS Analyzer API. Visit /docs for API documentation."}

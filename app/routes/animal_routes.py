from fastapi import APIRouter, UploadFile, File
import shutil
import os
from app.services.gemini_service import analyze_image

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/analyze")
async def analyze_animal_image(file: UploadFile = File(...)):
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    results = analyze_image(file_path)

    return {
        "filename": file.filename,
        "results": results
    }
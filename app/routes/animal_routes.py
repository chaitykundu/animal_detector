from fastapi import APIRouter, UploadFile, File
import shutil
import os
from app.services.pipeline_service import analyze_media

router = APIRouter()

@router.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Detect file type
    if file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
        file_type = "image"
    elif file.filename.lower().endswith((".mp4", ".avi", ".mov")):
        file_type = "video"
    else:
        return {"error": "Unsupported format"}

    results = analyze_media(file_path, file_type)

    return {
        "filename": file.filename,
        "type": file_type,
        "results": results
    }
import os, shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from typing import Optional
from tools.upload_csv import upload_csv, list_uploaded_tables

router     = APIRouter()
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_csv_file(
    file: UploadFile = File(...),
    table_name: Optional[str] = Form(None)
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files supported.")
    save_path = os.path.join(UPLOAD_DIR, file.filename.replace(" ", "_"))
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    result = upload_csv(file_path=save_path, table_name=table_name)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result

@router.get("/tables")
async def list_tables():
    return list_uploaded_tables()
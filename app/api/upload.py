from fastapi import APIRouter, UploadFile, File

from app.ingestion.parser import parse_csv

router = APIRouter()


@router.post("/upload")
async def upload_csv(file: UploadFile = File(...)):

    df = await parse_csv(file)

    return {
        "filename": file.filename,
        "rows": len(df),
        "columns": list(df.columns),
    }
from fastapi import APIRouter, UploadFile, File, HTTPException
import uuid
from pathlib import Path

router = APIRouter(prefix="/graphs", tags=["graphs"])
UPLOAD_DIR = Path("data/uploaded")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_graph(file: UploadFile = File(...)):
    ext = Path(file.filename).suffix.lower()
    if ext not in {'.edgelist', '.txt', '.mtx', '.csv'}:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    file_id = f"{uuid.uuid4()}{ext}"
    dest = UPLOAD_DIR / file_id
    dest.write_bytes(await file.read())
    return {"file_id": file_id}


@router.get("/")
def list_graphs():
    return [{"file_id": f.name} for f in UPLOAD_DIR.iterdir() if f.is_file()]

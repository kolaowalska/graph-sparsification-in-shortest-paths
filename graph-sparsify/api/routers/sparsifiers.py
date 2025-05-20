from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.graph_pipeline.parsers import infer_and_parse
from src.graph_pipeline.sparsifiers import sparsifiers_registry
from src.graph_pipeline.metrics import compute_metrics
from pathlib import Path

router = APIRouter(prefix="/sparsifiers", tags=["sparsifiers"])


class SparsifyRequest(BaseModel):
    file_id: str
    method: str
    rho: float = 0.5


@router.get("/methods")
def get_methods():
    return list(sparsifiers_registry.keys())


@router.post("/apply")
def apply_sparsifier(req: SparsifyRequest):
    path = Path("data/uploaded") / req.file_id
    if not path.exists():
        raise HTTPException(status_code=404, detail="Graph not found")
    if req.method not in sparsifiers_registry:
        raise HTTPException(status_code=400, detail="Method not supported")

    G = infer_and_parse(path)
    H = sparsifiers_registry[req.method](G, req.rho)
    metrics = compute_metrics(G, H, req.method)
    return {"metrics": metrics}

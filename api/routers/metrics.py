from fastapi import APIRouter
from src.graph_pipeline.parsers import infer_and_parse
from src.graph_pipeline.sparsifiers import sparsifiers_registry
from src.graph_pipeline.flatten_metrics import compute_metrics
from pydantic import BaseModel
from pathlib import Path

router = APIRouter(prefix="/metrics", tags=["metrics"])


class MetricsRequest(BaseModel):
    file_id: str
    method: str
    rho: float = 0.5


@router.post("/compute")
def compute_on_the_fly(req: MetricsRequest):
    path = Path("data/uploaded") / req.file_id
    G = infer_and_parse(path)
    H = sparsifiers_registry[req.method](G, req.rho)
    return compute_metrics(G, H, req.method)

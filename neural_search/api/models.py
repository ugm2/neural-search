from pydantic import BaseModel
from typing import List, Optional


class NeuralDocument(BaseModel):
    text: str
    id: Optional[str] = None
    metadata: Optional[dict] = {}


class IndexingData(BaseModel):
    documents: List[NeuralDocument]
    pipeline: dict
    parameters: dict


class IndexingResponse(BaseModel):
    indices: List[str]


class SearchData(BaseModel):
    queries: List[str]
    pipeline: dict
    parameters: dict
    filters: List[dict] = None


class SearchResponse(BaseModel):
    text: str
    score: float
    id: str
    fragment_id: str
    metadata: dict = {}
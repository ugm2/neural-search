from pydantic import BaseModel
from typing import List, Optional


class NeuralDocument(BaseModel):
    text: str
    id: Optional[str] = None
    tags: Optional[List[str]] = []


class IndexingData(BaseModel):
    documents: List[NeuralDocument]
    pipeline: dict
    parameters: dict


class SearchData(BaseModel):
    queries: List[str]
    pipeline: dict
    parameters: dict
    filters: List[dict] = None

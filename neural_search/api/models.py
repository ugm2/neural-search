from pydantic import BaseModel
from typing import List, Optional


class Document(BaseModel):
    text: str
    id: Optional[str] = None
    tags: Optional[List[str]] = []


class IndexingData(BaseModel):
    documents: List[Document]
    pipeline: dict
    parameters: dict
    clear_index: Optional[bool] = True


class SearchData(BaseModel):
    queries: List[str]
    pipeline: dict
    parameters: dict
    filters: List[dict] = None

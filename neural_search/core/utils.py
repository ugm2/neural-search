from haystack.schema import Document

import uuid
from typing import List

from neural_search.api.models import NeuralDocument


def format_docs(documents: List[NeuralDocument]):
    """Given a list of documents, format the documents and return the documents and doc ids."""
    db_docs: list = []

    for doc in documents:
        doc_id = doc.id if doc.id else str(uuid.uuid4())
        meta = doc.metadata
        meta.update({"id": doc_id})
        db_doc = {
            "content": doc.text,
            "content_type": "text",
            "id": str(uuid.uuid4()),
            "meta": meta,
        }
        db_docs.append(Document(**db_doc))
    return db_docs, [doc.meta["id"] for doc in db_docs]

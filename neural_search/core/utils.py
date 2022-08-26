from haystack.schema import Document

import uuid
from typing import List

from neural_search.api.models import NeuralDocument


def format_docs(documents: List[NeuralDocument]):
    """Given a list of documents, format the documents and return the documents and doc ids."""
    db_docs: list = []

    for doc in documents:
        doc_id = doc.id if doc.id else str(uuid.uuid4())
        db_doc = {
            "content": doc.text,
            "content_type": "text",
            "id": str(uuid.uuid4()),
            "meta": {"tags": doc.tags, "id": doc_id},
        }
        db_docs.append(Document(**db_doc))
    return db_docs, [doc.meta["id"] for doc in db_docs]


def index_documents_pipeline(
    indexing_pipeline,
    documents: List[NeuralDocument],
):
    """Given a list of documents, index them using the given pipeline."""
    documents, doc_ids = format_docs(documents)
    # Index documents
    indexing_pipeline.run(documents=documents)
    return doc_ids


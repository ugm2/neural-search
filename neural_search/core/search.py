from neural_search.core.utils import format_docs
from neural_search.api.models import NeuralDocument
from typing import List

def index_documents_pipeline(
    indexing_pipeline,
    documents: List[NeuralDocument],
):
    """Given a list of documents, index them using the given pipeline."""
    documents, doc_ids = format_docs(documents)
    # Index documents
    indexing_pipeline.run(documents=documents)
    return doc_ids
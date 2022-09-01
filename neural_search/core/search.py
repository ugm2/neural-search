from haystack import Pipeline
from typing import List, Optional, Union
from neural_search.api.utils import handle_pipeline_parameters
from neural_search.utils.utils import format_docs
from neural_search.api.models import NeuralDocument
from typing import List

def index_documents_pipeline(
    indexing_pipeline,
    documents: List[NeuralDocument],
    params: dict = {}
):
    """Given a list of documents, index them using the given pipeline."""
    documents, doc_ids = format_docs(documents)
    # Index documents
    run_parameters = handle_pipeline_parameters(params, "run_parameters")
    indexing_pipeline.run(documents=documents, params=run_parameters)
    return doc_ids

def run_search_pipeline(
    search_pipeline: Pipeline,
    queries: List[str],
    filters: Union[List[dict], dict] = {},
    params: dict = {},
    return_metadata: bool = False,
    min_score: Optional[float] = 0.0,
):
    """Given a list of queries, search using the given pipeline and filters/parameters."""
    results = []
    run_parameters = handle_pipeline_parameters(params, "run_parameters")
    if isinstance(filters, dict):
        filters = [filters for _ in range(len(queries))]
    run_parameters.update({"filters": filters})
    matches_queries = search_pipeline.run_batch(queries=queries, params=run_parameters)
    for matches in matches_queries["documents"]:
        results.append(
            sorted(
                [
                    {
                        "text": res.content,
                        "score": res.score,
                        "id": res.meta["id"],
                        "fragment_id": res.id,
                        "metadata": res.meta if return_metadata else {},
                    }
                    for res in matches
                    if res.score is not None and res.score >= min_score
                ],
                key=lambda x: x["score"],
                reverse=True,
            )
        )
    return results
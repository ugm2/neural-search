from typing import List
from fastapi import FastAPI, HTTPException
import os

from neural_search.api.utils import cache_pipeline
import neural_search.api.models as models
from neural_search.core.search import index_documents_pipeline, run_search_pipeline
import logging

logger = logging.getLogger("Neural Search Server")
logger.setLevel(os.getenv("LOGGER_LEVEL", logging.ERROR))

app = FastAPI()

# cache latest pipeline
cached_pipelines = {}


@app.post("/index/", response_model=models.IndexingResponse)
def neural_index(data: models.IndexingData):
    global cached_pipelines
    try:
        pipeline, cached_pipelines = cache_pipeline(
            pipeline=data.pipeline,
            params=data.parameters,
            cached_pipelines=cached_pipelines,
            pipeline_name="indexing",
        )
        doc_ids = index_documents_pipeline(
            indexing_pipeline=pipeline,
            documents=data.documents,
            params=data.parameters
        )
        return models.IndexingResponse(indices=doc_ids)
    except Exception as e:
        import traceback
        error_message = f"ERROR:{str(e)}  DETAIL: {traceback.format_exc()}"
        raise HTTPException(status_code=422, detail=error_message)


@app.post("/search/", response_model=List[List[models.SearchResponse]])
def neural_search(request: models.SearchData):
    global cached_pipelines
    try:
        pipeline, cached_pipelines = cache_pipeline(
            pipeline=request.pipeline,
            params=request.parameters,
            cached_pipelines=cached_pipelines,
            pipeline_name="query",
        )
        results = run_search_pipeline(
            search_pipeline=pipeline,
            queries=request.queries,
            filters=request.filters,
            params=request.parameters,
            return_metadata=request.return_metadata,
        )
        return [
            [models.SearchResponse(**match) for match in r]
            for r in results
        ]
    except Exception as e:
        import traceback
        error_message = f"ERROR:{str(e)}  DETAIL: {traceback.format_exc()}"
        raise HTTPException(status_code=422, detail=error_message)

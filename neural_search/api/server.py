from fastapi import FastAPI, HTTPException
import os

from neural_search.api.utils import cache_pipeline
import neural_search.api.models as models
from neural_search.core.search import index_documents_pipeline
import logging

logger = logging.getLogger("Neural Search Server")
logger.setLevel(os.getenv("LOGGER_LEVEL", logging.ERROR))

app = FastAPI()

# cache latest search pipeline
cached_pipelines = {}


@app.post("/index/")
def smart_index_v3(data: models.IndexingData):
    global cached_pipelines
    try:
        pipeline, cached_pipelines = cache_pipeline(
            data.pipeline,
            data.parameters,
            cached_pipelines,
            pipeline_name="indexing"
        )
        doc_ids = index_documents_pipeline(
            indexing_pipeline=pipeline,
            documents=data.documents
        )
        return {'indices': doc_ids}
    except Exception as e:
        import traceback
        error_message = "ERROR: " + str(e) + " ERROR DETAIL: " + traceback.format_exc()
        raise HTTPException(status_code=422, detail=error_message)


@app.post("/semantic_search/")
def smart_search_v3(request: models.SearchData):
    global cached_pipelines
    try:
        pipeline, cached_pipelines = cache_pipeline(
            request.pipeline,
            request.parameters,
            cached_pipelines,
            pipeline_name="query",
        )
    except Exception as e:
        import traceback
        error_message = "ERROR: " + str(e) + " ERROR DETAIL: " + traceback.format_exc()
        raise HTTPException(status_code=422, detail=error_message)

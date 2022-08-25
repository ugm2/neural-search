from fastapi import HTTPException, FastAPI
import uvicorn
import os

from api.utils import cache_pipeline
import api.models as models
import logging

logger = logging.getLogger("Neural Search Server")
logger.setLevel(os.getenv("LOGGER_LEVEL", logging.ERROR))

app = FastAPI()

# cache latest search pipeline
cached_pipelines = {}


@app.post("/v3/index/")
def smart_index_v3(data: models.IndexingData):
    pipeline, cached_pipelines = cache_pipeline(
        data.pipeline, data.parameters, cached_pipelines, pipeline_name="indexing"
    )


@app.post("/v3/semantic_search/")
def smart_search_v3(request: models.SearchData):
    global cached_pipelines
    pipeline, cached_pipelines = cache_pipeline(
        request.pipeline,
        request.parameters,
        cached_pipelines,
        pipeline_name="query",
    )

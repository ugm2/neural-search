from neural_search.core.pipeline_generation.generator import PipelineGenerator
from neural_search.core.pipeline_generation.pipelines import (
    query_classifier_keyword_dense_ranker_pipeline,
)

search_pipeline, index_pipeline = query_classifier_keyword_dense_ranker_pipeline(
    es_endpoint="127.0.0.1", es_port=9200, index="documents", use_gpu=True
)

pipeline_generator = PipelineGenerator()
pipeline_generator.generate(
    index_pipeline=index_pipeline,
    search_pipeline=search_pipeline,
    # Name of the folder that will be created. It should be a meaningful name
    pipeline_name="QueryClassifier",
    # Folder where the Pipeline folder and its JSON files will be generated
    folder="interface/data/pipelines/",
    # Whether to draw the pipelines. They will be saved as a pipeline.png
    draw_pipeline=True,
)

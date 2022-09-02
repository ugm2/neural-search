# -*- coding: utf-8 -*-
"""
Example of pipeline creation functions
"""

# Copyright Unai Garay Maestre

from haystack import Pipeline
from haystack.nodes import SklearnQueryClassifier
from haystack.document_stores.elasticsearch import ElasticsearchDocumentStore
from haystack.nodes.preprocessor import PreProcessor
from haystack.nodes.retriever import DensePassageRetriever, BM25Retriever
from haystack.nodes.ranker.sentence_transformers import SentenceTransformersRanker


def keyword_search_pipeline(es_endpoint="127.0.0.1", es_port=9200, index="documents"):
    document_store = ElasticsearchDocumentStore(
        host=es_endpoint, port=es_port, similarity="dot_product", index=index
    )
    es_retriever = BM25Retriever(document_store=(document_store))
    processor = PreProcessor(
        clean_empty_lines=True,
        clean_whitespace=True,
        clean_header_footer=True,
        split_by="word",
        split_length=200,
        split_respect_sentence_boundary=True,
        split_overlap=0,
    )
    # SEARCH PIPELINE
    search_pipeline = Pipeline()
    search_pipeline.add_node(es_retriever, name="ESRetriever", inputs=["Query"])

    # INDEXING PIPELINE
    index_pipeline = Pipeline()
    index_pipeline.add_node(processor, name="Preprocessor", inputs=["File"])
    index_pipeline.add_node(es_retriever, name="ESRetriever", inputs=["Preprocessor"])
    index_pipeline.add_node(
        document_store, name="DocumentStore", inputs=["ESRetriever"]
    )

    return search_pipeline, index_pipeline


def dense_passage_retrieval_pipeline(
    es_endpoint="127.0.0.1",
    es_port=9200,
    index="documents",
    use_gpu=True,
    query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
    passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base",
):
    document_store = ElasticsearchDocumentStore(
        host=es_endpoint, port=es_port, similarity="dot_product", index=index
    )
    dpr_retriever = DensePassageRetriever(
        document_store=document_store,
        query_embedding_model=query_embedding_model,
        passage_embedding_model=passage_embedding_model,
        use_gpu=use_gpu,
    )
    processor = PreProcessor(
        clean_empty_lines=True,
        clean_whitespace=True,
        clean_header_footer=True,
        split_by="word",
        split_length=100,
        split_respect_sentence_boundary=True,
        split_overlap=0,
    )
    # SEARCH PIPELINE
    search_pipeline = Pipeline()
    search_pipeline.add_node(dpr_retriever, name="DPRRetriever", inputs=["Query"])

    # INDEXING PIPELINE
    index_pipeline = Pipeline()
    index_pipeline.add_node(processor, name="Preprocessor", inputs=["File"])
    index_pipeline.add_node(dpr_retriever, name="DPRRetriever", inputs=["Preprocessor"])
    index_pipeline.add_node(
        document_store, name="DocumentStore", inputs=["DPRRetriever"]
    )

    return search_pipeline, index_pipeline


def query_classifier_keyword_dense_ranker_pipeline(
    es_endpoint="127.0.0.1",
    es_port=9200,
    index="documents",
    use_gpu=True,
    query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
    passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base",
    ranker_model="./models/cross-encoder/ms-marco-MiniLM-L-6-v2",
):
    document_store = ElasticsearchDocumentStore(
        host=es_endpoint, port=es_port, similarity="dot_product", index=index
    )
    es_retriever = BM25Retriever(document_store=(document_store))
    dpr_retriever = DensePassageRetriever(
        document_store=document_store,
        query_embedding_model=query_embedding_model,
        passage_embedding_model=passage_embedding_model,
        use_gpu=use_gpu,
    )
    processor = PreProcessor(
        clean_empty_lines=True,
        clean_whitespace=True,
        clean_header_footer=True,
        split_by="word",
        split_length=100,
        split_respect_sentence_boundary=True,
        split_overlap=0,
    )
    ranker = SentenceTransformersRanker(ranker_model)

    # SEARCH PIPELINE
    search_pipeline = Pipeline()
    search_pipeline.add_node(
        SklearnQueryClassifier(), inputs=["Query"], name="QueryClassifier"
    )
    search_pipeline.add_node(
        es_retriever, name="ESRetriever", inputs=["QueryClassifier.output_2"]
    )
    search_pipeline.add_node(
        dpr_retriever, name="DPRRetriever", inputs=["QueryClassifier.output_1"]
    )
    search_pipeline.add_node(ranker, name="Ranker", inputs=["DPRRetriever"])

    # INDEXING PIPELINE
    index_pipeline = Pipeline()
    index_pipeline.add_node(processor, name="Preprocessor", inputs=["File"])
    index_pipeline.add_node(dpr_retriever, name="DPRRetriever", inputs=["Preprocessor"])
    index_pipeline.add_node(
        document_store, name="DocumentStore", inputs=["DPRRetriever"]
    )

    return search_pipeline, index_pipeline


if __name__ == "__main__":
    from smart_search.core.pipeline_generation.generator import PipelineGenerator

    search_pipeline, index_pipeline = keyword_search_pipeline(
        es_endpoint="127.0.0.1", es_port=9200, index="documents"
    )

    pipeline_generator = PipelineGenerator()
    pipeline_generator.generate(
        index_pipeline=index_pipeline,
        search_pipeline=search_pipeline,
        pipeline_name="PipelineTest",  # this should be meaningful like KeywordSearch
        folder="test_data/json_pipelines/",
        draw_pipeline=True,
    )

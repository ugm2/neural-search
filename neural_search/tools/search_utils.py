"""Set of util functions to help make search requests"""
import requests
import json

def load_json(filename):
    with open(filename, "r") as f:
        return json.load(f)

def do_indexing(corpus, pipeline, parameters, url, reset_index=True):
    # indexing data
    index_params = {
        "documents": corpus,
        "pipeline": pipeline,
        "parameters": parameters,
        "clear_index": reset_index,
    }

    response = requests.post(f"{url}/index", json=index_params)
    return response.json()


def do_search(queries, pipeline, parameters, url, filters=None):
    if isinstance(filters, dict):
        filters = [filters]
    # searching
    search_params = {
        "queries": queries,
        "pipeline": pipeline,
        "parameters": parameters,
        "filters": filters
    }

    response = requests.post(f"{url}/search", json=search_params)
    return response.json()
"""Set of util functions to help make search requests"""
import requests
import json

def load_json(filename):
    with open(filename, "r") as f:
        return json.load(f)

def do_indexing(corpus, pipeline, parameters, url):
    # indexing data
    index_params = {
        "documents": corpus,
        "pipeline": pipeline,
        "parameters": parameters,
    }

    response = requests.post(f"{url}/index", json=index_params)
    return response.json()


def do_search(
    queries,
    pipeline,
    parameters,
    url,
    return_metadata=False,
    filters=None,
):
    # searching
    search_params = {
        "queries": queries,
        "pipeline": pipeline,
        "parameters": parameters,
        "filters": filters,
        "return_metadata": return_metadata,
    }
    print(search_params)

    response = requests.post(f"{url}/search", json=search_params)
    return response.json()
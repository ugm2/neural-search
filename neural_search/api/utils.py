from haystack import Pipeline

def handle_pipeline_parameters(params, params_type):
    """
    Handle pipeline parameters for create/run
    """
    final_params = {}
    for node, node_params in params.items():
        if params_type in node_params:
            final_params[node] = node_params[params_type]
    return final_params

def config_pipeline(pipeline, params):
    """
    Configure a pipeline with the given parameters.
    """
    for component in pipeline["components"]:
        if component["name"] in params:
            component["params"] = params[component["name"]]
    return pipeline


def cache_pipeline(pipeline, params, cached_pipelines, pipeline_name):
    """
    Cache a pipeline if it is not already cached.
    """
    pipeline_cache_name = str(pipeline) + str(params)
    if pipeline_cache_name not in cached_pipelines:
        cached_pipelines.clear()  # avoid storing multiple pipelines
        create_params = handle_pipeline_parameters(params, "create_parameters")
        pipeline = config_pipeline(pipeline, create_params)
        p = Pipeline.load_from_config(pipeline, pipeline_name=pipeline_name)
        cached_pipelines[pipeline_cache_name] = p
    else:
        p = cached_pipelines[pipeline_cache_name]

    return p, cached_pipelines

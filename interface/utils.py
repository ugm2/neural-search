import os
import streamlit as st


def list_files_in_folder(folder):
    return [f for f in os.listdir(folder)]


@st.cache
def get_pipelines(pipelines_folder, type="search"):
    pipelines = []
    parameters = []
    folders = list_files_in_folder(pipelines_folder)
    for f in folders:
        folder_path = os.path.join(pipelines_folder, f)
        files = list_files_in_folder(folder_path)
        if "pipeline.json" in files:
            pipeline_path = os.path.join(f, "pipeline.json")
            pipelines.append(pipeline_path)
        if type == "search":
            if "search_parameters.json" in files:
                parameters_path = os.path.join(f, "search_parameters.json")
                parameters.append(parameters_path)
        else:
            if "index_parameters.json" in files:
                parameters_path = os.path.join(f, "index_parameters.json")
                parameters.append(parameters_path)
    return pipelines, parameters

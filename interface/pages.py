import json
from pathlib import Path

import streamlit as st
from streamlit_tags import st_tags
from streamlit_option_menu import option_menu

from interface.components import (
    component_file_input,
    component_show_and_validate_pipeline,
    component_show_search_result,
    component_text_input,
)
from neural_search.utils.search_utils import do_indexing, do_search, load_json
from interface.utils import get_pipelines

SEARCH_RESULTS_KEY = "search_results_key"
PIPELINES_FOLDER = "data/pipelines/"


@st.experimental_singleton
def load_documents(filename):
    with open(filename, "r") as f:
        return json.load(f)


def page_landing_page(container):
    with container:
        st.header("Neural Search")

        st.markdown(
            "This is a tool to allow indexing & search content using neural capabilities"
        )


def page_search(container):
    st.sidebar.markdown("**Default settings**")
    service_url = st.sidebar.text_input(
        "Smart search URL", st.session_state["demo_config"]["service_url"]
    )
    pipelines, parameters = get_pipelines(PIPELINES_FOLDER)
    search_pipe_file = st.sidebar.selectbox("Search pipeline", pipelines)
    search_pipe = load_json(Path(PIPELINES_FOLDER, search_pipe_file))
    search_params_file = st.sidebar.selectbox("Search parameters", parameters)
    search_params = load_json(Path(PIPELINES_FOLDER, search_params_file))

    with container:
        st.title("Query me!")

        ## SEARCH ##
        query = st.text_input("Query")
        filters = {}
        with st.expander("Search parameters"):
            return_metadata = st.checkbox("Return metadata", value=True)
            st.markdown("# Apply Filters:")
            idx = 1
            while True:
                col1, col2 = st.columns(2)
                with col1:
                    filter_name = st.text_input("Filter name", "tags", key=idx)
                with col2:
                    filter_values = st_tags(
                        label=filter_name,
                        text="Press enter to add more",
                        value=[],
                        key=idx,
                    )
                if filter_values != []:
                    filters[filter_name] = filter_values
                    idx += 1
                else:
                    break
        component_show_and_validate_pipeline(container, search_pipe, search_params)

        if st.button("Search"):
            st.session_state[SEARCH_RESULTS_KEY] = do_search(
                queries=[query],
                pipeline=search_pipe,
                parameters=search_params,
                url=service_url,
                filters=filters,
                return_metadata=return_metadata,
            )

        if SEARCH_RESULTS_KEY in st.session_state:
            if "detail" not in st.session_state[SEARCH_RESULTS_KEY]:
                component_show_search_result(
                    container=container,
                    results=st.session_state[SEARCH_RESULTS_KEY][0]
                )
            else:
                st.error(st.session_state[SEARCH_RESULTS_KEY])


def page_index(container):
    st.sidebar.markdown("**Default settings**")
    service_url = st.sidebar.text_input(
        "Smart search URL", st.session_state["demo_config"]["service_url"]
    )
    pipelines, parameters = get_pipelines(PIPELINES_FOLDER, type="index")
    index_pipe_file = st.sidebar.selectbox("Index pipeline", pipelines)
    index_pipe = load_json(Path(PIPELINES_FOLDER, index_pipe_file))
    index_params_file = st.sidebar.selectbox("Index parameters", parameters)
    index_params = load_json(Path(PIPELINES_FOLDER, index_params_file))
    with container:
        st.title("Index time!")

        component_show_and_validate_pipeline(container, index_pipe, index_params)

        input_funcs = {
            "Raw Text": (component_text_input, "card-text"),
            "File": (component_file_input, "file-earmark-arrow-up"),
        }
        selected_input = option_menu(
            "Input Text",
            list(input_funcs.keys()),
            icons=[f[1] for f in input_funcs.values()],
            menu_icon="list",
            default_index=0,
            orientation="horizontal",
        )

        corpus = input_funcs[selected_input][0](container)

        if len(corpus) > 0:
            index_results = None
            if st.button("Index"):
                index_results = do_indexing(
                    corpus=corpus,
                    pipeline=index_pipe,
                    parameters=index_params,
                    url=service_url,
                )
            if index_results:
                st.write(index_results)

import json
import streamlit as st

from pages import page_landing_page, page_search, page_index


@st.experimental_singleton
def load_config_file(filename):
    with open(filename, "r") as f:
        data = json.load(f)
    return {k: v for k, v in data.items()}

# Define default Session Variables over the whole session.
session_state_variables = {"demo_config": load_config_file("data/demo_config.json")}

# Define Pages for the demo
pages = {
    "Introduction": (page_landing_page, "house-fill"),
    "Search": (page_search, "search"),
    "Index": (page_index, "files"),
}

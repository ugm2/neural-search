import streamlit as st

st.set_page_config(
    page_title="Neural Search",
    page_icon="img/search.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

from streamlit_option_menu import option_menu
from config import session_state_variables, pages

# Initialization of session state
for key, value in session_state_variables.items():
    if key not in st.session_state:
        st.session_state[key] = value


def run_demo():

    main_page = st.container()

    st.sidebar.image("img/search.png")

    navigation = st.sidebar.container()

    with navigation:

        selected_page = option_menu(
            "Navigation",
            list(pages.keys()),
            icons=[f[1] for f in pages.values()],
            menu_icon="cast",
            default_index=0,
        )

    # Draw the correct page
    pages[selected_page][0](main_page)


run_demo()

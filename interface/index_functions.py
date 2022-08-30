import streamlit as st
from streamlit_tags import st_tags


def text_input():
    """Draw the Text Input widget"""
    texts = []
    idx = 1
    with st.expander("Enter documents"):
        while True:
            text = st.text_input(f"Document {idx}", key=idx)
            tags = st_tags(label="Enter tags", suggestions=["TAG1", "TAG2"], key=idx)
            if text != "":
                texts.append({"text": text, "tags": tags})
                idx += 1
                st.markdown("---")
            else:
                break
    corpus = [
        {"text": doc["text"], "metadata": {"tags": doc["tags"]}, "id": idx}
        for idx, doc in enumerate(texts)
    ]
    return corpus
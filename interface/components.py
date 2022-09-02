import streamlit as st
from annotated_text import annotated_text
from streamlit_tags import st_tags
from interface.convert_data import parse_from_cvs
import json
import pandas as pd


def component_show_and_validate_pipeline(container, pipeline, params):
    """Helper to validate pipes vs params files (steps must match)"""
    with container:
        with st.expander("Validation of pipeline"):
            pipe_nodes = set([c["name"] for c in pipeline["components"]])
            params_nodes = set(params.keys())
            if not params_nodes.issubset(pipe_nodes):
                st.warning("pipeline and params JSON do not match")
            else:
                st.success("Pipeline and parameters validated")
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("Pipeline")
                st.write(pipeline)
            with col2:
                st.markdown("Parameters")
                st.write(params)


def component_show_search_result(container, results):
    with container:
        for idx, document in enumerate(results):
            st.markdown(f"### Match {idx+1}")
            if "metadata" in document and "tags" in document["metadata"]:
                annotated_text(
                    *[(tag, "", "orange") for tag in document["metadata"]["tags"]]
                )
            st.markdown(f"**Text**: {document['text']}")
            st.markdown(f"**Document**: {document['id']}")
            st.markdown(f"**Score**: {document['score']:.3f}")
            if "metadata" in document and document["metadata"] != {}:
                with st.expander("Metadata"):
                    st.write(document["metadata"])
            st.markdown("---")


def component_text_input(container):
    """Draw the Text Input widget"""
    with container:
        texts = []
        doc_id = 1
        with st.expander("Enter documents"):
            while True:
                text = st.text_input(f"Document {doc_id}", key=doc_id)
                metadata = {}
                idx = 1
                while True:
                    col1, col2 = st.columns(2)
                    with col1:
                        metadata_name = st.text_input(
                            "Metadata name", "tags", key=f"{doc_id}_{idx}"
                        )
                    with col2:
                        metadata_values = st_tags(
                            label=metadata_name,
                            text="Press enter to add more",
                            value=[],
                            key=f"{doc_id}{idx}",
                        )
                    if metadata_values != []:
                        metadata[metadata_name] = metadata_values
                        idx += 1
                    else:
                        break
                if text != "":
                    texts.append({"text": text, "metadata": metadata})
                    doc_id += 1
                    st.markdown("---")
                else:
                    break
        corpus = [
            {"text": doc["text"], "metadata": doc["metadata"], "id": doc_id}
            for doc_id, doc in enumerate(texts)
        ]
        return corpus

def component_file_input(container):
    """Draw the File Input Widget"""
    with container:
        st.sidebar.download_button(
            label="Download example csv data for indexing",
            data=pd.read_csv("data/passages_coronavirus_metadata.csv")
            .to_csv()
            .encode("utf-8"),
            file_name="passages_coronavirus_metadata.csv",
            mime="text/csv",
        )
        json_file = {}
        metadata_fields = []
        uploaded_file = st.file_uploader("Upload File (JSON/CSV)")
        if uploaded_file is not None:
            # Process CSV
            if uploaded_file.type == "text/csv":
                col1, col2, col3 = st.columns(3)
                with col1:
                    text_field = st.text_input("Text field in CSV", "passage")
                with col2:
                    metadata_fields = st_tags(label="Enter metadata", value=["tags"])
                with col3:
                    id_field = st.text_input("ID field if any")
                    id_field = id_field if id_field != "" else None
                if text_field is not None:
                    # Convert to JSON
                    json_file = parse_from_cvs(
                        uploaded_file, text_field, metadata_fields, id_field
                    )
            # Process JSON
            elif uploaded_file.type == "application/json":
                json_file = json.loads(uploaded_file.read())
            else:
                st.error("File must be of type CSV/JSON")
        # Process final JSON file
        corpus = []
        for key, values in json_file.items():
            document = {"text": values["text"], "id": key}
            del values["text"]
            document.update({"metadata": values})
            corpus.append(document)
        return corpus
import streamlit as st
from annotated_text import annotated_text
from streamlit_tags import st_tags


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


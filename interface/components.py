import streamlit as st


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


def component_show_search_result(container, results, min_score):
    with container:
        for idx, document in enumerate(results):
            if document["score"] < min_score:
                continue
            match_doc_id = document["id"]
            st.markdown(f"### Match {idx+1}")
            with st.expander("Show text"):
                st.write(document["text"])
            st.markdown(f"**Document**: {match_doc_id}")
            st.markdown(f"**Score**: {document['score']:.3f}")
            st.markdown("---")

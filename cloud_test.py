
import os
import time
import streamlit as st

os.environ["AI_PROVIDER"] = "llama_cpp"

st.set_page_config(
    page_title="FinWise Cloud Test",
    page_icon="⚡"
)

st.title("FinWise — Cloud Diagnostics")

st.caption(
    "Temporary deployment test using demonstration data."
)

st.info("Model: Qwen 2.5 1.5B | CPU Inference")

tests = {
    "Calculation": (
        "My income is 15000 rupees and expenses "
        "are 9500 rupees. Calculate my remaining balance."
    ),
    "RAG": (
        "Search the financial knowledge base "
        "and explain the 50/30/20 budgeting rule."
    ),
    "Multiple Tools": (
        "Analyze my transactions and create a "
        "monthly budget plan with an income "
        "of 15000 rupees."
    )
}

selected = st.selectbox(
    "Select diagnostic test",
    list(tests.keys())
)

st.code(tests[selected], language=None)

if st.button("Run Test", type="primary"):

    start = time.time()

    try:

        with st.spinner("Running FinWise agent..."):

            from agents import run_agent

            result = run_agent(
                tests[selected],
                return_trace=True
            )

        elapsed = time.time() - start

        if result["validated"]:
            st.success("Workflow validation passed")
        else:
            st.warning("Workflow incomplete")

        st.metric(
            "Execution Time",
            f"{elapsed:.2f} seconds"
        )

        st.subheader("Agent Response")
        st.write(result["answer"])

        st.subheader("Execution Trace")

        st.json({
            "required_tools": result["required_tools"],
            "executed_tools": result["executed_tools"],
            "recovered_tools": result["recovered_tools"],
            "missing_tools": result["missing_tools"],
            "knowledge_sources": result["knowledge_sources"],
            "validated": result["validated"]
        })

    except Exception as error:

        st.error("Cloud inference failed")
        st.exception(error)

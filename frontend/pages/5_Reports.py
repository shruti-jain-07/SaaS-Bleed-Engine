import streamlit as st

st.set_page_config(page_title="Executive Reports", layout="wide")
st.title("Executive Financial Reports")

st.markdown(
    "Generate and download structured executive summaries for leadership review."
)

col1, col2 = st.columns(2)
with col1:
    st.subheader("CSV Audit Export")
    st.write(
        "Export granular transaction logs, ML anomaly scores, and contract risk flags."
    )
    st.button("Generate CSV Audit Log")

with col2:
    st.subheader("PDF Executive Summary")
    st.write(
        "Generate a formatted executive report covering spend metrics and AI recommendations."
    )
    st.button("Generate PDF Summary")
import streamlit as st

# Configure multi-page Streamlit application layout
st.set_page_config(
    page_title="FinOps SaaS Bleed Engine",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar Branding
st.sidebar.title("SaaS Bleed Engine")
st.sidebar.caption("FinOps Audit & Financial Intelligence Platform")

# Main Header Section
st.title("Executive Financial Intelligence Platform")
st.markdown("""
Welcome to the **SaaS Bleed Audit & Anomaly Engine**.

This enterprise platform integrates credit card transaction monitoring, ML spend anomaly detection, 
and unstructured PDF contract parsing into a unified management interface for finance leadership.

### Module Navigation
* **Overview:** Key spend metrics, flagged waste totals, and monthly expenditure trends.
* **Transactions:** Granular audit log inspector with machine learning anomaly scores.
* **Contracts:** Contract intelligence vault, notice period tracking, and risk profiles.
* **Recommendations:** Prioritized cost-cutting action items synthesized by AI.
* **Reports:** Downloadable executive CSV and PDF reports.
""")

st.info("Select a view from the left sidebar navigation menu to proceed.")
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Contract Vault", layout="wide")
st.title("Contract Intelligence Vault")

contracts = [
    {
        "Vendor": "Zoom Video",
        "Value ($)": 18000.0,
        "Notice Window": "30 Days",
        "Auto-Renew": True,
        "Risk Level": "HIGH",
        "Summary": "Requires 30-day notice prior to Oct 15 renewal.",
    },
    {
        "Vendor": "AWS Infrastructure",
        "Value ($)": 85000.0,
        "Notice Window": "60 Days",
        "Auto-Renew": True,
        "Risk Level": "CRITICAL",
        "Summary": "High value with automatic annual lock-in clause.",
    },
    {
        "Vendor": "Slack Tech",
        "Value ($)": 12000.0,
        "Notice Window": "15 Days",
        "Auto-Renew": False,
        "Risk Level": "LOW",
        "Summary": "Standard term without automatic renewal terms.",
    },
]

df = pd.DataFrame(contracts)
risk_filter = st.multiselect(
    "Filter by Risk Level",
    options=["LOW", "HIGH", "CRITICAL"],
    default=["HIGH", "CRITICAL"],
)
filtered_df = df[df["Risk Level"].isin(risk_filter)]

st.dataframe(filtered_df, use_container_width=True)
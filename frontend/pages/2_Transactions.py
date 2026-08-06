import pandas as pd
import streamlit as st

st.set_page_config(page_title="Transaction Inspector", layout="wide")
st.title("Transaction Anomaly Inspector")

# Mock transaction audit records
transactions = [
    {
        "Transaction ID": "TXN-9041",
        "Vendor": "Zoom Video",
        "Department": "Sales",
        "Amount ($)": 4500.00,
        "Anomaly Score": 0.88,
        "Status": "FLAGGED",
    },
    {
        "Transaction ID": "TXN-9042",
        "Vendor": "AWS Cloud",
        "Department": "Engineering",
        "Amount ($)": 14200.00,
        "Anomaly Score": 0.12,
        "Status": "CLEARED",
    },
    {
        "Transaction ID": "TXN-9043",
        "Vendor": "Slack Technologies",
        "Department": "Marketing",
        "Amount ($)": 3200.00,
        "Anomaly Score": 0.76,
        "Status": "FLAGGED",
    },
]

df_txn = pd.DataFrame(transactions)

search_query = st.text_input("Filter Transactions by Vendor or ID", "")
if search_query:
    df_txn = df_txn[
        df_txn["Vendor"].str.contains(search_query, case=False)
        | df_txn["Transaction ID"].str.contains(search_query, case=False)
    ]

st.dataframe(df_txn, use_container_width=True)
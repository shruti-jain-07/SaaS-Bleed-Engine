import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Executive Overview", layout="wide")
st.title("Executive Dashboard Overview")

# Metric Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total SaaS Spend", "$284,500", "+11.4% MoM", delta_color="inverse")
col2.metric(
    "Flagged SaaS Bleed", "$42,300", "14.8% of Total", delta_color="inverse"
)
col3.metric("High-Risk Contracts", "6 Contracts", "Action Required")
col4.metric("Est. Annual Savings", "$57,300", "Actionable")

st.divider()

# Plotly Visualizations
col_left, col_right = st.columns(2)
with col_left:
    st.subheader("Monthly Spend vs. Anomaly Spikes")
    df_trend = pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "Baseline Spend": [34000, 35500, 36000, 35000, 37000, 38500],
        "Anomalous Waste": [1800, 4200, 1100, 7800, 2900, 9400],
    })
    fig_trend = px.bar(
        df_trend,
        x="Month",
        y=["Baseline Spend", "Anomalous Waste"],
        title="Expenditure Breakdown ($)",
        barmode="stack",
        color_discrete_sequence=["#1f77b4", "#d62728"],
    )
    st.plotly_chart(fig_trend, use_container_width=True)

with col_right:
    st.subheader("Department Spend Distribution")
    df_dept = pd.DataFrame({
        "Department": ["Engineering", "Marketing", "Sales", "HR", "Product"],
        "Spend": [115000, 68000, 52000, 27000, 22500],
    })
    fig_dept = px.pie(
        df_dept,
        values="Spend",
        names="Department",
        title="Spend Share by Department",
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Blues_r,
    )
    st.plotly_chart(fig_dept, use_container_width=True)
import sys
from pathlib import Path

import plotly.express as px
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.pipeline import run_pipeline


st.set_page_config(
    page_title="FADA",
    page_icon=":bar_chart:",
    layout="wide",
)

st.markdown(
    """
    <style>
    :root {
        --card-bg: var(--secondary-background-color);
        --text-main: var(--text-color);
        --border-color: rgba(128, 128, 128, 0.24);
        --soft-border: rgba(128, 128, 128, 0.16);
    }

    .block-container {
        padding: 1.1rem 2rem 2rem 2rem;
        max-width: 1500px;
    }

    h1 {
        font-size: 1.8rem !important;
        margin-bottom: 0.15rem !important;
        color: var(--text-main) !important;
    }

    h2 {
        font-size: 1.15rem !important;
        margin-top: 1rem !important;
        margin-bottom: 0.3rem !important;
        color: var(--text-main) !important;
    }

    h3 {
        font-size: 0.96rem !important;
        margin-bottom: 0.25rem !important;
        color: var(--text-main) !important;
    }

    p, label, .stMarkdown, .stCaption {
        font-size: 0.88rem !important;
        color: var(--text-main);
    }

    .info-card {
        background: var(--card-bg);
        color: var(--text-main);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 0.9rem 1rem;
        margin-top: 0.6rem;
        margin-bottom: 0.9rem;
    }

    .section-caption {
        color: var(--text-main);
        opacity: 0.68;
        font-size: 0.82rem;
        margin-bottom: 0.55rem;
    }

    [data-testid="stMetric"] {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 0.75rem 0.95rem;
    }

    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"],
    [data-testid="stMetricDelta"],
    [data-testid="stSidebar"] * {
        color: var(--text-main) !important;
    }

    [data-testid="stSidebar"] {
        background: var(--secondary-background-color);
        border-right: 1px solid var(--soft-border);
    }

    hr {
        margin-top: 0.75rem !important;
        margin-bottom: 0.75rem !important;
        border-color: var(--border-color) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_analysis():
    return run_pipeline(export=False)


database, summary = load_analysis()

st.title("FADA")
st.caption(
    "Behavioral and statistical analysis of financial transactions with explainable risk scoring."
)
st.markdown(
    """
    <div class="info-card">
        <strong>How to read this dashboard</strong><br>
        This system does not determine whether a transaction is fraudulent.
        It identifies transactions that differ from typical behavior and assigns
        a risk score based on statistical and behavioral signals.
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Transactions analyzed", f"{summary['total_transactions']:,}")
col2.metric("Unique customers", f"{summary['unique_customers']:,}")
col3.metric("Transactions with alerts", f"{summary['suspicious_transactions']:,}")
col4.metric("High-risk transactions", f"{summary['high_risk_transactions']:,}")

st.sidebar.title("Filters")
risk_options = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
selected_risk = st.sidebar.multiselect("Risk level", risk_options, default=risk_options)
selected_categories = st.sidebar.multiselect(
    "Transaction category",
    sorted(database["category"].dropna().unique()),
    default=sorted(database["category"].dropna().unique()),
)
selected_cities = st.sidebar.multiselect(
    "City",
    sorted(database["city"].dropna().unique()),
    default=sorted(database["city"].dropna().unique()),
)

filtered = database[
    database["risk_level"].isin(selected_risk)
    & database["category"].isin(selected_categories)
    & database["city"].isin(selected_cities)
]

if filtered.empty:
    st.warning("No transactions match the current filter selection.")
    st.stop()

st.subheader("Quick Insights")
st.markdown(
    '<div class="section-caption">A compact overview of the current selection.</div>',
    unsafe_allow_html=True,
)

insight1, insight2, insight3, insight4 = st.columns(4)
insight1.metric("Most common category", filtered["category"].value_counts().idxmax())
insight2.metric("Most active city", filtered["city"].value_counts().idxmax())
insight3.metric("Average transaction", f"R$ {filtered['amount'].mean():,.2f}")
insight4.metric("Highest risk score", int(filtered["risk_score"].max()))

st.subheader("Risk Distribution")
risk_counts = (
    filtered["risk_level"].value_counts().reindex(risk_options, fill_value=0).reset_index()
)
risk_counts.columns = ["Risk Level", "Transactions"]
risk_colors = {
    "LOW": "#22c55e",
    "MEDIUM": "#eab308",
    "HIGH": "#f97316",
    "CRITICAL": "#ef4444",
}
fig_risk = px.bar(
    risk_counts,
    x="Risk Level",
    y="Transactions",
    color="Risk Level",
    color_discrete_map=risk_colors,
    text="Transactions",
)
fig_risk.update_layout(height=310, showlegend=False, margin=dict(l=20, r=20, t=10, b=20))
fig_risk.update_traces(textposition="outside")
st.plotly_chart(fig_risk, width="stretch", theme="streamlit")

left, right = st.columns(2)
with left:
    st.subheader("Top Transaction Categories")
    category_counts = filtered["category"].value_counts().head(8).reset_index()
    category_counts.columns = ["Category", "Transactions"]
    fig_categories = px.bar(
        category_counts,
        x="Transactions",
        y="Category",
        orientation="h",
        text="Transactions",
    )
    fig_categories.update_layout(height=340, margin=dict(l=10, r=20, t=5, b=10))
    st.plotly_chart(fig_categories, width="stretch", theme="streamlit")

with right:
    st.subheader("Transaction Value Distribution")
    fig_amounts = px.histogram(filtered, x="amount", nbins=40)
    fig_amounts.update_layout(height=340, margin=dict(l=20, r=20, t=5, b=10))
    st.plotly_chart(fig_amounts, width="stretch", theme="streamlit")

st.subheader("Transaction Activity Over Time")
daily_activity = (
    filtered.set_index("datetime").resample("D")["transaction_id"].count().reset_index()
)
daily_activity.columns = ["Date", "Transactions"]
fig_daily = px.line(daily_activity, x="Date", y="Transactions", markers=True)
fig_daily.update_layout(height=290, margin=dict(l=20, r=20, t=5, b=10))
st.plotly_chart(fig_daily, width="stretch", theme="streamlit")

st.subheader("Most Common Anomaly Signals")
anomaly_columns = {
    "high_amount": "High amount",
    "unusual_customer_amount": "Above customer average",
    "unusual_hour": "Unusual hour",
    "transaction_burst": "Transaction burst",
    "rapid_city_change": "Rapid city change",
    "unusual_category": "Unusual category",
}
anomaly_counts = [
    {"Signal": label, "Triggered": int(filtered[column].sum())}
    for column, label in anomaly_columns.items()
    if column in filtered.columns
]
fig_anomalies = px.bar(
    anomaly_counts,
    x="Triggered",
    y="Signal",
    orientation="h",
    text="Triggered",
)
fig_anomalies.update_layout(height=330, margin=dict(l=10, r=20, t=5, b=10))
st.plotly_chart(fig_anomalies, width="stretch", theme="streamlit")

st.subheader("Suspicious Transactions")
suspicious = filtered[filtered["risk_score"] > 0].sort_values(
    "risk_score",
    ascending=False,
)
display_columns = [
    "transaction_id",
    "customer_id",
    "amount",
    "category",
    "city",
    "risk_score",
    "risk_level",
]
st.dataframe(
    suspicious[display_columns],
    width="stretch",
    height=330,
    hide_index=True,
)

st.subheader("Transaction Inspector")
transaction_ids = suspicious["transaction_id"].astype(str).tolist()

if transaction_ids:
    selected_transaction = st.selectbox("Select transaction", transaction_ids)
    transaction = suspicious[
        suspicious["transaction_id"].astype(str) == selected_transaction
    ].iloc[0]

    detail1, detail2, detail3, detail4 = st.columns(4)
    detail1.metric("Amount", f"R$ {transaction['amount']:,.2f}")
    detail2.metric("Risk score", int(transaction["risk_score"]))
    detail3.metric("Risk level", transaction["risk_level"])
    detail4.metric("Category", transaction["category"])

    st.markdown("#### Why was this transaction flagged?")
    st.info(transaction["risk_reasons"])

    details_left, details_right = st.columns(2)
    with details_left:
        st.markdown(
            f"""
            **Customer ID:** {transaction['customer_id']}  
            **City:** {transaction['city']}  
            **Payment method:** {transaction['payment_method']}
            """
        )
    with details_right:
        st.markdown(
            f"""
            **Date:** {transaction['datetime']}  
            **Customer average:** R$ {transaction['customer_avg_amount']:,.2f}  
            **Amount vs average:** {transaction['amount_vs_customer_avg']:.2f}x
            """
        )
else:
    st.info("No suspicious transactions match the current filters.")

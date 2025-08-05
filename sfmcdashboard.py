import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="SFMC Email Campaign Dashboard", layout="wide")

# Title
st.title("📧 SFMC Email Campaign Performance Dashboard")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("sfmc_email_campaign_sample.csv", parse_dates=["Send Date"])

df = load_data()

# Sidebar filters
with st.sidebar:
    st.header("🔍 Filter Campaigns")
    campaign_filter = st.multiselect(
        "Select Campaign(s)", options=df["Campaign Name"].unique(),
        default=df["Campaign Name"].unique()
    )
    date_range = st.date_input(
        "Select Date Range",
        [df["Send Date"].min(), df["Send Date"].max()]
    )

# Apply filters
filtered_df = df[
    (df["Campaign Name"].isin(campaign_filter)) &
    (df["Send Date"].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])))
]

# Display KPIs
st.subheader("📊 Campaign Summary")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Avg. Open Rate", f"{filtered_df['Open Rate (%)'].mean():.2f}%")
col2.metric("Avg. Click Rate", f"{filtered_df['Click Rate (%)'].mean():.2f}%")
col3.metric("Avg. Unsubscribe Rate", f"{filtered_df['Unsubscribe Rate (%)'].mean():.2f}%")
col4.metric("Avg. Bounce Rate", f"{filtered_df['Bounce Rate (%)'].mean():.2f}%")

# Table
st.dataframe(filtered_df.style.format({
    "Open Rate (%)": "{:.2f}%",
    "Click Rate (%)": "{:.2f}%",
    "Unsubscribe Rate (%)": "{:.2f}%",
    "Bounce Rate (%)": "{:.2f}%"
}))

# Charts
st.subheader("📈 Engagement Trends")

fig = px.bar(
    filtered_df,
    x="Campaign Name",
    y=["Open Rate (%)", "Click Rate (%)", "Unsubscribe Rate (%)", "Bounce Rate (%)"],
    barmode="group",
    title="Performance by Campaign"
)
st.plotly_chart(fig, use_container_width=True)

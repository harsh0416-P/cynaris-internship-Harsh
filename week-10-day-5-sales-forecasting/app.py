
import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(
    page_title="Sales Forecasting Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Sales Forecasting Dashboard")
st.caption("Historical Sales Analysis & 12-Month Forecast")

OUTPUT_DIR = "outputs"

monthly = pd.read_csv(
    os.path.join(OUTPUT_DIR, "monthly_sales.csv")
)

forecast = pd.read_csv(
    os.path.join(OUTPUT_DIR, "sales_forecast_12_months.csv")
)

performance = pd.read_csv(
    os.path.join(OUTPUT_DIR, "model_performance.csv")
)

cleaned = pd.read_csv(
    os.path.join(OUTPUT_DIR, "cleaned_sales_data.csv")
)

monthly["Date"] = pd.to_datetime(monthly["Date"])
forecast["Forecast_Date"] = pd.to_datetime(forecast["Forecast_Date"])

total_sales = cleaned["Sales"].sum()
total_orders = cleaned["Order ID"].nunique()
total_customers = cleaned["Customer ID"].nunique()

c1, c2, c3 = st.columns(3)

c1.metric("Total Sales", f"${total_sales:,.2f}")
c2.metric("Total Orders", f"{total_orders:,}")
c3.metric("Total Customers", f"{total_customers:,}")

st.divider()

st.subheader("Historical Monthly Sales")

fig1 = px.line(
    monthly,
    x="Date",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend"
)

st.plotly_chart(fig1, use_container_width=True)

st.subheader("12-Month Sales Forecast")

fig2 = px.line(
    forecast,
    x="Forecast_Date",
    y="Predicted_Sales",
    markers=True,
    title="Future Sales Prediction"
)

fig2.add_scatter(
    x=forecast["Forecast_Date"],
    y=forecast["Upper_Bound"],
    mode="lines",
    name="Upper Bound",
    line=dict(dash="dash")
)

fig2.add_scatter(
    x=forecast["Forecast_Date"],
    y=forecast["Lower_Bound"],
    mode="lines",
    name="Lower Bound",
    line=dict(dash="dash")
)

st.plotly_chart(fig2, use_container_width=True)

st.subheader("Sales by Category")

category_sales = cleaned.groupby("Category")["Sales"].sum().reset_index()

fig3 = px.pie(
    category_sales,
    names="Category",
    values="Sales",
    title="Category Sales Distribution"
)

st.plotly_chart(fig3, use_container_width=True)

st.subheader("Model Performance")

st.dataframe(performance, use_container_width=True)

st.subheader("Forecast Data")

st.dataframe(forecast, use_container_width=True)

st.success("Sales Forecasting Dashboard Loaded Successfully")

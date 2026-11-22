import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

from data_loader import load_data

st.set_page_config(
    page_title="Real Estate Forecasting | W10D4",
    page_icon="🏠",
    layout="wide"
)

st.markdown("""
<style>
.main {background-color: #f7f9fc;}
[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e5eaf2;
    padding: 18px;
    border-radius: 12px;
}
[data-testid="stMetricValue"] {
    color: #163a63;
}
</style>
""", unsafe_allow_html=True)

st.title("🏠 Real Estate Price Forecasting")
st.caption("Indian property listings | Historical analysis and Prophet forecasting")

try:
    listings, monthly, forecast, evaluation = load_data()
except Exception as exc:
    st.error(f"Data loading failed: {exc}")
    st.stop()

# Sidebar filters
st.sidebar.title("Dashboard Controls")

cities = ["All"] + sorted(listings["city"].dropna().unique().tolist())
types = ["All"] + sorted(listings["type"].dropna().unique().tolist())

selected_city = st.sidebar.selectbox("City", cities)
selected_type = st.sidebar.selectbox("Property type", types)

future_months = st.sidebar.slider(
    "Forecast horizon (months)",
    min_value=1,
    max_value=3,
    value=3
)

filtered = listings.copy()

if selected_city != "All":
    filtered = filtered[filtered["city"] == selected_city]

if selected_type != "All":
    filtered = filtered[filtered["type"] == selected_type]

filtered_monthly = (
    filtered.assign(
        month=filtered["listed_date"].dt.to_period("M").dt.to_timestamp()
    )
    .groupby("month", as_index=False)
    .agg(
        actual_price=("total_price_lakh", "mean"),
        listing_count=("total_price_lakh", "size")
    )
    .sort_values("month")
)

future_forecast = (
    forecast[forecast["ds"] > monthly["month"].max()]
    .head(future_months)
)

# Evaluation metrics
actual = evaluation["Actual Price (Lakh)"].astype(float)
predicted = evaluation["Predicted Price (Lakh)"].astype(float)

mae = np.mean(np.abs(actual - predicted))
rmse = np.sqrt(np.mean((actual - predicted) ** 2))
mape = np.mean(np.abs((actual - predicted) / actual)) * 100

latest_price = (
    filtered_monthly["actual_price"].iloc[-1]
    if not filtered_monthly.empty else np.nan
)

next_forecast = (
    future_forecast["yhat"].iloc[0]
    if not future_forecast.empty else np.nan
)

forecast_end = (
    future_forecast["yhat"].iloc[-1]
    if not future_forecast.empty else np.nan
)

# KPI cards
st.subheader("Key Performance Indicators")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Listings", f"{len(filtered):,}")
c2.metric(
    "Latest Monthly Average",
    f"₹{latest_price:,.2f} L" if pd.notna(latest_price) else "N/A"
)
c3.metric(
    "Next Forecast",
    f"₹{next_forecast:,.2f} L" if pd.notna(next_forecast) else "N/A"
)
c4.metric("Model MAPE", f"{mape:.2f}%")

st.divider()

# Historical price chart
st.subheader("1. Historical Monthly Average Property Price")

if not filtered_monthly.empty:
    history_fig = px.line(
        filtered_monthly,
        x="month",
        y="actual_price",
        markers=True,
        labels={
            "month": "Month",
            "actual_price": "Average property price (₹ lakh)"
        },
        template="plotly_white"
    )

    history_fig.update_traces(line=dict(width=3))
    history_fig.update_layout(hovermode="x unified")

    st.plotly_chart(history_fig, use_container_width=True)
else:
    st.warning("No historical listings match these filters.")

# Listing volume
st.subheader("2. Monthly Listing Volume")

volume_fig = px.bar(
    filtered_monthly,
    x="month",
    y="listing_count",
    labels={
        "month": "Month",
        "listing_count": "Number of listings"
    },
    template="plotly_white"
)

st.plotly_chart(volume_fig, use_container_width=True)

# Forecast chart
st.subheader("3. Prophet Forecast and Uncertainty Interval")

forecast_fig = go.Figure()

forecast_fig.add_trace(go.Scatter(
    x=forecast["ds"],
    y=forecast["yhat_upper"],
    mode="lines",
    line=dict(width=0),
    showlegend=False,
    hoverinfo="skip"
))

forecast_fig.add_trace(go.Scatter(
    x=forecast["ds"],
    y=forecast["yhat_lower"],
    mode="lines",
    fill="tonexty",
    fillcolor="rgba(31,119,180,0.15)",
    line=dict(width=0),
    name="Uncertainty interval"
))

forecast_fig.add_trace(go.Scatter(
    x=forecast["ds"],
    y=forecast["yhat"],
    mode="lines",
    name="Prophet prediction",
    line=dict(width=3)
))

forecast_fig.add_vline(
    x=monthly["month"].max(),
    line_dash="dash",
    annotation_text="End of historical observations"
)

forecast_fig.update_layout(
    xaxis_title="Month",
    yaxis_title="Predicted average price (₹ lakh)",
    template="plotly_white",
    hovermode="x unified"
)

st.plotly_chart(forecast_fig, use_container_width=True)

if not future_forecast.empty:
    st.markdown("**Future forecast summary**")
    f1, f2, f3 = st.columns(3)

    f1.metric("First Forecast", f"₹{next_forecast:,.2f} L")
    f2.metric("Final Forecast", f"₹{forecast_end:,.2f} L")
    f3.metric(
        "Final Forecast Interval",
        f"₹{future_forecast['yhat_lower'].iloc[-1]:,.2f}–"
        f"₹{future_forecast['yhat_upper'].iloc[-1]:,.2f} L"
    )

# Model evaluation
st.subheader("4. Model Evaluation")

m1, m2, m3 = st.columns(3)
m1.metric("MAE", f"₹{mae:,.2f} L")
m2.metric("RMSE", f"₹{rmse:,.2f} L")
m3.metric("MAPE", f"{mape:.2f}%")

comparison = evaluation.copy()
comparison["Absolute Error"] = np.abs(actual - predicted)

comparison_fig = go.Figure()

comparison_fig.add_trace(go.Scatter(
    x=comparison["ds"],
    y=actual,
    mode="lines+markers",
    name="Actual price"
))

comparison_fig.add_trace(go.Scatter(
    x=comparison["ds"],
    y=predicted,
    mode="lines+markers",
    name="Predicted price"
))

comparison_fig.update_layout(
    title="Actual vs Predicted Price — Test Period",
    xaxis_title="Month",
    yaxis_title="Average price (₹ lakh)",
    template="plotly_white"
)

st.plotly_chart(comparison_fig, use_container_width=True)

st.dataframe(comparison, use_container_width=True)

# Forecast table
with st.expander("View future forecast values"):
    st.dataframe(
        future_forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]],
        use_container_width=True
    )

# Limitations
st.divider()
st.subheader("5. Data Sources and Model Limitations")

st.markdown("""
- Source: Original real estate listings dataset used in W10D2.
- Historical period: January 2023 to December 2024.
- Dataset size: 600 listings.
- Forecast model: Existing Prophet model from W10D2.
- Evaluation period: October–December 2024 (3 observations).
- Evaluation metrics are based on only three test observations and should
  not be interpreted as strong evidence of future model accuracy.
- Forecast represents overall monthly average listed property prices.
- City and property-type filters affect historical analysis only.
- Forecasts are not recalculated for individual city or property selections.
- Prediction intervals represent model uncertainty, not guaranteed price ranges.
""")

st.caption("W10D4 | Forecasting Dashboard — Streamlit + Plotly")

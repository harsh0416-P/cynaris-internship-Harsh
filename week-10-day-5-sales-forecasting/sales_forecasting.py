import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error
import warnings

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Indian Business Sales Forecast",
    page_icon="📊",
    layout="wide"
)

st.title("Indian Business Sales Forecasting Dashboard")
st.caption("Cynaris Internship | Week 10 | Day 5")

uploaded = st.file_uploader(
    "Upload your Indian Business Dataset",
    type=["csv", "xlsx"]
)

if uploaded is None:
    st.info("Upload a CSV or Excel sales dataset to begin.")
    st.stop()

try:
    if uploaded.name.endswith(".csv"):
        df = pd.read_csv(uploaded)
    else:
        df = pd.read_excel(uploaded)
except Exception as error:
    st.error(f"Dataset loading failed: {error}")
    st.stop()

st.subheader("1. Dataset Overview")
st.write(f"Rows: {df.shape[0]} | Columns: {df.shape[1]}")
st.dataframe(df.head(10), use_container_width=True)

date_col = st.selectbox("Select date column", df.columns)

numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

if not numeric_cols:
    st.error("The dataset has no numeric columns.")
    st.stop()

sales_col = st.selectbox("Select sales/revenue column", numeric_cols)

data = df[[date_col, sales_col]].copy()
data.columns = ["Date", "Sales"]

data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
data["Sales"] = pd.to_numeric(data["Sales"], errors="coerce")
data = data.dropna().sort_values("Date")

if data.empty:
    st.error("No valid date and sales records were found.")
    st.stop()

st.subheader("2. Data Quality")
c1, c2, c3 = st.columns(3)
c1.metric("Valid Records", len(data))
c2.metric("Missing Values Removed", len(df) - len(data))
c3.metric("Unique Dates", data["Date"].nunique())

monthly = (
    data.set_index("Date")["Sales"]
    .resample("MS")
    .sum()
    .reset_index()
)

monthly.columns = ["ds", "y"]
monthly = monthly.dropna()

if len(monthly) < 12:
    st.error(
        "At least 12 months of valid sales history are required. "
        "Check the selected date and sales columns."
    )
    st.stop()

st.subheader("3. Business Performance")

a, b, c, d = st.columns(4)
a.metric("Total Sales", f"{data.Sales.sum():,.2f}")
b.metric("Average Sales", f"{data.Sales.mean():,.2f}")
c.metric("Highest Sale", f"{data.Sales.max():,.2f}")
d.metric("Monthly Periods", len(monthly))

st.subheader("4. Exploratory Data Analysis")

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=monthly["ds"],
    y=monthly["y"],
    mode="lines+markers",
    name="Monthly Sales"
))
fig.update_layout(
    title="Historical Monthly Sales Trend",
    xaxis_title="Month",
    yaxis_title="Sales",
    template="plotly_white"
)
st.plotly_chart(fig, use_container_width=True)

monthly["Year"] = monthly["ds"].dt.year
monthly["Month"] = monthly["ds"].dt.month

yearly = monthly.groupby("Year", as_index=False)["y"].sum()

st.plotly_chart(
    go.Figure(go.Bar(
        x=yearly["Year"].astype(str),
        y=yearly["y"],
        name="Annual Sales"
    )).update_layout(
        title="Annual Sales Comparison",
        xaxis_title="Year",
        yaxis_title="Sales",
        template="plotly_white"
    ),
    use_container_width=True
)

st.subheader("5. Sales Forecasting")

horizon = st.slider(
    "Forecast horizon (months)",
    min_value=3,
    max_value=12,
    value=6
)

if st.button("Generate Forecast", type="primary"):

    if len(monthly) < 15:
        st.warning(
            "The dataset has fewer than 15 monthly observations. "
            "A three-month test set leaves limited training data."
        )

    with st.spinner("Training Prophet forecasting model..."):

        try:
            train = monthly[["ds", "y"]].iloc[:-3].copy()
            test = monthly[["ds", "y"]].iloc[-3:].copy()

            evaluation_model = Prophet(
                yearly_seasonality="auto",
                weekly_seasonality=False,
                daily_seasonality=False
            )
            evaluation_model.fit(train)

            test_future = evaluation_model.make_future_dataframe(
                periods=3,
                freq="MS"
            )

            test_predictions = evaluation_model.predict(test_future).tail(3)

            actual = test["y"].to_numpy()
            predicted = test_predictions["yhat"].to_numpy()

            mae = mean_absolute_error(actual, predicted)
            rmse = np.sqrt(mean_squared_error(actual, predicted))

            nonzero = actual != 0
            mape = (
                np.mean(
                    np.abs(
                        (actual[nonzero] - predicted[nonzero])
                        / actual[nonzero]
                    )
                ) * 100
                if nonzero.any()
                else np.nan
            )

            final_model = Prophet(
                yearly_seasonality="auto",
                weekly_seasonality=False,
                daily_seasonality=False,
                interval_width=0.95
            )
            final_model.fit(monthly[["ds", "y"]])

            future = final_model.make_future_dataframe(
                periods=horizon,
                freq="MS"
            )

            forecast = final_model.predict(future)

            st.subheader("6. Forecast Visualization")

            chart = go.Figure()

            chart.add_trace(go.Scatter(
                x=monthly["ds"],
                y=monthly["y"],
                mode="lines+markers",
                name="Actual Sales"
            ))

            chart.add_trace(go.Scatter(
                x=forecast["ds"],
                y=forecast["yhat"],
                mode="lines",
                name="Predicted Sales"
            ))

            chart.add_trace(go.Scatter(
                x=forecast["ds"],
                y=forecast["yhat_upper"],
                mode="lines",
                line=dict(width=0),
                showlegend=False
            ))

            chart.add_trace(go.Scatter(
                x=forecast["ds"],
                y=forecast["yhat_lower"],
                mode="lines",
                fill="tonexty",
                name="95% Uncertainty Interval",
                line=dict(width=0)
            ))

            chart.update_layout(
                title="Historical Sales and Future Forecast",
                xaxis_title="Month",
                yaxis_title="Sales",
                template="plotly_white"
            )

            st.plotly_chart(chart, use_container_width=True)

            st.subheader("7. Model Evaluation")

            x, y, z = st.columns(3)
            x.metric("MAE", f"{mae:,.2f}")
            y.metric("RMSE", f"{rmse:,.2f}")
            z.metric(
                "MAPE",
                f"{mape:.2f}%" if np.isfinite(mape) else "N/A"
            )

            st.caption(
                "Evaluation uses the last three observed months as a "
                "holdout test set. The final model is retrained on all "
                "available observations."
            )

            st.subheader("8. Future Sales Predictions")

            result = forecast.tail(horizon)[
                ["ds", "yhat", "yhat_lower", "yhat_upper"]
            ].copy()

            result.columns = [
                "Month",
                "Predicted Sales",
                "Lower Bound",
                "Upper Bound"
            ]

            st.dataframe(result, use_container_width=True)

            csv = result.to_csv(index=False).encode("utf-8")

            st.download_button(
                "Download Forecast CSV",
                data=csv,
                file_name="sales_forecast.csv",
                mime="text/csv"
            )

            st.success("Forecast generated successfully.")

        except Exception as error:
            st.error(f"Forecasting failed: {error}")

st.divider()
st.caption("Cynaris Internship | W10D5 | Sales Forecasting Dashboard")

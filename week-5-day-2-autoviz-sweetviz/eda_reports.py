
import os
import pandas as pd
import sweetviz as sv
from autoviz.AutoViz_Class import AutoViz_Class

# Load the dataset
df = pd.read_csv("indian_air_quality.csv")
print("Dataset loaded:", df.shape)

# Create output folders
os.makedirs("reports", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# Generate SweetViz report
print("Generating SweetViz report...")
report = sv.analyze(df)
report.show_html(
    filepath="reports/sweetviz_report.html",
    open_browser=False
)
print("SweetViz report saved.")

# Generate AutoViz charts
print("Generating AutoViz report...")
autoviz_df = df.copy()
autoviz_df.columns = [
    "country", "state", "city", "station", "last_update",
    "latitude", "longitude", "pollutant_type",
    "minimum_value", "maximum_value", "average_value"
]

try:
    AV = AutoViz_Class()
    AV.AutoViz(
        filename="",
        sep=",",
        depVar="",
        dfte=autoviz_df,
        header=0,
        verbose=1,
        lowess=False,
        chart_format="html",
        max_rows_analyzed=15000,
        max_cols_analyzed=30,
        save_plot_dir="outputs"
    )
    print("AutoViz completed.")
except Exception as e:
    print("AutoViz error:", e)

print("EDA script finished.")

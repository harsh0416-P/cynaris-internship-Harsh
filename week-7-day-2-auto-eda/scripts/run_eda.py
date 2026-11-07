from pathlib import Path

import pandas as pd
from ydata_profiling import ProfileReport
import sweetviz as sv

# Resolve paths relative to this script
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_DIR / "data" / "sales.csv"
REPORT_DIR = PROJECT_DIR / "reports"


def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading dataset...")
    df = pd.read_csv(DATA_PATH)
    print(f"Dataset loaded: {df.shape[0]} rows x {df.shape[1]} columns")

    print("Generating ydata-profiling report...")
    profile = ProfileReport(
        df,
        title="W7D2 - Sales Data Profiling Report",
        explorative=True,
        minimal=True
    )
    profile.to_file(REPORT_DIR / "profile_report.html")

    print("Generating SweetViz report...")
    sweetviz_report = sv.analyze(df)
    sweetviz_report.show_html(
        str(REPORT_DIR / "sweetviz_report.html"),
        open_browser=False
    )

    print("\nBoth EDA reports generated successfully.")
    print(f"Reports directory: {REPORT_DIR}")


if __name__ == "__main__":
    main()

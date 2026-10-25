
import logging
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "indian_air_quality.csv"
OUTPUT_FILE = BASE_DIR / "reliable_results.txt"
LOG_FILE = BASE_DIR / "error_log.txt"

logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.ERROR,
    format="%(asctime)s %(levelname)s %(message)s",
)

def main():
    try:
        df = pd.read_csv(DATA_FILE)

        questions = [
            ("1. How many records are in this dataset?",
             lambda: len(df)),
            ("2. Which states are represented?",
             lambda: sorted(df["state"].dropna().unique().tolist())),
            ("3. How many unique cities are represented?",
             lambda: df["city"].nunique()),
            ("4. Counts of each pollutant type",
             lambda: df["pollutant_id"].value_counts().to_dict()),
            ("5. Overall average pollutant_avg",
             lambda: round(df["pollutant_avg"].mean(), 2)),
            ("6. Five cities with highest average pollutant_avg",
             lambda: df.groupby("city")["pollutant_avg"]
                        .mean().nlargest(5).round(2).to_dict()),
            ("7. Average pollutant_avg by pollutant_id",
             lambda: df.groupby("pollutant_id")["pollutant_avg"]
                        .mean().round(2).to_dict()),
            ("8. Missing values by column",
             lambda: df.isna().sum().to_dict()),
            ("9. Records where pollutant_avg > 100",
             lambda: df.loc[
                 df["pollutant_avg"] > 100,
                 ["state", "city", "pollutant_id", "pollutant_avg"]
             ].to_string(index=False)),
            ("10. Average pollutant_avg by state and pollutant",
             lambda: df.groupby(["state", "pollutant_id"])
                        ["pollutant_avg"].mean().round(2).to_string()),
        ]

        with OUTPUT_FILE.open("w", encoding="utf-8") as output:
            output.write("INDIAN AIR QUALITY - ANALYSIS RESULTS\n")
            output.write(f"Dataset shape: {df.shape}\n\n")

            for question, operation in questions:
                print(f"\n{question}")
                output.write(f"{question}\n")
                try:
                    result = operation()
                    text = str(result)
                    print(text)
                    output.write(text + "\n\n")
                except Exception:
                    logging.exception("Analysis failed: %s", question)
                    print("Analysis failed; see error_log.txt")
                    output.write("Analysis failed; see error_log.txt\n\n")

        print(f"\nAll results saved to: {OUTPUT_FILE}")

    except Exception:
        logging.exception("Could not load or analyze dataset")
        print("Could not complete analysis. Check error_log.txt.")

if __name__ == "__main__":
    main()

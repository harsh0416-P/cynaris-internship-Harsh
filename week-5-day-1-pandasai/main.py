
import logging
from pathlib import Path

import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm.local_llm import LocalLLM

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "indian_air_quality.csv"
LOG_FILE = BASE_DIR / "error_log.txt"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.ERROR,
    format="%(asctime)s %(levelname)s %(message)s",
)

QUESTIONS = [
    "How many records are in this dataset?",
    "Which states are represented?",
    "How many unique cities are represented?",
    "What are the counts of each pollutant type?",
    "What is the average pollutant_avg across all records?",
    "Which five cities have the highest average pollutant_avg?",
    "What is the average pollutant_avg for each pollutant_id?",
    "Are there any missing values in the dataset?",
    "Which records have pollutant_avg greater than 100?",
    "Summarize the air quality data by state and pollutant.",
]


def main():
    if not DATA_FILE.exists() or DATA_FILE.stat().st_size == 0:
        print(f"CSV missing or empty: {DATA_FILE}")
        return

    try:
        df = pd.read_csv(DATA_FILE)
        required = {
            "state", "city", "pollutant_id",
            "pollutant_min", "pollutant_max", "pollutant_avg"
        }
        missing = required - set(df.columns)
        if missing:
            raise ValueError(f"Missing expected columns: {sorted(missing)}")

        print("Dataset loaded successfully")
        print("Shape:", df.shape)
        print("\nColumns:", df.columns.tolist())
        print("\nMissing values:\n", df.isna().sum())
        print("\nExact duplicate rows:", df.duplicated().sum())

        # Manual Pandas answers for comparison
        manual = {
            "record_count": len(df),
            "missing_values": df.isna().sum().to_dict(),
            "average_by_pollutant": (
                df.groupby("pollutant_id")["pollutant_avg"]
                .mean().round(2).to_dict()
            ),
        }

        print("\nMANUAL PANDAS RESULTS")
        for name, result in manual.items():
            print(f"{name}: {result}")

        # Requires Ollama running locally with llama3 downloaded.
        llm = LocalLLM(
            api_base="http://localhost:11434/v1",
            model="llama3",
        )
        sdf = SmartDataframe(df, config={"llm": llm})

        print("\nPANDASAI RESULTS")
        for i, question in enumerate(QUESTIONS, 1):
            try:
                result = sdf.chat(question)
                print(f"\n{i}. {question}\nResult: {result}")
            except Exception as exc:
                logging.exception("PandasAI query failed: %s", question)
                print(f"\n{i}. Query failed. Details saved to error_log.txt")

    except Exception:
        logging.exception("Dataset or initialization failure")
        print("An error occurred. Check error_log.txt")


if __name__ == "__main__":
    main()

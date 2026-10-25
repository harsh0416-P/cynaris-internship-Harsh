import logging
import time
from pathlib import Path

import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm.local_llm import LocalLLM

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "indian_air_quality.csv"
LOG_FILE = BASE_DIR / "error_log.txt"
RESULT_FILE = BASE_DIR / "pandasai_results.txt"

MODEL_NAME = "llama3.2:1b"
API_BASE = "http://localhost:11434/v1"

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

logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.ERROR,
    format="%(asctime)s %(levelname)s %(message)s",
)


def run_manual_comparisons(df):
    """Calculate three answers directly with Pandas."""
    return {
        "record_count": len(df),
        "missing_values": df.isna().sum().to_dict(),
        "average_by_pollutant": (
            df.groupby("pollutant_id")["pollutant_avg"]
            .mean()
            .round(2)
            .to_dict()
        ),
    }


def run_pandasai_questions(df):
    """Attempt all ten questions and continue after individual failures."""
    try:
        llm = LocalLLM(
            api_base=API_BASE,
            model=MODEL_NAME,
        )
        sdf = SmartDataframe(df, config={"llm": llm})
    except Exception:
        logging.exception("Could not initialize PandasAI or Ollama.")
        print("\nCould not initialize PandasAI. Check error_log.txt.")
        return

    with RESULT_FILE.open("w", encoding="utf-8") as output:
        output.write("PANDASAI NATURAL-LANGUAGE QUERY RESULTS\n\n")

        for number, question in enumerate(QUESTIONS, start=1):
            print(f"\n[{number}/{len(QUESTIONS)}] {question}")
            output.write(f"\n{number}. {question}\n")

            try:
                start = time.time()
                result = sdf.chat(question)
                elapsed = time.time() - start

                result_text = str(result)
                print("Result:", result_text)
                print(f"Time: {elapsed:.1f} seconds")

                output.write(f"Result: {result_text}\n")
                output.write(f"Time: {elapsed:.1f} seconds\n")

            except KeyboardInterrupt:
                print("\nStopped by user. Completed results were saved.")
                output.write("Remaining questions were not run.\n")
                break

            except Exception as exc:
                logging.exception(
                    "PandasAI query %s failed: %s",
                    number,
                    question,
                )
                message = f"FAILED: {type(exc).__name__}: {exc}"
                print(message)
                output.write(message + "\n")

    print(f"\nPandasAI results saved to: {RESULT_FILE}")
    print(f"Error log: {LOG_FILE}")


def main():
    if not DATA_FILE.exists() or DATA_FILE.stat().st_size == 0:
        print(f"CSV is missing or empty: {DATA_FILE}")
        return

    try:
        df = pd.read_csv(DATA_FILE)

        required = {
            "state",
            "city",
            "pollutant_id",
            "pollutant_min",
            "pollutant_max",
            "pollutant_avg",
        }
        missing = required - set(df.columns)

        if missing:
            raise ValueError(
                f"Missing expected columns: {sorted(missing)}"
            )

        print("=" * 55)
        print("WEEK 5 DAY 1 - PANDASAI")
        print("=" * 55)
        print("Dataset:", DATA_FILE.name)
        print("Shape:", df.shape)
        print("\nColumns:", df.columns.tolist())
        print("\nMissing values:\n", df.isna().sum())
        print("\nExact duplicate rows:", df.duplicated().sum())

        # Comparison 1: total record count
        # Comparison 2: missing-value counts
        # Comparison 3: average pollutant value by pollutant type
        manual_results = run_manual_comparisons(df)

        print("\n" + "=" * 55)
        print("MANUAL PANDAS RESULTS - BASELINE FOR COMPARISON")
        print("=" * 55)

        for name, result in manual_results.items():
            print(f"\n{name}: {result}")

        # Save manual results separately for review.
        manual_file = BASE_DIR / "manual_pandas_results.txt"
        with manual_file.open("w", encoding="utf-8") as output:
            output.write("MANUAL PANDAS RESULTS\n\n")
            for name, result in manual_results.items():
                output.write(f"{name}: {result}\n")

        print(f"\nManual results saved to: {manual_file}")

        # Run the ten natural-language queries using real PandasAI.
        run_pandasai_questions(df)

    except KeyboardInterrupt:
        print("\nProgram stopped by user.")

    except Exception:
        logging.exception("Dataset loading or main program failed.")
        print("\nAn error occurred. Check error_log.txt.")


if __name__ == "__main__":
    main()

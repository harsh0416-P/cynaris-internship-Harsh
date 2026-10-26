
import logging
from pathlib import Path

import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm.local_llm import LocalLLM

# Project settings
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "indian_air_quality.csv"
MODEL_NAME = "llama3.2:1b"
API_BASE = "http://localhost:11434/v1"

logging.basicConfig(
    filename=BASE_DIR / "error_log.txt",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def main():
    print("\n=== PandasAI Air Quality Assistant ===")

    if not DATA_FILE.exists():
        print(f"Dataset not found: {DATA_FILE}")
        return

    df = pd.read_csv(DATA_FILE)
    print(f"Dataset loaded: {len(df)} rows, {len(df.columns)} columns")

    try:
        llm = LocalLLM(
            api_base=API_BASE,
            model=MODEL_NAME,
        )

        sdf = SmartDataframe(df, config={"llm": llm})

    except Exception as exc:
        logging.exception("Failed to initialize PandasAI")
        print(f"Could not initialize PandasAI: {exc}")
        return

    print("\nType a question about the dataset.")
    print("Type 'exit' to quit.")
    print("Example: How many rows are present in this dataset?")

    while True:
        question = input("\nYour question: ").strip()

        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        if not question:
            continue

        try:
            answer = sdf.chat(question)
            print("\nAI answer:")
            print(answer)

        except Exception as exc:
            logging.exception("PandasAI query failed: %s", question)
            print(f"\nPandasAI could not answer: {exc}")
            print(
                "Try a simpler question, or use reliable_analysis.py "
                "for reproducible Pandas results."
            )

if __name__ == "__main__":
    main()


import pandas as pd
import logging
import time
from pathlib import Path
from pandasai import SmartDataframe
from pandasai.llm.local_llm import LocalLLM

# Create required folders
Path("logs").mkdir(exist_ok=True)
Path("outputs").mkdir(exist_ok=True)

# Configure error logging
logging.basicConfig(
    filename="logs/pandasai_errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    force=True
)

# Load dataset
df = pd.read_csv("data/sales.csv")
print("Dataset loaded:", df.shape)

# Configure local LLM
llm = LocalLLM(
    api_base="http://localhost:11434/v1",
    model="llama3.2:3b"
)

sdf = SmartDataframe(df, config={"llm": llm})

# Ten natural-language questions
questions = [
    "Calculate the total sum of Sales.",
    "What are the top 5 cities by total Sales?",
    "Which Category has the highest total Sales?",
    "Calculate the average Sales.",
    "Show total Sales grouped by Region.",
    "Which Segment generates the highest total Sales?",
    "Show the top 10 Product Names by total Sales.",
    "How many unique Order IDs are present?",
    "Which month has the highest total Sales? Use Order Date.",
    "Show total Sales grouped by Category."
]

# PandasAI sometimes returns errors as text instead of raising exceptions.
failure_markers = [
    "unfortunately, i was not able to answer",
    "no code found",
    "no result returned",
    "generated code includes import",
    "traceback",
    "error:"
]

results = []

for i, question in enumerate(questions, 1):
    print("\n" + "=" * 60)
    print(f"Query {i}: {question}")

    start = time.time()

    try:
        answer = sdf.chat(question)
        elapsed = round(time.time() - start, 2)
        answer_text = str(answer)

        failed = (
            not answer_text.strip()
            or any(marker in answer_text.lower()
                   for marker in failure_markers)
        )

        if failed:
            status = "Failed"
            logging.error(
                "PandasAI returned an error for query: %s | Answer: %s",
                question,
                answer_text
            )
        else:
            status = "Returned - verify manually"

        print("Answer:", answer_text)
        print("Status:", status)
        print("Time:", elapsed, "seconds")

        results.append({
            "Question": question,
            "Answer": answer_text,
            "Status": status,
            "Time_seconds": elapsed
        })

    except Exception as error:
        elapsed = round(time.time() - start, 2)
        logging.exception("Query execution failed: %s", question)

        print("Error:", error)

        results.append({
            "Question": question,
            "Answer": str(error),
            "Status": "Failed",
            "Time_seconds": elapsed
        })

# Save all results
results_df = pd.DataFrame(results)
results_df.to_csv("outputs/pandasai_results.csv", index=False)

print("\n" + "=" * 60)
print("FINAL QUERY SUMMARY")
print(results_df[["Question", "Status", "Time_seconds"]])

print("\nResults saved to outputs/pandasai_results.csv")
print("Error log saved to logs/pandasai_errors.log")

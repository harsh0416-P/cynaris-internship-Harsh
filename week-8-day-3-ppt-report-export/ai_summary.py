import os
from dotenv import load_dotenv
from groq import Groq

ENV_PATH = r"D:\Cynaris-Internship\week-8-day-1-executive-summary\.env"
load_dotenv(ENV_PATH)

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment file.")

client = Groq(api_key=api_key)

MODEL = "openai/gpt-oss-20b"


def generate_executive_summary(insights, total_sales=None):
    prompt = f"""
You are a professional data analyst.

Write a concise, factual executive summary of the Superstore Sales Dataset.

Dataset period: 2015 to 2018.
Total sales: {total_sales if total_sales is not None else "See supplied insights"}

Verified insights:
{insights}

STRICT RULES:
- Use only the supplied figures.
- Use a neutral, professional tone.
- Do not predict future growth or performance.
- Do not give business recommendations.
- Do not claim market share.
- Do not use the phrase year-to-date.
- Do not describe performance as stable, balanced, or positive.
- Do not invent causes or correlations.
- Mention only facts supported by the data.
- Keep the summary between 100 and 150 words.
- Return plain text without Markdown formatting.
- Never describe sales value as transaction or shipment frequency.
- Say "Standard Class recorded the highest shipping-mode sales".
- Do not describe the dataset as a complete financial picture.
"""

    print("Sending request to Groq...")

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        reasoning_effort="low",
        max_completion_tokens=4096
    )

    summary = response.choices[0].message.content

    if not summary or not summary.strip():
        raise ValueError("Groq returned an empty summary.")

    print("AI summary generated successfully.")
    return summary.strip()

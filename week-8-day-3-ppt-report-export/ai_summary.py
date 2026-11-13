
import os
from dotenv import load_dotenv
from groq import Groq

# Load existing W8D1 API configuration
ENV_PATH = (
    r"D:\Cynaris-Internship"
    r"\week-8-day-1-executive-summary\.env"
)

load_dotenv(ENV_PATH)

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("Groq API key not found. Check the W8D1 .env file.")

client = Groq(api_key=api_key)

MODEL = "openai/gpt-oss-120b"


def generate_executive_summary(insights):
    """Generate an approximately 200-word business summary."""

    prompt = f"""
You are a professional business data analyst.

Write an executive summary of approximately 200 words
using ONLY the following verified business insights.

DATASET: Superstore Sales Dataset
TOTAL SALES: $2,261,536.78

FIVE VERIFIED INSIGHTS:
{insights}

Requirements:
1. Explain the major business performance findings.
2. Include relevant figures and percentages.
3. Use professional business language.
4. Do not invent data or unsupported explanations.
5. Do not confuse sales revenue with profit.
6. Do not claim that correlation proves causation.
7. Include a short business outlook.
8. Target approximately 200 words.

Return only the executive summary.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=500
    )

    return response.choices[0].message.content


if __name__ == "__main__":

    business_insights = """
    1. Technology generated $827,455.87 (36.59%).
    2. West region generated $710,219.68 (31.40%).
    3. Consumer segment generated $1,148,060.53 (50.76%).
    4. Standard Class generated $1,340,831.31 (59.29%).
    5. 2018 generated $722,052.02 (31.93%).
    """

    print("Generating AI Executive Summary...\n")

    summary = generate_executive_summary(business_insights)

    print("=" * 60)
    print("AI EXECUTIVE SUMMARY")
    print("=" * 60)
    print(summary)

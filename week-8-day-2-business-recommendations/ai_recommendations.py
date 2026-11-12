
from pathlib import Path
import os

from dotenv import load_dotenv
from groq import Groq


BASE_DIR = Path(__file__).resolve().parent
MODEL = "openai/gpt-oss-120b"

# Reuse the existing W8D1 environment file
ENV_PATH = (
    BASE_DIR.parent
    / "week-8-day-1-executive-summary"
    / ".env"
)


def generate_recommendations(insights):
    """Generate an evidence-based business narrative using Groq."""

    load_dotenv(dotenv_path=ENV_PATH)

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY not configured.")

    client = Groq(api_key=api_key)

    # Prepare verified business data
    data = f"""
BUSINESS PERFORMANCE

Total customers: {insights['total_customers']}
Total revenue: Rs. {insights['total_revenue']:,.2f}
Total orders: {insights['total_orders']}
Average revenue per customer: Rs. {insights['average_revenue']:,.2f}
Average orders per customer: {insights['average_orders']:.2f}

CUSTOMER CHURN

Churned customers: {insights['churned_customers']}
Overall churn rate: {insights['churn_rate']:.2f}%

CITY PERFORMANCE
{insights['city_performance'].to_string()}

ACQUISITION CHANNEL PERFORMANCE
{insights['channel_performance'].to_string()}

AGE GROUP PERFORMANCE
{insights['age_performance'].to_string()}
"""

    prompt = f"""
You are an experienced business data analyst.

Analyze the verified business data below.

Produce two sections:

SECTION 1: EXECUTIVE SUMMARY
- Approximately 200 words.
- Explain the major business findings.
- Include relevant numerical evidence.

SECTION 2: FIVE BUSINESS RECOMMENDATIONS
For each recommendation provide:
1. Finding: What does the data show?
2. Recommendation: What should management investigate or test?
3. Expected business benefit: What potential improvement could this create?


IMPORTANT RULES:

- Use only the supplied verified data.
- Never invent numbers or business facts.
- Do not confuse revenue with profit.
- Do not describe churn as low or high without a benchmark.
- Do not invent reasons for customer churn.
- Do not claim correlation or causation without evidence.
- Clearly distinguish observations from recommendations.
- Do not calculate hypothetical financial benefits unless
  the assumptions and formula are explicitly stated.
- Never present fractional customers as actual retained customers.
- Do not assume churned customers have average customer revenue.
- Do not make arithmetic errors.
- Do not claim that zero observed churn proves a channel
  has better retention.
- Present recommendations as experiments to investigate,
  not guaranteed outcomes.
- Mention that the dataset contains 200 customers and
  6 customers flagged as churned.

VERIFIED DATA:
{data}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are an evidence-driven business analyst."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_completion_tokens=2500,
        temperature=0.2
    )

    if not response.choices:
        raise ValueError("Groq returned no response.")

    result = response.choices[0].message.content

    if not result or not result.strip():
        raise ValueError("Groq returned an empty response.")

    result = result.strip()

    output_path = BASE_DIR / "business_recommendations.txt"
    output_path.write_text(result, encoding="utf-8")

    print("\n===== AI BUSINESS RECOMMENDATIONS =====")
    print(result)
    print("\nSaved to:", output_path)

    return result

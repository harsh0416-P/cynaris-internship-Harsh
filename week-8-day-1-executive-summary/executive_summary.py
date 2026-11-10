
import pandas as pd

# 1. Load the customer dataset
file_path = "../project 1 Stakeholder brief + data inventory/data/da_customer_profiles.csv"

df = pd.read_csv(file_path)

# 2. Display basic information
print("\n========== DATASET OVERVIEW ==========")

print("Total customers:", len(df))
print("Total columns:", len(df.columns))

print("\nColumn names:")
print(df.columns.tolist())

# 3. Display sample records
print("\n========== FIRST 5 CUSTOMERS ==========")
print(df.head())

# 4. Check missing values
print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

# 5. Check data types
print("\n========== DATA TYPES ==========")
print(df.dtypes)

# ==========================================
# STEP 12: FIVE BUSINESS INSIGHTS
# ==========================================

print("\n========== INSIGHT 1: REVENUE BY CITY ==========")

city_revenue = (
    df.groupby("City")["Total_Revenue"]
    .sum()
    .sort_values(ascending=False)
)

print(city_revenue)


print("\n========== INSIGHT 2: REVENUE BY ACQUISITION CHANNEL ==========")

channel_revenue = (
    df.groupby("Acquisition_Channel")["Total_Revenue"]
    .sum()
    .sort_values(ascending=False)
)

print(channel_revenue)


print("\n========== INSIGHT 3: REVENUE BY AGE GROUP ==========")

age_revenue = (
    df.groupby("Age_Band")["Total_Revenue"]
    .sum()
    .sort_values(ascending=False)
)

print(age_revenue)


print("\n========== INSIGHT 4: CUSTOMER CHURN ==========")

total_customers = len(df)
churned_customers = (df["Churned"] == 1).sum()

churn_rate = (churned_customers / total_customers) * 100

print("Total customers:", total_customers)
print("Churned customers:", churned_customers)
print(f"Customer churn rate: {churn_rate:.2f}%")


print("\n========== INSIGHT 5: CUSTOMER VALUE ==========")

average_orders = df["Total_Orders"].mean()
average_revenue = df["Total_Revenue"].mean()

total_revenue = df["Total_Revenue"].sum()
total_orders = df["Total_Orders"].sum()

print(f"Average orders per customer: {average_orders:.2f}")
print(f"Average revenue per customer: ₹{average_revenue:,.2f}")
print(f"Total customer revenue: ₹{total_revenue:,.2f}")
print("Total orders:", total_orders)

# ==========================================
# STEP 19: GROQ EXECUTIVE SUMMARY GENERATOR
# ==========================================

from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
import os

# 1. Load API key securely
env_path = Path(__file__).with_name(".env")
load_dotenv(dotenv_path=env_path, override=True)

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found. Check your .env file.")

# 2. Connect to Groq
client = Groq(api_key=api_key)

# 3. Prepare the five calculated insights
insights = f"""
1. Revenue by city:
{city_revenue.to_string()}

2. Revenue by acquisition channel:
{channel_revenue.to_string()}

3. Revenue by age group:
{age_revenue.to_string()}

4. Customer churn:
Total customers: {total_customers}
Churned customers: {churned_customers}
Churn rate: {churn_rate:.2f}%

5. Customer value:
Average orders per customer: {average_orders:.2f}
Average revenue per customer: Rs. {average_revenue:,.2f}
Total revenue: Rs. {total_revenue:,.2f}
Total orders: {total_orders}
"""

# 4. Create the AI prompt
prompt = f"""
You are a professional business data analyst.

Write an executive summary of approximately 200 words
based ONLY on the following verified data insights.

Requirements:
- Use professional business language.
- Explain the most important findings.
- Highlight revenue performance by city, channel and age group.
- Explain the customer churn result accurately.
- Provide practical business recommendations.
- Do not invent statistics or unsupported explanations.
- Distinguish revenue totals from per-customer performance.
- Mention that the dataset contains 200 customers.
- Do not claim a monthly or annual churn rate.

DATA INSIGHTS:
{insights}
"""

# 5. Send the prompt to Groq
print("\n========== GENERATING EXECUTIVE SUMMARY ==========")

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "system",
            "content": "You are an accurate and evidence-driven business analyst."
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    max_completion_tokens=800,
    temperature=0.3
)

summary = response.choices[0].message.content

# 6. Display the result
print("\n========== AI EXECUTIVE SUMMARY ==========")
print(summary)

# 7. Save the summary to a text file
output_path = Path(__file__).with_name("executive_summary.txt")
output_path.write_text(summary, encoding="utf-8")

print("\nExecutive summary saved successfully!")
print("File:", output_path)

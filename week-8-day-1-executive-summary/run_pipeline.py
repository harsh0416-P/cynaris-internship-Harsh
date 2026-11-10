
from pathlib import Path
import os
import sys

import pandas as pd
from dotenv import load_dotenv
from groq import Groq

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION


# ==========================================
# 1. CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

NAVY = RGBColor(20, 39, 69)
BLUE = RGBColor(44, 112, 190)
LIGHT_BLUE = RGBColor(225, 237, 250)
WHITE = RGBColor(255, 255, 255)
DARK = RGBColor(48, 57, 70)
GREY = RGBColor(112, 124, 140)
LIGHT_GREY = RGBColor(244, 247, 251)

MODEL = "openai/gpt-oss-120b"


# ==========================================
# 2. LOAD AND VALIDATE CSV
# ==========================================

def load_dataset(csv_path):

    path = Path(csv_path).resolve()

    if not path.exists():
        raise FileNotFoundError(f"CSV not found: {path}")

    df = pd.read_csv(path)

    required = [
        "Customer_ID",
        "City",
        "Age_Band",
        "Acquisition_Channel",
        "Total_Orders",
        "Total_Revenue",
        "Churned"
    ]

    missing_columns = [
        col for col in required if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    if df.empty:
        raise ValueError("The CSV contains no records.")

    for col in ["Total_Orders", "Total_Revenue", "Churned"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    if df[["Total_Orders", "Total_Revenue", "Churned"]].isnull().any().any():
        raise ValueError("Numeric columns contain invalid or missing values.")

    if not df["Churned"].isin([0, 1]).all():
        raise ValueError("Churned must contain only 0 or 1.")

    print("\n========== DATASET OVERVIEW ==========")
    print("Rows:", len(df))
    print("Columns:", len(df.columns))
    print("Missing values:", int(df.isnull().sum().sum()))
    print("Duplicate customer IDs:", int(df["Customer_ID"].duplicated().sum()))

    return df


# ==========================================
# 3. CALCULATE FIVE INSIGHTS
# ==========================================

def calculate_insights(df):

    city_revenue = (
        df.groupby("City")["Total_Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    channel_revenue = (
        df.groupby("Acquisition_Channel")["Total_Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    age_revenue = (
        df.groupby("Age_Band")["Total_Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    total_customers = len(df)

    churned_customers = int((df["Churned"] == 1).sum())

    churn_rate = (
        churned_customers / total_customers
    ) * 100

    total_revenue = float(df["Total_Revenue"].sum())

    total_orders = int(df["Total_Orders"].sum())

    average_revenue = float(df["Total_Revenue"].mean())

    average_orders = float(df["Total_Orders"].mean())

    insights = {
        "city_revenue": city_revenue,
        "channel_revenue": channel_revenue,
        "age_revenue": age_revenue,
        "total_customers": total_customers,
        "churned_customers": churned_customers,
        "churn_rate": churn_rate,
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "average_revenue": average_revenue,
        "average_orders": average_orders
    }

    print("\n========== FIVE BUSINESS INSIGHTS ==========")

    print("\n1. Revenue by city:")
    print(city_revenue)

    print("\n2. Revenue by acquisition channel:")
    print(channel_revenue)

    print("\n3. Revenue by age group:")
    print(age_revenue)

    print("\n4. Customer churn:")
    print(f"{churned_customers}/{total_customers}")
    print(f"{churn_rate:.2f}%")

    print("\n5. Customer value:")
    print(f"Average revenue: Rs. {average_revenue:,.2f}")
    print(f"Average orders: {average_orders:.2f}")
    print(f"Total revenue: Rs. {total_revenue:,.2f}")
    print(f"Total orders: {total_orders}")

    return insights


# ==========================================
# 4. GENERATE GROQ EXECUTIVE SUMMARY
# ==========================================

def generate_ai_summary(insights):

    env_path = BASE_DIR / ".env"
    load_dotenv(dotenv_path=env_path, override=True)

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY not found in .env")

    client = Groq(api_key=api_key)

    data = f"""
Dataset: {insights['total_customers']} customers

Revenue by city:
{insights['city_revenue'].to_string()}

Revenue by acquisition channel:
{insights['channel_revenue'].to_string()}

Revenue by age group:
{insights['age_revenue'].to_string()}

Churned customer records: {insights['churned_customers']}
Churn percentage: {insights['churn_rate']:.2f}%

Total revenue: Rs. {insights['total_revenue']:,.2f}
Total orders: {insights['total_orders']}
Average revenue per customer: Rs. {insights['average_revenue']:,.2f}
Average orders per customer: {insights['average_orders']:.2f}
"""

    prompt = f"""
You are a professional business data analyst.

Write an executive summary of approximately 200 words.

Use ONLY the verified data below.

Requirements:
- Explain the major business findings.
- Discuss city, channel and age-group performance.
- Explain the churn percentage accurately.
- Include practical business recommendations.
- Do not invent figures or unsupported explanations.
- Do not claim that revenue totals prove individual
  customer spending performance.
- Do not claim a monthly or annual churn rate.
- Clearly distinguish facts from recommendations.

VERIFIED DATA:
{data}
"""

    print("\n========== GENERATING GROQ SUMMARY ==========")

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
        max_completion_tokens=2000,
        temperature=0.2
    )

   
    # Validate Groq response
    if not response.choices:
        raise ValueError("Groq returned no response choices.")

    choice = response.choices[0]
    summary = choice.message.content

    print("Groq finish reason:", choice.finish_reason)

    if not summary or not summary.strip():
        print("Groq returned an empty summary.")
        print(
            "Response details:",
            choice.message.model_dump(exclude={"content"})
        )
        raise ValueError("Groq returned an empty summary.")

    summary = summary.strip()


    output = BASE_DIR / "executive_summary.txt"
    output.write_text(summary, encoding="utf-8")

    print("\n========== EXECUTIVE SUMMARY ==========")
    print(summary)
    print("\nSummary saved:", output)

    return summary


# ==========================================
# 5. POWERPOINT HELPER FUNCTIONS
# ==========================================

def add_text(slide, text, x, y, w, h,
             size=18, color=DARK, bold=False,
             align=PP_ALIGN.LEFT):

    box = slide.shapes.add_textbox(
        Inches(x), Inches(y), Inches(w), Inches(h)
    )

    tf = box.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = str(text)
    p.alignment = align
    p.font.name = "Aptos"
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color

    return box


def add_background(slide, color=WHITE):

    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        0, 0, Inches(13.333), Inches(7.5)
    )

    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()

    slide.shapes._spTree.remove(shape._element)
    slide.shapes._spTree.insert(2, shape._element)


def add_card(slide, x, y, w, h, label, value, description):

    card = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(x), Inches(y), Inches(w), Inches(h)
    )

    card.fill.solid()
    card.fill.fore_color.rgb = LIGHT_GREY
    card.line.color.rgb = LIGHT_BLUE

    add_text(
        slide, label,
        x + 0.2, y + 0.18, w - 0.4, 0.35,
        11, GREY, True
    )

    add_text(
        slide, value,
        x + 0.2, y + 0.65, w - 0.4, 0.65,
        21, NAVY, True
    )

    add_text(
        slide, description,
        x + 0.2, y + 1.35, w - 0.4, 0.4,
        10, GREY
    )


def add_header(slide, title, section, page):

    add_text(
        slide, section.upper(),
        0.65, 0.3, 8, 0.3,
        10, BLUE, True
    )

    add_text(
        slide, title,
        0.65, 0.75, 12, 0.65,
        27, NAVY, True
    )

    add_text(
        slide, f"{page:02d} / 07",
        11.8, 7.08, 1, 0.2,
        9, GREY, align=PP_ALIGN.RIGHT
    )

    add_text(
        slide, "INDIAN BUSINESS CUSTOMER ANALYSIS",
        0.65, 7.08, 8, 0.2,
        9, GREY
    )


def add_chart(slide, series_data, x, y, w, h):

    data = CategoryChartData()
    data.categories = list(series_data.index.astype(str))
    data.add_series(
        "Revenue (Rs.)",
        list(series_data.values)
    )

    chart = slide.shapes.add_chart(
        XL_CHART_TYPE.BAR_CLUSTERED,
        Inches(x), Inches(y), Inches(w), Inches(h),
        data
    ).chart

    chart.has_legend = False
    chart.has_title = False

    plot = chart.plots[0]
    plot.has_data_labels = True
    plot.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
    plot.data_labels.font.size = Pt(10)
    plot.data_labels.number_format = '#,##0'

    series = chart.series[0]
    series.format.fill.solid()
    series.format.fill.fore_color.rgb = BLUE

    chart.category_axis.reverse_order = True

    chart.value_axis.has_major_gridlines = True

    return chart


def new_slide(prs, title, section, page):

    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_background(slide)
    add_header(slide, title, section, page)

    return slide


# ==========================================
# 6. GENERATE SEVEN-SLIDE POWERPOINT
# ==========================================

def generate_powerpoint(insights):

    prs = Presentation()

    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # SLIDE 1: TITLE
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, NAVY)

    add_text(
        slide, "DATA ANALYTICS | EXECUTIVE REPORT",
        1.2, 1.8, 10, 0.4, 13, LIGHT_BLUE, True
    )

    add_text(
        slide, "Indian Business\nCustomer Analysis",
        1.2, 2.5, 11, 1.7, 36, WHITE, True
    )

    add_text(
        slide, "Revenue • Customer behaviour • Recommendations",
        1.2, 4.6, 10, 0.5, 16, LIGHT_BLUE
    )

    add_text(
        slide, f"{insights['total_customers']} CUSTOMER RECORDS",
        1.2, 6.3, 8, 0.4, 12, WHITE, True
    )

    # SLIDE 2: CITY
    slide = new_slide(
        prs, "Revenue Performance by City",
        "Insight 01 | Geographic Performance", 2
    )

    add_chart(
        slide, insights["city_revenue"],
        0.8, 1.8, 7.4, 4.8
    )

    city = insights["city_revenue"].idxmax()
    city_value = insights["city_revenue"].max()

    add_text(
        slide, "TOP-PERFORMING CITY",
        8.6, 2.2, 3.7, 0.4, 15, BLUE, True
    )

    add_card(
        slide, 8.6, 3.2, 3.7, 1.8,
        "LEADING CITY",
        str(city),
        f"Revenue: Rs. {city_value:,.0f}"
    )

    # SLIDE 3: CHANNEL
    slide = new_slide(
        prs, "Revenue by Acquisition Channel",
        "Insight 02 | Channel Performance", 3
    )

    add_chart(
        slide, insights["channel_revenue"],
        0.8, 1.8, 7.4, 4.8
    )

    channel = insights["channel_revenue"].idxmax()
    channel_value = insights["channel_revenue"].max()
    channel_pct = channel_value / insights["total_revenue"] * 100

    add_text(
        slide, "LEADING CHANNEL",
        8.6, 2.2, 3.7, 0.4, 15, BLUE, True
    )

    add_card(
        slide, 8.6, 3.2, 3.7, 1.8,
        "TOP CHANNEL",
        str(channel),
        f"Rs. {channel_value:,.0f} | {channel_pct:.1f}% of revenue"
    )

    # SLIDE 4: AGE
    slide = new_slide(
        prs, "Revenue by Customer Age Group",
        "Insight 03 | Customer Segmentation", 4
    )

    add_chart(
        slide, insights["age_revenue"],
        0.8, 1.8, 7.4, 4.8
    )

    age = insights["age_revenue"].idxmax()
    age_value = insights["age_revenue"].max()

    add_text(
        slide, "TOP AGE SEGMENT",
        8.6, 2.2, 3.7, 0.4, 15, BLUE, True
    )

    add_card(
        slide, 8.6, 3.2, 3.7, 1.8,
        "HIGHEST REVENUE AGE GROUP",
        str(age),
        f"Revenue: Rs. {age_value:,.0f}"
    )

    # SLIDE 5: CHURN
    slide = new_slide(
        prs, "Customer Churn Overview",
        "Insight 04 | Customer Retention", 5
    )

    add_card(
        slide, 0.9, 2.1, 3.3, 2.0,
        "TOTAL CUSTOMERS",
        str(insights["total_customers"]),
        "Customer records analysed"
    )

    add_card(
        slide, 5.0, 2.1, 3.3, 2.0,
        "FLAGGED AS CHURNED",
        str(insights["churned_customers"]),
        "Customers with Churned = 1"
    )

    add_card(
        slide, 9.1, 2.1, 3.3, 2.0,
        "CHURN RATE",
        f"{insights['churn_rate']:.2f}%",
        "Share flagged as churned"
    )

    add_text(
        slide, "BUSINESS INTERPRETATION",
        1.0, 5.0, 6, 0.4, 14, BLUE, True
    )

    add_text(
        slide,
        "Investigate the customer records flagged as churned "
        "before designing targeted retention actions.",
        1.0, 5.5, 11.2, 0.8, 17, DARK
    )

    # SLIDE 6: CUSTOMER VALUE
    slide = new_slide(
        prs, "Customer Value and Revenue",
        "Insight 05 | Overall Business Performance", 6
    )

    add_card(
        slide, 0.9, 2.0, 3.5, 1.8,
        "TOTAL REVENUE",
        f"Rs. {insights['total_revenue']:,.0f}",
        "Revenue across customer records"
    )

    add_card(
        slide, 4.9, 2.0, 3.5, 1.8,
        "AVERAGE REVENUE",
        f"Rs. {insights['average_revenue']:,.0f}",
        "Per customer record"
    )

    add_card(
        slide, 8.9, 2.0, 3.5, 1.8,
        "TOTAL ORDERS",
        f"{insights['total_orders']:,}",
        "Recorded customer orders"
    )

    add_card(
        slide, 2.9, 4.4, 3.5, 1.8,
        "AVERAGE ORDERS",
        f"{insights['average_orders']:.2f}",
        "Per customer record"
    )

    add_card(
        slide, 6.9, 4.4, 3.5, 1.8,
        "CUSTOMERS",
        str(insights["total_customers"]),
        "Records analysed"
    )

    # SLIDE 7: RECOMMENDATIONS
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(slide, NAVY)

    add_text(
        slide, "FINAL SECTION | ACTION PLAN",
        0.8, 0.55, 8, 0.35, 12, LIGHT_BLUE, True
    )

    add_text(
        slide, "Business Recommendations",
        0.8, 1.05, 11, 0.8, 30, WHITE, True
    )

    recommendations = [
        (
            "01", "Geographic focus",
            f"Evaluate opportunities in {', '.join(insights['city_revenue'].head(3).index.astype(str))}."
        ),
        (
            "02", "Channel strategy",
            f"Investigate the {channel} channel's revenue performance before increasing investment."
        ),
        (
            "03", "Customer segmentation",
            f"Develop relevant campaigns for the {age} age segment."
        ),
        (
            "04", "Customer retention",
            f"Investigate the {insights['churned_customers']} customers flagged as churned."
        )
    ]

    y = 2.15

    for number, heading, description in recommendations:

        add_text(
            slide, number,
            0.9, y, 0.7, 0.5, 19, LIGHT_BLUE, True
        )

        add_text(
            slide, heading,
            1.8, y, 3.1, 0.4, 17, WHITE, True
        )

        add_text(
            slide, description,
            5.0, y, 7.2, 0.7, 15, LIGHT_BLUE
        )

        y += 1.05

    # SAVE AND VERIFY
    output = BASE_DIR / "executive_summary.pptx"
    prs.save(output)

    check = Presentation(output)

    if len(check.slides) != 7:
        raise ValueError("PowerPoint must contain seven slides.")

    print("\n========== POWERPOINT GENERATED ==========")
    print("Location:", output)
    print("Slides:", len(check.slides))


# ==========================================
# 7. RUN COMPLETE PIPELINE
# ==========================================

def main():

    if len(sys.argv) > 1:
        csv_path = sys.argv[1]
    else:
        csv_path = (
            BASE_DIR.parent
            / "project 1 Stakeholder brief + data inventory"
            / "data"
            / "da_customer_profiles.csv"
        )

    print("\n========== W8D1 EXECUTIVE SUMMARY PIPELINE ==========")

    df = load_dataset(csv_path)

    insights = calculate_insights(df)

    summary = generate_ai_summary(insights)

    generate_powerpoint(insights)

    print("\n========== PIPELINE COMPLETED ==========")
    print("CSV loaded successfully.")
    print("Five insights calculated.")
    print("Groq summary generated.")
    print("Seven-slide PowerPoint created.")
    print("\nAll outputs saved in:", BASE_DIR)


if __name__ == "__main__":
    main()

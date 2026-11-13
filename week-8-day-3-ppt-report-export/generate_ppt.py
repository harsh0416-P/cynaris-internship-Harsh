import os
import pandas as pd
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
from ai_summary import generate_executive_summary

DATA_PATH = r"D:\Cynaris-Internship\week-7-day-2-auto-eda\data\sales.csv"
OUTPUT_FILE = "superstore_business_report.pptx"

NAVY = RGBColor(25, 45, 75)
BLUE = RGBColor(40, 100, 180)
WHITE = RGBColor(255, 255, 255)
GREY = RGBColor(90, 100, 115)


def add_title(slide, title):
    box = slide.shapes.add_textbox(
        Inches(0.6), Inches(0.35), Inches(12), Inches(0.7)
    )
    p = box.text_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = NAVY


def add_footer(slide):
    box = slide.shapes.add_textbox(
        Inches(0.6), Inches(7.1), Inches(12), Inches(0.2)
    )
    p = box.text_frame.paragraphs[0]
    p.text = "Superstore Business Report"
    p.font.size = Pt(9)
    p.font.color.rgb = GREY


def add_chart_slide(prs, title, series):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title(slide, title)

    chart_data = CategoryChartData()
    chart_data.categories = [str(x) for x in series.index]
    chart_data.add_series("Sales", [float(x) for x in series.values])

    chart = slide.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_CLUSTERED,
        Inches(1), Inches(1.5), Inches(11), Inches(5),
        chart_data
    ).chart

    chart.has_title = True
    chart.chart_title.text_frame.text = title
    chart.has_legend = False
    chart.plots[0].has_data_labels = True
    chart.plots[0].data_labels.number_format = '$#,##0'

    add_footer(slide)


def main():
    print("Loading dataset...")
    df = pd.read_csv(DATA_PATH)
    df["Order Date"] = pd.to_datetime(
        df["Order Date"], dayfirst=True, errors="coerce"
    )
    df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
    df = df.dropna(subset=["Order Date", "Sales"])

    if df.empty:
        raise ValueError("No valid data found.")

    total_sales = df["Sales"].sum()

    category = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
    region = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
    segment = df.groupby("Segment")["Sales"].sum().sort_values(ascending=False)
    shipping = df.groupby("Ship Mode")["Sales"].sum().sort_values(ascending=False)
    yearly = df.groupby(df["Order Date"].dt.year)["Sales"].sum().sort_index()

    insights = f"""
    1. Technology sales: ${category.get('Technology', 0):,.2f}
    2. Leading region: {region.index[0]}, ${region.iloc[0]:,.2f}
    3. Leading segment: {segment.index[0]}, ${segment.iloc[0]:,.2f}
    4. Leading shipping mode: {shipping.index[0]}, ${shipping.iloc[0]:,.2f}
    5. Highest annual sales: {yearly.idxmax()}, ${yearly.max():,.2f}
    Total sales: ${total_sales:,.2f}
    """

    print("Generating Groq AI executive summary...")
    summary = generate_executive_summary(insights)

    if not summary:
        raise ValueError("AI summary was empty.")

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Slide 1: Title
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = NAVY

    box = slide.shapes.add_textbox(
        Inches(1), Inches(2.4), Inches(11), Inches(1.5)
    )
    p = box.text_frame.paragraphs[0]
    p.text = "SUPERSTORE BUSINESS SALES REPORT"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER

    # Slide 2: AI executive summary
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title(slide, "AI-Generated Executive Summary")

    box = slide.shapes.add_textbox(
        Inches(0.8), Inches(1.4), Inches(11.7), Inches(4.8)
    )
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = summary
    p.font.size = Pt(17)
    p.font.color.rgb = NAVY
    add_footer(slide)

    # Slides 3–7: Five data insights
    add_chart_slide(prs, "Sales by Category", category)
    add_chart_slide(prs, "Sales by Region", region)
    add_chart_slide(prs, "Sales by Customer Segment", segment)
    add_chart_slide(prs, "Sales by Shipping Mode", shipping)
    add_chart_slide(prs, "Yearly Sales", yearly)

    # Slide 8: Recommendations
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title(slide, "Business Recommendations")

    recommendations = [
        "Investigate the performance of the leading product category.",
        "Study regional sales patterns and customer demand.",
        "Review customer segment contributions.",
        "Compare shipping modes using delivery cost and time data.",
        "Compare yearly sales trends and investigate changes.",
        "Analyze profit and discount data before making profitability decisions."
    ]

    box = slide.shapes.add_textbox(
        Inches(0.9), Inches(1.5), Inches(11.5), Inches(5)
    )
    tf = box.text_frame

    for i, item in enumerate(recommendations):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"{i + 1}. {item}"
        p.font.size = Pt(19)
        p.font.color.rgb = NAVY
        p.space_after = Pt(18)

    add_footer(slide)

    prs.save(OUTPUT_FILE)

    print("\nPowerPoint generated successfully!")
    print(f"File: {OUTPUT_FILE}")
    print(f"Total slides: {len(prs.slides)}")
    print(f"Total sales: ${total_sales:,.2f}")


if __name__ == "__main__":
    main()

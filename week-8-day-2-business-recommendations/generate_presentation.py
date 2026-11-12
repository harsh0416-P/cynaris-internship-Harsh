
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN


BASE_DIR = Path(__file__).resolve().parent

NAVY = RGBColor(20, 39, 69)
BLUE = RGBColor(44, 112, 190)
WHITE = RGBColor(255, 255, 255)
DARK = RGBColor(48, 57, 70)


def add_title(slide, text):
    box = slide.shapes.add_textbox(
        Inches(0.6), Inches(0.4), Inches(12), Inches(0.8)
    )
    paragraph = box.text_frame.paragraphs[0]
    paragraph.text = text
    paragraph.font.size = Pt(28)
    paragraph.font.bold = True
    paragraph.font.color.rgb = NAVY


def add_content(slide, lines):
    box = slide.shapes.add_textbox(
        Inches(0.8), Inches(1.6), Inches(11.5), Inches(5.2)
    )

    frame = box.text_frame
    frame.word_wrap = True

    for index, line in enumerate(lines):
        paragraph = (
            frame.paragraphs[0]
            if index == 0
            else frame.add_paragraph()
        )

        paragraph.text = str(line)
        paragraph.font.size = Pt(19)
        paragraph.font.color.rgb = DARK
        paragraph.space_after = Pt(16)


def generate_presentation(insights, recommendations):

    prs = Presentation()
    prs.slide_width = Inches(13.33)
    prs.slide_height = Inches(7.5)

    # Slide 1: Title
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    title = slide.shapes.add_textbox(
        Inches(1), Inches(2.2), Inches(11), Inches(1.2)
    )

    paragraph = title.text_frame.paragraphs[0]
    paragraph.text = "Business Performance Report"
    paragraph.font.size = Pt(34)
    paragraph.font.bold = True
    paragraph.font.color.rgb = NAVY
    paragraph.alignment = PP_ALIGN.CENTER

    subtitle = slide.shapes.add_textbox(
        Inches(1), Inches(3.5), Inches(11), Inches(0.7)
    )

    p = subtitle.text_frame.paragraphs[0]
    p.text = "Customer Analytics and Business Recommendations"
    p.font.size = Pt(20)
    p.font.color.rgb = BLUE
    p.alignment = PP_ALIGN.CENTER

    # Slide 2: City performance
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title(slide, "City Performance")

    city = insights["city_performance"]

    lines = [
        f"{name}: Revenue Rs. {row['revenue']:,.0f}, "
        f"{int(row['customers'])} customers, "
        f"Churn {row['churn_rate']:.2f}%"
        for name, row in city.iterrows()
    ]

    add_content(slide, lines)

    # Slide 3: Acquisition channel
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title(slide, "Acquisition Channel Performance")

    channel = insights["channel_performance"]

    lines = [
        f"{name}: Revenue Rs. {row['revenue']:,.0f}, "
        f"Average revenue Rs. {row['average_revenue']:,.0f}, "
        f"Churn {row['churn_rate']:.2f}%"
        for name, row in channel.iterrows()
    ]

    add_content(slide, lines)

    # Slide 4: Age group
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title(slide, "Age Group Performance")

    age = insights["age_performance"]

    lines = [
        f"{name}: {int(row['customers'])} customers, "
        f"Revenue Rs. {row['revenue']:,.0f}, "
        f"Average Rs. {row['average_revenue']:,.0f}"
        for name, row in age.iterrows()
    ]

    add_content(slide, lines)

    # Slide 5: Churn
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title(slide, "Customer Churn Analysis")

    lines = [
        f"Total customers: {insights['total_customers']}",
        f"Churned customers: {insights['churned_customers']}",
        f"Observed churn rate: {insights['churn_rate']:.2f}%",
        "Pune: 3 churned customers",
        "Bangalore: 2 churned customers",
        "Offline channel: 3 churned customers"
    ]

    add_content(slide, lines)

    # Slide 6: Overall performance
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title(slide, "Overall Business Performance")

    lines = [
        f"Total revenue: Rs. {insights['total_revenue']:,.2f}",
        f"Total orders: {insights['total_orders']}",
        f"Total customers: {insights['total_customers']}",
        f"Average revenue per customer: "
        f"Rs. {insights['average_revenue']:,.2f}",
        f"Average orders per customer: "
        f"{insights['average_orders']:.2f}"
    ]

    add_content(slide, lines)

    # Slide 7: AI recommendations
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title(slide, "AI Business Recommendations")

    # Keep the text readable by splitting it into paragraphs.
    clean_lines = [
        line.strip()
        for line in recommendations.splitlines()
        if line.strip()
    ]

    add_content(slide, clean_lines[:12])

    output_path = BASE_DIR / "business_performance_report.pptx"

    prs.save(output_path)

    print("\nPowerPoint saved:", output_path)

    return output_path

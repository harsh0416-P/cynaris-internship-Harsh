
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION


# ==========================================
# 1. PRESENTATION CONFIGURATION
# ==========================================

prs = Presentation()

prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Corporate color palette
NAVY = RGBColor(20, 39, 69)
BLUE = RGBColor(44, 112, 190)
LIGHT_BLUE = RGBColor(225, 237, 250)
WHITE = RGBColor(255, 255, 255)
DARK = RGBColor(48, 57, 70)
GREY = RGBColor(112, 124, 140)
LIGHT_GREY = RGBColor(244, 247, 251)
GREEN = RGBColor(37, 139, 100)

OUTPUT = Path(__file__).with_name("executive_summary.pptx")


# ==========================================
# 2. HELPER FUNCTIONS
# ==========================================

def add_background(slide, color=WHITE):

    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        0, 0, prs.slide_width, prs.slide_height
    )

    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()

    # Move background behind all other objects
    slide.shapes._spTree.remove(shape._element)
    slide.shapes._spTree.insert(2, shape._element)


def add_text(
    slide, text, x, y, w, h,
    size=18, color=DARK, bold=False,
    align=PP_ALIGN.LEFT
):

    textbox = slide.shapes.add_textbox(
        Inches(x), Inches(y),
        Inches(w), Inches(h)
    )

    tf = textbox.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.04)
    tf.margin_right = Inches(0.04)
    tf.margin_top = Inches(0.04)

    paragraph = tf.paragraphs[0]
    paragraph.text = str(text)
    paragraph.alignment = align

    paragraph.font.name = "Aptos"
    paragraph.font.size = Pt(size)
    paragraph.font.bold = bold
    paragraph.font.color.rgb = color

    return textbox


def add_card(slide, x, y, w, h, label, value, description=""):

    card = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(x), Inches(y),
        Inches(w), Inches(h)
    )

    card.fill.solid()
    card.fill.fore_color.rgb = LIGHT_GREY
    card.line.color.rgb = LIGHT_BLUE

    add_text(
        slide, label,
        x + 0.2, y + 0.18, w - 0.4, 0.35,
        12, GREY, True
    )

    add_text(
        slide, value,
        x + 0.2, y + 0.65, w - 0.4, 0.65,
        23, NAVY, True
    )

    if description:
        add_text(
            slide, description,
            x + 0.2, y + 1.35, w - 0.4, 0.4,
            10, GREY
        )


def add_header(slide, title, section):

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

    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0.65), Inches(1.48),
        Inches(12), Inches(0.025)
    )

    line.fill.solid()
    line.fill.fore_color.rgb = LIGHT_BLUE
    line.line.fill.background()


def add_footer(slide, page):

    add_text(
        slide, "INDIAN BUSINESS CUSTOMER ANALYSIS",
        0.65, 7.08, 8, 0.2,
        9, GREY
    )

    add_text(
        slide, f"{page:02d} / 07",
        11.8, 7.08, 1, 0.2,
        9, GREY,
        align=PP_ALIGN.RIGHT
    )


def new_content_slide(title, section, page):

    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_background(slide)
    add_header(slide, title, section)
    add_footer(slide, page)

    return slide


def add_bar_chart(slide, labels, values, x, y, w, h):

    data = CategoryChartData()
    data.categories = labels
    data.add_series("Revenue (Rs.)", values)

    chart = slide.shapes.add_chart(
        XL_CHART_TYPE.BAR_CLUSTERED,
        Inches(x), Inches(y),
        Inches(w), Inches(h),
        data
    ).chart

    chart.has_legend = False
    chart.has_title = False
    chart.chart_style = 10

    plot = chart.plots[0]
    plot.has_data_labels = True

    plot.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
    plot.data_labels.font.size = Pt(10)
    plot.data_labels.font.color.rgb = DARK
    plot.data_labels.number_format = '#,##0'

    series = chart.series[0]
    series.format.fill.solid()
    series.format.fill.fore_color.rgb = BLUE
    series.format.line.fill.background()

    chart.category_axis.reverse_order = True
    chart.category_axis.tick_labels.font.size = Pt(11)
    chart.category_axis.tick_labels.font.color.rgb = DARK

    chart.value_axis.tick_labels.font.size = Pt(9)
    chart.value_axis.tick_labels.font.color.rgb = GREY
    chart.value_axis.has_major_gridlines = True

    return chart


def add_finding(slide, heading, message):

    add_text(
        slide, heading,
        8.6, 2.2, 3.7, 0.45,
        15, BLUE, True
    )

    add_text(
        slide, message,
        8.6, 2.8, 3.7, 1.5,
        17, DARK
    )


# ==========================================
# 3. VERIFIED DATA
# ==========================================

total_revenue = 4992621

cities = [
    "Pune", "Mumbai", "Hyderabad",
    "Delhi", "Bangalore", "Chennai"
]

city_values = [
    1102350, 926771, 847312,
    767386, 720507, 628295
]

channels = [
    "App", "Offline", "Website", "Marketplace"
]

channel_values = [
    1468234, 1299449, 1242438, 982500
]

age_groups = [
    "45-54", "55+", "18-24", "25-34", "35-44"
]

age_values = [
    1365174, 1075519, 1002911, 883331, 665686
]

# Calculate percentages using actual totals
app_percentage = (1468234 / total_revenue) * 100
pune_percentage = (1102350 / total_revenue) * 100
age_percentage = (1365174 / total_revenue) * 100


# ==========================================
# 4. SLIDE 1 — TITLE
# ==========================================

slide = prs.slides.add_slide(prs.slide_layouts[6])

add_background(slide, NAVY)

accent = slide.shapes.add_shape(
    MSO_SHAPE.RECTANGLE,
    Inches(0.9), Inches(1.65),
    Inches(0.12), Inches(3.8)
)

accent.fill.solid()
accent.fill.fore_color.rgb = BLUE
accent.line.fill.background()

add_text(
    slide, "DATA ANALYTICS | EXECUTIVE REPORT",
    1.35, 1.8, 10, 0.4,
    13, LIGHT_BLUE, True
)

add_text(
    slide, "Indian Business\nCustomer Analysis",
    1.3, 2.5, 10.8, 1.8,
    36, WHITE, True
)

add_text(
    slide,
    "Revenue performance • Customer behaviour • Business recommendations",
    1.35, 4.65, 10.5, 0.7,
    16, LIGHT_BLUE
)

add_text(
    slide, "WEEK 8 | DAY 1",
    1.35, 6.45, 5, 0.35,
    12, WHITE, True
)

add_text(
    slide, "200 CUSTOMER RECORDS",
    8.6, 6.45, 3.5, 0.35,
    12, WHITE, True,
    align=PP_ALIGN.RIGHT
)


# ==========================================
# 5. SLIDE 2 — REVENUE BY CITY
# ==========================================

slide = new_content_slide(
    "Revenue Performance by City",
    "Insight 01 | Geographic Performance",
    2
)

add_bar_chart(
    slide, cities, city_values,
    0.8, 1.85, 7.3, 4.7
)

add_finding(
    slide,
    "TOP-PERFORMING CITY",
    "Pune leads with Rs. 11,02,350 in total customer revenue."
)

add_card(
    slide, 8.6, 4.8, 3.7, 1.65,
    "PUNE REVENUE",
    "Rs. 11.02 Lakh",
    f"{pune_percentage:.1f}% of total revenue"
)


# ==========================================
# 6. SLIDE 3 — ACQUISITION CHANNEL
# ==========================================

slide = new_content_slide(
    "Revenue by Acquisition Channel",
    "Insight 02 | Channel Performance",
    3
)

add_bar_chart(
    slide, channels, channel_values,
    0.8, 1.85, 7.3, 4.7
)

add_finding(
    slide,
    "LEADING CHANNEL",
    "The App channel contributes the highest total revenue."
)

add_card(
    slide, 8.6, 4.8, 3.7, 1.65,
    "APP REVENUE",
    "Rs. 14.68 Lakh",
    f"{app_percentage:.1f}% of total revenue"
)


# ==========================================
# 7. SLIDE 4 — AGE GROUP
# ==========================================

slide = new_content_slide(
    "Revenue by Customer Age Group",
    "Insight 03 | Customer Segmentation",
    4
)

add_bar_chart(
    slide, age_groups, age_values,
    0.8, 1.85, 7.3, 4.7
)

add_finding(
    slide,
    "TOP AGE SEGMENT",
    "Customers aged 45–54 generate the highest total revenue."
)

add_card(
    slide, 8.6, 4.8, 3.7, 1.65,
    "AGE 45–54",
    "Rs. 13.65 Lakh",
    f"{age_percentage:.1f}% of total revenue"
)


# ==========================================
# 8. SLIDE 5 — CUSTOMER CHURN
# ==========================================

slide = new_content_slide(
    "Customer Churn Overview",
    "Insight 04 | Customer Retention",
    5
)

# Corrected card widths and positions
add_card(
    slide, 0.9, 2.1, 3.3, 2.0,
    "TOTAL CUSTOMERS",
    "200",
    "Customer records analysed"
)

add_card(
    slide, 5.0, 2.1, 3.3, 2.0,
    "FLAGGED AS CHURNED",
    "6",
    "Customers with Churned = 1"
)

add_card(
    slide, 9.1, 2.1, 3.3, 2.0,
    "CHURN RATE",
    "3.00%",
    "Share flagged as churned"
)

add_text(
    slide, "BUSINESS INTERPRETATION",
    1.0, 5.0, 6, 0.4,
    14, BLUE, True
)

add_text(
    slide,
    "Six customer records are flagged as churned. "
    "Investigate their profiles and churn status before "
    "designing targeted retention actions.",
    1.0, 5.5, 11.2, 0.9,
    17, DARK
)


# ==========================================
# 9. SLIDE 6 — CUSTOMER VALUE
# ==========================================

slide = new_content_slide(
    "Customer Value and Revenue",
    "Insight 05 | Overall Business Performance",
    6
)

add_card(
    slide, 0.9, 2.0, 3.5, 1.8,
    "TOTAL REVENUE",
    "Rs. 49.93 Lakh",
    "Revenue across 200 customer records"
)

add_card(
    slide, 4.9, 2.0, 3.5, 1.8,
    "AVERAGE REVENUE",
    "Rs. 24,963",
    "Per customer"
)

add_card(
    slide, 8.9, 2.0, 3.5, 1.8,
    "TOTAL ORDERS",
    "2,307",
    "Recorded customer orders"
)

add_card(
    slide, 2.9, 4.4, 3.5, 1.8,
    "AVERAGE ORDERS",
    "11.54",
    "Per customer"
)

add_card(
    slide, 6.9, 4.4, 3.5, 1.8,
    "CUSTOMERS",
    "200",
    "Records analysed"
)


# ==========================================
# 10. SLIDE 7 — RECOMMENDATIONS
# ==========================================

slide = prs.slides.add_slide(prs.slide_layouts[6])

add_background(slide, NAVY)

add_text(
    slide, "FINAL SECTION | ACTION PLAN",
    0.8, 0.55, 8, 0.35,
    12, LIGHT_BLUE, True
)

add_text(
    slide, "Business Recommendations",
    0.8, 1.05, 11, 0.8,
    30, WHITE, True
)

recommendations = [
    (
        "01",
        "Geographic focus",
        "Evaluate localized campaigns in Pune, Mumbai and Hyderabad."
    ),
    (
        "02",
        "Channel strategy",
        "Investigate the App channel's revenue performance before increasing investment."
    ),
    (
        "03",
        "Customer segmentation",
        "Develop relevant campaigns for the 45–54 and 55+ age groups."
    ),
    (
        "04",
        "Customer retention",
        "Investigate the six customers flagged as churned and identify possible retention actions."
    )
]

y = 2.15

for number, heading, description in recommendations:

    add_text(
        slide, number,
        0.9, y, 0.7, 0.5,
        19, LIGHT_BLUE, True
    )

    add_text(
        slide, heading,
        1.8, y, 3.1, 0.4,
        17, WHITE, True
    )

    add_text(
        slide, description,
        5.0, y, 7.2, 0.7,
        15, LIGHT_BLUE
    )

    y += 1.05

add_text(
    slide, "END OF EXECUTIVE REPORT",
    0.9, 6.75, 7, 0.3,
    10, WHITE, True
)


# ==========================================
# 11. SAVE AND VERIFY PRESENTATION
# ==========================================

prs.save(OUTPUT)

# Reopen file to verify its structure
check = Presentation(OUTPUT)

print("\n========== PRESENTATION GENERATED ==========")
print("File:", OUTPUT)
print("Total slides:", len(check.slides))
print("File size:", round(OUTPUT.stat().st_size / 1024, 2), "KB")

if len(check.slides) == 7:
    print("SUCCESS: All seven slides verified.")
else:
    raise ValueError("Presentation must contain exactly seven slides.")


import io
import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from dotenv import load_dotenv
from groq import Groq

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR


# =====================================================
# 1. CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Business Intelligence Studio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).resolve().parent

ENV_PATH = (
    BASE_DIR.parent
    / "week-8-day-1-executive-summary"
    / ".env"
)

MODEL = "openai/gpt-oss-120b"

REQUIRED_COLUMNS = [
    "Customer_ID",
    "City",
    "Age_Band",
    "Acquisition_Channel",
    "Total_Orders",
    "Total_Revenue",
    "Churned"
]

NAVY = RGBColor(20, 39, 69)
BLUE = RGBColor(44, 112, 190)
LIGHT = RGBColor(238, 244, 251)
DARK = RGBColor(48, 57, 70)
WHITE = RGBColor(255, 255, 255)


# =====================================================
# 2. CUSTOM DASHBOARD DESIGN
# =====================================================

st.markdown("""
<style>
    .stApp {
        background-color: #0e1422;
        color: #e8edf5;
    }

    [data-testid="stSidebar"] {
        background-color: #141d30;
    }

    .main-title {
        font-size: 34px;
        font-weight: 750;
        color: #f0f5ff;
        margin-bottom: 4px;
    }

    .subtitle {
        color: #9caec8;
        font-size: 14px;
        margin-bottom: 25px;
    }

    .metric-card {
        background: linear-gradient(145deg, #1c2940, #172238);
        border: 1px solid #30415e;
        border-radius: 14px;
        padding: 20px;
        min-height: 120px;
    }

    .metric-label {
        color: #a8b8d0;
        font-size: 13px;
    }

    .metric-value {
        color: #ffffff;
        font-size: 27px;
        font-weight: 700;
        margin-top: 9px;
    }

    .section-heading {
        font-size: 21px;
        font-weight: 700;
        color: #eaf1ff;
        margin-top: 25px;
        margin-bottom: 12px;
    }

    .insight-card {
        background: #1a263b;
        border: 1px solid #344662;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
    }

    .small-muted {
        color: #a8b8d0;
        font-size: 13px;
    }

    div[data-testid="stDownloadButton"] button {
        background-color: #2563eb;
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: 600;
    }

    div[data-testid="stDownloadButton"] button:hover {
        background-color: #1d4ed8;
        color: white;
    }
</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. CSV LOADING AND VALIDATION
# =====================================================

def load_dataset(uploaded_file):

    df = pd.read_csv(uploaded_file)

    missing_columns = [
        col for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    if df.empty:
        raise ValueError("The uploaded CSV is empty.")

    if df["Customer_ID"].duplicated().any():
        raise ValueError("Duplicate Customer_ID values found.")

    if df[REQUIRED_COLUMNS].isnull().any().any():
        raise ValueError(
            "Missing values found in required columns."
        )

    for col in ["Total_Orders", "Total_Revenue", "Churned"]:
        df[col] = pd.to_numeric(df[col], errors="raise")

    if not df["Churned"].isin([0, 1]).all():
        raise ValueError("Churned must contain only 0 or 1.")

    if (df["Total_Orders"] < 0).any():
        raise ValueError("Total_Orders cannot be negative.")

    if (df["Total_Revenue"] < 0).any():
        raise ValueError("Total_Revenue cannot be negative.")

    return df


# =====================================================
# 4. BUSINESS ANALYSIS
# =====================================================

def calculate_insights(df):

    total_customers = len(df)

    total_revenue = float(df["Total_Revenue"].sum())

    total_orders = int(df["Total_Orders"].sum())

    average_revenue = float(df["Total_Revenue"].mean())

    average_orders = float(df["Total_Orders"].mean())

    churned_customers = int(df["Churned"].sum())

    churn_rate = (
        churned_customers / total_customers
    ) * 100

    # City analysis
    city = (
        df.groupby("City")
        .agg(
            customers=("Customer_ID", "count"),
            revenue=("Total_Revenue", "sum"),
            average_revenue=("Total_Revenue", "mean"),
            churned=("Churned", "sum")
        )
        .reset_index()
    )

    city["churn_rate"] = (
        city["churned"] / city["customers"] * 100
    )

    city = city.sort_values("revenue", ascending=False)

    # Acquisition channel analysis
    channel = (
        df.groupby("Acquisition_Channel")
        .agg(
            customers=("Customer_ID", "count"),
            revenue=("Total_Revenue", "sum"),
            average_revenue=("Total_Revenue", "mean"),
            churned=("Churned", "sum")
        )
        .reset_index()
    )

    channel["churn_rate"] = (
        channel["churned"] / channel["customers"] * 100
    )

    channel = channel.sort_values(
        "revenue", ascending=False
    )

    # Age group analysis
    age = (
        df.groupby("Age_Band")
        .agg(
            customers=("Customer_ID", "count"),
            revenue=("Total_Revenue", "sum"),
            average_revenue=("Total_Revenue", "mean")
        )
        .reset_index()
    )

    age = age.sort_values(
        "revenue", ascending=False
    )

    return {
        "total_customers": total_customers,
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "average_revenue": average_revenue,
        "average_orders": average_orders,
        "churned_customers": churned_customers,
        "churn_rate": churn_rate,
        "city": city,
        "channel": channel,
        "age": age
    }


# =====================================================
# 5. GROQ AI RECOMMENDATIONS
# =====================================================

def generate_ai_report(insights):

    load_dotenv(ENV_PATH)

    api_key = __import__("os").getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "Groq API key not found. Check the W8D1 .env file."
        )

    client = Groq(api_key=api_key)

    data = {
        "total_customers": insights["total_customers"],
        "total_revenue": insights["total_revenue"],
        "total_orders": insights["total_orders"],
        "average_revenue": insights["average_revenue"],
        "average_orders": insights["average_orders"],
        "churned_customers": insights["churned_customers"],
        "churn_rate": insights["churn_rate"],
        "city_performance": insights["city"].to_dict("records"),
        "channel_performance": insights["channel"].to_dict("records"),
        "age_performance": insights["age"].to_dict("records")
    }

    data_json = json.dumps(
        data,
        indent=2,
        default=lambda value: (
            value.item() if hasattr(value, "item")
            else str(value)
        )
    )

    prompt = f"""
You are an evidence-driven business data analyst.

Analyze the following verified customer dataset.

Return a JSON object with exactly these keys:

{{
  "executive_summary": "Approximately 180-220 words",
  "recommendations": [
    {{
      "title": "Short recommendation title",
      "finding": "Verified numerical observation",
      "action": "Specific experiment or investigation",
      "benefit": "Potential benefit, without unsupported financial claims"
    }}
  ]
}}

Return exactly FIVE recommendations.

RULES:
- Use only supplied data.
- Never invent numbers.
- Do not confuse revenue with profit.
- Do not call churn low or high without a benchmark.
- Do not invent churn causes.
- Do not claim correlation or causation without evidence.
- Do not assume a customer will behave like an average customer.
- Do not use fractional customers as actual outcomes.
- Distinguish facts from proposed actions.
- Do not claim that a zero-churn sample proves a channel is safer.
- Present recommendations as experiments, not guaranteed outcomes.
- Do not include Markdown fences around the JSON.
- Never invent or alter numerical metrics.
- Use exact values from the supplied dataset.
- Do not calculate revenue gaps unless verified.
- Do not claim profitability improvements because cost data is unavailable.
- If a metric is not supplied, do not estimate it.
CURRENCY AND REPORTING RULES:
- All revenue values are in Indian Rupees (INR).
- Always use ₹ or INR. Never use $ or USD.
- Do not describe churn as low, high, modest, or severe
  without a supplied benchmark.
- Use neutral terms such as "observed churn rate".
- Never invent industry benchmarks.
- Clearly distinguish observed findings from hypotheses.
- Treat recommendations as experiments, not proven solutions.

VERIFIED DATA:
{data_json}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "Return valid JSON only. Be precise and evidence-driven."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format={"type": "json_object"},
        temperature=0.2,
        max_completion_tokens=3000
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError("Groq returned an empty response.")

    report = json.loads(content)

    if not isinstance(report.get("executive_summary"), str):
        raise ValueError("Invalid executive summary in AI response.")

    recommendations = report.get("recommendations")

    if not isinstance(recommendations, list) or len(recommendations) != 5:
        raise ValueError(
            "AI response must contain exactly five recommendations."
        )

    for recommendation in recommendations:
        for field in ["title", "finding", "action", "benefit"]:
            if not isinstance(recommendation.get(field), str):
                raise ValueError(
                    f"Recommendation is missing valid field: {field}"
                )

    return report


# =====================================================
# 6. POWERPOINT GENERATION
# =====================================================

def add_slide_title(slide, title, subtitle=None):

    box = slide.shapes.add_textbox(
        Inches(0.65),
        Inches(0.4),
        Inches(12),
        Inches(0.8)
    )

    paragraph = box.text_frame.paragraphs[0]
    paragraph.text = title
    paragraph.font.size = Pt(28)
    paragraph.font.bold = True
    paragraph.font.color.rgb = NAVY

    if subtitle:
        sub = slide.shapes.add_textbox(
            Inches(0.7),
            Inches(1.2),
            Inches(11.5),
            Inches(0.5)
        )

        p = sub.text_frame.paragraphs[0]
        p.text = subtitle
        p.font.size = Pt(13)
        p.font.color.rgb = DARK


def add_bullet_list(slide, lines):

    box = slide.shapes.add_textbox(
        Inches(0.9),
        Inches(1.8),
        Inches(11.4),
        Inches(4.9)
    )

    frame = box.text_frame
    frame.word_wrap = True

    for index, line in enumerate(lines):

        p = (
            frame.paragraphs[0]
            if index == 0
            else frame.add_paragraph()
        )

        p.text = str(line)
        p.font.size = Pt(18)
        p.font.color.rgb = DARK
        p.space_after = Pt(17)


def create_powerpoint(insights, report):

    prs = Presentation()
    prs.slide_width = Inches(13.33)
    prs.slide_height = Inches(7.5)

    # Slide 1: Title
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_slide_title(
        slide,
        "Business Intelligence Report",
        "Customer Analytics | Business Recommendations"
    )

    add_bullet_list(
        slide,
        [
            "Customer performance analysis",
            "Revenue and acquisition channel analysis",
            "Customer churn investigation",
            "AI-generated business recommendations"
        ]
    )

    # Slide 2: Executive summary
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_slide_title(slide, "Executive Summary")

    add_bullet_list(
        slide,
        [
            report["executive_summary"]
        ]
    )

    # Slide 3: City performance
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_slide_title(slide, "City Performance")

    add_bullet_list(
        slide,
        [
            f"{row.City}: Revenue Rs. {row.revenue:,.0f}, "
            f"{row.customers} customers, "
            f"churn {row.churn_rate:.2f}%"
            for row in insights["city"].itertuples()
        ]
    )

    # Slide 4: Channel performance
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_slide_title(slide, "Acquisition Channel Performance")

    add_bullet_list(
        slide,
        [
            f"{row.Acquisition_Channel}: "
            f"Revenue Rs. {row.revenue:,.0f}, "
            f"average revenue Rs. {row.average_revenue:,.0f}, "
            f"churn {row.churn_rate:.2f}%"
            for row in insights["channel"].itertuples()
        ]
    )

    # Slide 5: Age group
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_slide_title(slide, "Age Group Performance")

    add_bullet_list(
        slide,
        [
            f"{row.Age_Band}: {row.customers} customers, "
            f"Revenue Rs. {row.revenue:,.0f}, "
            f"average Rs. {row.average_revenue:,.0f}"
            for row in insights["age"].itertuples()
        ]
    )

    # Slide 6: Churn
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_slide_title(slide, "Customer Churn")

    add_bullet_list(
        slide,
        [
            f"Total customers: {insights['total_customers']}",
            f"Churned customers: {insights['churned_customers']}",
            f"Observed churn rate: {insights['churn_rate']:.2f}%",
            "Churn distribution varies by city and acquisition channel."
        ]
    )

    # Slides 7-11: One recommendation per slide
    for index, recommendation in enumerate(
        report["recommendations"], start=1
    ):

        slide = prs.slides.add_slide(prs.slide_layouts[6])

        add_slide_title(
            slide,
            f"Recommendation {index}: {recommendation['title']}"
        )

        add_bullet_list(
            slide,
            [
                "FINDING: " + recommendation["finding"],
                "ACTION: " + recommendation["action"],
                "POTENTIAL BENEFIT: " + recommendation["benefit"]
            ]
        )

    # Save to memory for Streamlit download
    output = io.BytesIO()
    prs.save(output)
    output.seek(0)

    return output.getvalue()


# =====================================================
# 7. SIDEBAR
# =====================================================

st.sidebar.markdown("## 📊 BI Studio")

st.sidebar.caption("Cynaris Internship | Week 8 Day 2")

st.sidebar.markdown("---")

uploaded_file = st.sidebar.file_uploader(
    "Upload customer CSV",
    type=["csv"]
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "Upload a dataset containing customer, revenue, "
    "acquisition and churn information."
)


# =====================================================
# 8. MAIN HEADER
# =====================================================

st.markdown(
    '<div class="main-title">Business Intelligence Studio</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Explore customer performance, discover insights, '
    'and generate AI-powered business recommendations.'
    '</div>',
    unsafe_allow_html=True
)


# =====================================================
# 9. DATA UPLOAD AND VALIDATION
# =====================================================

if uploaded_file is None:

    st.info("Upload your customer CSV file using the sidebar.")

    st.markdown("### Required CSV columns")

    st.code(
        "Customer_ID, City, Age_Band, "
        "Acquisition_Channel, Total_Orders, "
        "Total_Revenue, Churned"
    )

    st.stop()


try:

    df = load_dataset(uploaded_file)

except Exception as error:

    st.error(f"Dataset validation failed: {error}")
    st.stop()


st.success(
    f"Dataset validated successfully: {len(df)} customers loaded."
)


# =====================================================
# 10. FILTERS
# =====================================================

st.markdown(
    '<div class="section-heading">Analytics Filters</div>',
    unsafe_allow_html=True
)

f1, f2, f3 = st.columns(3)

with f1:
    selected_cities = st.multiselect(
        "Select cities",
        sorted(df["City"].unique()),
        default=sorted(df["City"].unique())
    )

with f2:
    selected_channels = st.multiselect(
        "Acquisition channels",
        sorted(df["Acquisition_Channel"].unique()),
        default=sorted(df["Acquisition_Channel"].unique())
    )

with f3:
    selected_ages = st.multiselect(
        "Age groups",
        sorted(df["Age_Band"].unique()),
        default=sorted(df["Age_Band"].unique())
    )

# Track filter changes and invalidate outdated AI reports
current_filter_signature = (
    tuple(sorted(selected_cities)),
    tuple(sorted(selected_channels)),
    tuple(sorted(selected_ages))
)

if (
    "previous_filter_signature" not in st.session_state
    or st.session_state["previous_filter_signature"]
    != current_filter_signature
):
    st.session_state.pop("ai_report", None)
    st.session_state.pop("ppt_bytes", None)
    st.session_state["previous_filter_signature"] = (
        current_filter_signature
    )
filtered_df = df[
    df["City"].isin(selected_cities)
    & df["Acquisition_Channel"].isin(selected_channels)
    & df["Age_Band"].isin(selected_ages)
].copy()


if filtered_df.empty:

    st.warning("No customers match the selected filters.")
    st.stop()


insights = calculate_insights(filtered_df)


# =====================================================
# 11. KPI CARDS
# =====================================================

st.markdown(
    '<div class="section-heading">Business Overview</div>',
    unsafe_allow_html=True
)


def metric_card(label, value):

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


m1, m2, m3, m4 = st.columns(4)

with m1:
    metric_card(
        "Total Customers",
        f"{insights['total_customers']:,}"
    )

with m2:
    metric_card(
        "Total Revenue",
        f"₹{insights['total_revenue']:,.0f}"
    )

with m3:
    metric_card(
        "Total Orders",
        f"{insights['total_orders']:,}"
    )

with m4:
    metric_card(
        "Observed Churn",
        f"{insights['churn_rate']:.2f}%"
    )


st.markdown("")


# =====================================================
# 12. INTERACTIVE CHARTS
# =====================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🏙️ City Analysis",
        "📱 Acquisition",
        "👥 Age Groups",
        "⚠️ Churn Analysis"
    ]
)


with tab1:

    st.markdown("### Revenue by City")

    fig = px.bar(
        insights["city"],
        x="City",
        y="revenue",
        color="revenue",
        text_auto=".2s",
        title="Total Revenue by City",
        color_continuous_scale="Blues"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0e1422",
        plot_bgcolor="#0e1422"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        insights["city"],
        use_container_width=True,
        hide_index=True
    )


with tab2:

    st.markdown("### Acquisition Channel Performance")

    fig = px.bar(
        insights["channel"],
        x="Acquisition_Channel",
        y="average_revenue",
        color="average_revenue",
        text_auto=".2s",
        title="Average Revenue per Customer",
        color_continuous_scale="Teal"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0e1422",
        plot_bgcolor="#0e1422"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        insights["channel"],
        use_container_width=True,
        hide_index=True
    )


with tab3:

    st.markdown("### Age Group Revenue")

    fig = px.bar(
        insights["age"],
        x="Age_Band",
        y="revenue",
        color="average_revenue",
        text_auto=".2s",
        title="Revenue by Age Group",
        color_continuous_scale="Viridis"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0e1422",
        plot_bgcolor="#0e1422"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        insights["age"],
        use_container_width=True,
        hide_index=True
    )


with tab4:

    st.markdown("### Customer Churn Distribution")

    churn_data = pd.DataFrame({
        "Status": ["Active", "Churned"],
        "Customers": [
            insights["total_customers"]
            - insights["churned_customers"],
            insights["churned_customers"]
        ]
    })

    fig = px.pie(
        churn_data,
        names="Status",
        values="Customers",
        hole=0.55,
        title="Customer Status Distribution"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0e1422"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Churn by City")

    st.dataframe(
        insights["city"][
            ["City", "customers", "churned", "churn_rate"]
        ],
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# 13. AI REPORT
# =====================================================

st.markdown(
    '<div class="section-heading">AI Business Intelligence</div>',
    unsafe_allow_html=True
)

st.caption(
    "Generate an executive summary and five evidence-based "
    "recommendations using Groq."
)


if st.button(
    "✨ Generate AI Business Recommendations",
    type="primary",
    use_container_width=True
):

    with st.spinner("Groq is analyzing your business data..."):

        try:

            report = generate_ai_report(insights)

            st.session_state["ai_report"] = report

            st.success("AI report generated successfully.")

        except Exception as error:

            st.error(f"AI generation failed: {error}")


if "ai_report" in st.session_state:

    report = st.session_state["ai_report"]

    st.markdown("### Executive Summary")

    st.markdown(
        f'<div class="insight-card">'
        f'{report["executive_summary"]}'
        f'</div>',
        unsafe_allow_html=True
    )

    st.markdown("### Five Business Recommendations")

    for index, recommendation in enumerate(
        report["recommendations"], start=1
    ):

        with st.expander(
            f"{index}. {recommendation['title']}",
            expanded=True
        ):

            st.markdown("**Finding**")
            st.write(recommendation["finding"])

            st.markdown("**Recommended action**")
            st.write(recommendation["action"])

            st.markdown("**Potential benefit**")
            st.write(recommendation["benefit"])


    # =================================================
    # 14. POWERPOINT DOWNLOAD
    # =================================================

    st.markdown("### Download Executive Presentation")

    if st.button("Prepare PowerPoint"):

        with st.spinner("Building your presentation..."):

            try:

                ppt_bytes = create_powerpoint(
                    insights,
                    report
                )

                st.session_state["ppt_bytes"] = ppt_bytes

                st.success("PowerPoint created successfully.")

            except Exception as error:

                st.error(f"PowerPoint generation failed: {error}")


    if "ppt_bytes" in st.session_state:

        st.download_button(
            label="⬇ Download Business Performance Report",
            data=st.session_state["ppt_bytes"],
            file_name="business_performance_report.pptx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "presentationml.presentation"
            ),
            use_container_width=True
        )


# =====================================================
# 15. FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "Cynaris Internship | Week 8 Day 2 | "
    "Business Intelligence Studio"
)

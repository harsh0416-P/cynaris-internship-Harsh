
from data_analysis import load_dataset, calculate_insights
from ai_recommendations import generate_recommendations
from generate_presentation import generate_presentation


def main():

    print("\n========== W8D2 BUSINESS RECOMMENDATIONS ==========")

    # Step 1: Load CSV
    df = load_dataset()

    # Step 2: Calculate business insights
    insights = calculate_insights(df)

    print("\nBusiness insights calculated successfully.")

    # Step 3: Generate AI recommendations
    recommendations = generate_recommendations(insights)

    # Step 4: Generate PowerPoint
    presentation = generate_presentation(
        insights,
        recommendations
    )

    print("\n========== PIPELINE COMPLETED ==========")
    print("AI report:", "business_recommendations.txt")
    print("PowerPoint:", presentation.name)


if __name__ == "__main__":
    main()

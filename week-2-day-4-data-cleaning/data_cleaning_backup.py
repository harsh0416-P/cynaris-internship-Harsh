
import pandas as pd
import numpy as np
from pathlib import Path

# Create a sample dataset with common data-quality problems
df = pd.DataFrame({
    "name": [" Alice ", "BOB", "alice", "David ", None, "Eva"],
    "age": [25, 30, np.nan, 200, 40, 28],
    "salary": [30000, 45000, 35000, 50000, np.nan, 1000000],
    "city": ["Bangalore", "mumbai", "BANGALORE ", "Delhi", "Pune", None],
    "department": ["IT", "HR", "IT", "Finance", "HR", "IT"]
})

# Save the original dataset
df.to_csv("original_dataset.csv", index=False)

# 1. Inspect missing values and duplicates
missing_before = df.isnull().sum()
duplicates_before = int(df.duplicated().sum())

# 2. Standardise text values
for col in ["name", "city", "department"]:
    df[col] = df[col].str.strip().str.title()

# 3. Impute missing values
df["age"] = df["age"].fillna(df["age"].median())
df["salary"] = df["salary"].fillna(df["salary"].median())
df["city"] = df["city"].fillna(df["city"].mode()[0])
df["name"] = df["name"].fillna("Unknown")

# 4. Detect outliers using the IQR method and cap them
outlier_log = []

for col in ["age", "salary"]:
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    count = int(((df[col] < lower) | (df[col] > upper)).sum())
    outlier_log.append(
        f"{col}: {count} outliers detected; capped to [{lower:.2f}, {upper:.2f}]"
    )

    df[col] = df[col].clip(lower=lower, upper=upper)

# 5. Remove duplicate rows, if any
df = df.drop_duplicates()

# 6. Save cleaned dataset
df.to_csv("cleaned_dataset.csv", index=False)

# 7. Before/after quality comparison
comparison = pd.DataFrame({
    "Metric": [
        "Rows",
        "Missing values",
        "Duplicate rows"
    ],
    "Before": [
        6,
        int(missing_before.sum()),
        duplicates_before
    ],
    "After": [
        len(df),
        int(df.isnull().sum().sum()),
        int(df.duplicated().sum())
    ]
})

comparison.to_csv("data_quality_comparison.csv", index=False)

# 8. Document cleaning decisions
log = [
    "# Data Cleaning Log",
    "",
    "## Dataset",
    "Sample employee dataset created for Week 2 Day 4 practice.",
    "",
    "## Missing values before cleaning",
    missing_before.to_string(),
    "",
    "## Cleaning decisions",
    "- Standardised text by trimming whitespace and applying title case.",
    "- Filled missing age and salary with their median values.",
    "- Filled missing city with its mode and missing name with 'Unknown'.",
    "- Detected outliers using the 1.5 × IQR rule and capped numeric values.",
    "- Removed duplicate rows where present.",
    "",
    "## Outlier detection",
    *[f"- {item}" for item in outlier_log],
    "",
    "## Before/after quality comparison",
    comparison.to_string(index=False),
    "",
    "## Final missing values",
    df.isnull().sum().to_string()
]

Path("cleaning_log.md").write_text("\n".join(log), encoding="utf-8")

print("Data cleaning completed successfully!")
print("\nBefore/after comparison:")
print(comparison)
print("\nCleaned dataset:")
print(df)

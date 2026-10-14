# Week 3 — Day 2: DAX Basics

## 1. Total Sales Measure

```dax
Total Sales = SUM('sales_data'[Sales])
```

**Explanation:** Adds all sales values and displays the total. The result changes dynamically when report filters are applied.

## 2. CALCULATE() — Sales by Region

```dax
Sales by Region =
CALCULATE(
    [Total Sales],
    'sales_data'[Region] = "South"
)
```

**Explanation:** CALCULATE evaluates the Total Sales measure with a filter for the South region. Replace `"South"` with a region present in the dataset.

## 3. Year-to-Date (YTD) Sales

```dax
YTD Sales =
CALCULATE(
    [Total Sales],
    DATESYTD('sales_data'[Date])
)
```

**Explanation:** Calculates sales from the beginning of the year up to the current date in the date context. A proper date column and date table are recommended for time intelligence.

## 4. Running Total Using EARLIER()

```dax
Running Total =
CALCULATE(
    SUM('sales_data'[Sales]),
    FILTER(
        'sales_data',
        'sales_data'[Date] <= EARLIER('sales_data'[Date])
    )
)
```

**Explanation:** This calculated column adds sales for rows with dates up to the current row's date. EARLIER accesses the outer row context. For large datasets, a running-total measure is often more flexible.

## 5. Profit Margin Percentage

```dax
Profit Margin % =
DIVIDE(
    SUM('sales_data'[Profit]),
    SUM('sales_data'[Sales]),
    0
) * 100
```

**Explanation:** Calculates profit as a percentage of sales. DIVIDE safely handles division by zero. This example assumes the dataset has a Profit column.

## Key Concepts

- **Measure:** Calculated dynamically when a visual or report filter changes.
- **Calculated column:** Calculated for each row during data refresh.
- **Row context:** Refers to the current row being evaluated.
- **Filter context:** The filters affecting a calculation.
- **Context transition:** CALCULATE can convert row context into filter context.

**Note:** Check the actual table and column names in Power BI. Replace `sales_data`, `Sales`, `Date`, `Region`, and `Profit` if your dataset uses different names.
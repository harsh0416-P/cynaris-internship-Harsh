
import json
import re
import pandas as pd
import plotly.express as px

from pandasai import SmartDataframe
from pandasai.llm.local_llm import LocalLLM


class CSVAnalyzer:

    def __init__(self, dataframe):
        self.df = dataframe.copy()

        self.llm = LocalLLM(
            api_base="http://localhost:11434/v1",
            model="llama3.2:3b"
        )

        self.sdf = SmartDataframe(
            self.df,
            config={"llm": self.llm, "verbose": False}
        )

    def get_dataset_info(self):
        return {
            "rows": int(len(self.df)),
            "columns_count": int(len(self.df.columns)),
            "columns": self.df.columns.tolist(),
            "missing_values": {
                str(k): int(v)
                for k, v in self.df.isnull().sum().items()
            },
            "preview": json.loads(
                self.df.head(5).to_json(
                    orient="records",
                    date_format="iso"
                )
            )
        }

    def find_column(self, names):
        for name in names:
            for col in self.df.columns:
                if str(col).strip().lower() == name.lower():
                    return col
        return None

    def find_group_column(self, question):
        q = question.lower()

        keywords = [
            "sub-category", "subcategory",
            "category", "region", "city",
            "state", "segment", "ship mode"
        ]

        for keyword in keywords:
            if keyword in q:
                col = self.find_column([keyword])
                if col is not None:
                    return col

        return None

    def find_measure_column(self, question):
        q = question.lower()

        if "quantity" in q:
            col = self.find_column(["quantity"])
            if col is not None:
                return col

        if "profit" in q:
            col = self.find_column(["profit"])
            if col is not None:
                return col

        col = self.find_column(["sales", "revenue", "amount"])

        if col is not None:
            return col

        numeric = self.df.select_dtypes(
            include="number"
        ).columns.tolist()

        return numeric[0] if numeric else None

    def pandas_analysis(self, question):
        q = question.lower().strip()

        if "how many rows" in q or "row count" in q:
            return f"Total rows: {len(self.df)}"

        if "how many columns" in q or "column count" in q:
            return f"Total columns: {len(self.df.columns)}"

        if "column names" in q or "list columns" in q:
            return ", ".join(map(str, self.df.columns))

        if "missing" in q or "null values" in q:
            missing = self.df.isnull().sum()
            details = {
                str(k): int(v)
                for k, v in missing.items() if v > 0
            }
            return (
                f"Total missing values: {int(missing.sum())}\n"
                f"Details: {details}"
            )

        if "first" in q and "row" in q:
            match = re.search(r"first\s+(\d+)", q)
            count = int(match.group(1)) if match else 5
            return self.df.head(min(count, 20)).to_string(index=False)

        if "unique order" in q:
            col = self.find_column(["Order ID"])
            if col is not None:
                return f"Unique orders: {self.df[col].nunique()}"

        group_col = self.find_group_column(q)
        measure = self.find_measure_column(q)

        if "unique" in q and group_col is not None:
            return str(self.df[group_col].dropna().unique().tolist())

        if measure is None:
            return None

        series = pd.to_numeric(
            self.df[measure], errors="coerce"
        ).dropna()

        if "average" in q or "mean" in q:
            return f"Average {measure}: {series.mean():,.2f}"

        if "maximum" in q or "highest value" in q:
            return f"Maximum {measure}: {series.max():,.2f}"

        if "minimum" in q or "lowest value" in q:
            return f"Minimum {measure}: {series.min():,.2f}"

        if group_col is not None:
            grouped = (
                self.df.groupby(group_col)[measure]
                .sum()
                .sort_values(ascending=False)
            )

            if "highest" in q or "top" in q:
                return (
                    f"Highest {measure} by {group_col}: "
                    f"{grouped.index[0]} "
                    f"({grouped.iloc[0]:,.2f})"
                )

            if "lowest" in q:
                return (
                    f"Lowest {measure} by {group_col}: "
                    f"{grouped.index[-1]} "
                    f"({grouped.iloc[-1]:,.2f})"
                )

            return (
                f"Total {measure} by {group_col}:\n"
                f"{grouped.to_string()}"
            )

        if "total" in q or "sum" in q or "revenue" in q:
            return f"Total {measure}: {series.sum():,.2f}"

        return None

    def generate_chart(self, question):
        q = question.lower()

        group_col = self.find_group_column(q)
        measure = self.find_measure_column(q)

        if group_col is None or measure is None:
            return None

        if not any(word in q for word in [
            "chart", "graph", "visual",
            "by", "each", "distribution"
        ]):
            return None

        aggregated = (
            self.df.groupby(group_col)[measure]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        labels = aggregated[group_col].fillna(
            "Unknown"
        ).astype(str).tolist()

        values = aggregated[measure].astype(float).tolist()

        chart_type = "pie" if "pie" in q else "bar"

        if chart_type == "pie":
            fig = px.pie(
                aggregated,
                names=group_col,
                values=measure,
                title=f"{measure} by {group_col}"
            )
        else:
            fig = px.bar(
                aggregated,
                x=group_col,
                y=measure,
                title=f"{measure} by {group_col}"
            )

        return {
            "plotly_json": fig.to_json(),
            "chartjs": {
                "type": chart_type,
                "labels": labels,
                "datasets": [{
                    "label": f"Total {measure}",
                    "data": values
                }]
            }
        }

    def analyze(self, question):
        if not question or not question.strip():
            raise ValueError("Question cannot be empty.")

        answer = self.pandas_analysis(question)
        source = "pandas"

        if answer is None:
            try:
                answer = str(self.sdf.chat(question))

                if (
                    "no code found in the response" in answer.lower()
                    or "unfortunately, i was not able to answer" in answer.lower()
                ):
                    raise RuntimeError(answer)

                source = "pandasai"

            except Exception as error:
                raise RuntimeError(
                    f"PandasAI analysis failed: {error}"
                ) from error

        chart = self.generate_chart(question)

        return {
            "success": True,
            "question": question,
            "answer": str(answer),
            "answer_source": source,
            "chart": chart
        }

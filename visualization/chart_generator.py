
import pandas as pd
import plotly.express as px


def create_chart(query_result):
    """
    Create an interactive chart from SQL query results.
    Returns a Plotly figure or None if no suitable chart exists.
    """

    if not isinstance(query_result, dict):
        return None

    columns = query_result.get("columns", [])
    rows = query_result.get("rows", [])

    if not columns or not rows:
        return None

    try:
        dataframe = pd.DataFrame(rows, columns=columns)

        if dataframe.empty:
            return None

        # Identify numeric columns, including numeric values
        # returned by MySQL as Decimal or string objects.
        for column in dataframe.columns:
            if dataframe[column].dtype == "object":
                converted = pd.to_numeric(
                    dataframe[column], errors="coerce"
                )
                if converted.notna().all():
                    dataframe[column] = converted

        numeric_columns = dataframe.select_dtypes(
            include="number"
        ).columns.tolist()

        categorical_columns = [
            column
            for column in dataframe.columns
            if column not in numeric_columns
        ]

        # Case 1: A category and a numeric value
        if categorical_columns and numeric_columns:
            x_column = categorical_columns[0]
            y_column = numeric_columns[0]

            chart_data = dataframe

            if len(chart_data) > 30:
                chart_data = chart_data.head(30)

            figure = px.bar(
                chart_data,
                x=x_column,
                y=y_column,
                title=f"{y_column} by {x_column}",
                labels={
                    x_column: x_column.replace("_", " ").title(),
                    y_column: y_column.replace("_", " ").title(),
                },
                hover_data=[x_column, y_column],
            )

            figure.update_layout(
                template="plotly_white",
                xaxis_tickangle=-35,
                margin=dict(l=30, r=30, t=70, b=100),
            )
            return figure

        # Case 2: Two or more numeric columns
        if len(numeric_columns) >= 2:
            figure = px.scatter(
                dataframe,
                x=numeric_columns[0],
                y=numeric_columns[1],
                title=(
                    f"{numeric_columns[1]} vs "
                    f"{numeric_columns[0]}"
                ),
            )
            figure.update_layout(template="plotly_white")
            return figure

        # Case 3: One numeric column
        if len(numeric_columns) == 1:
            figure = px.histogram(
                dataframe,
                x=numeric_columns[0],
                title=f"Distribution of {numeric_columns[0]}",
            )
            figure.update_layout(template="plotly_white")
            return figure

        return None

    except (ValueError, TypeError, KeyError) as error:
        print(f"Could not create chart: {error}")
        return None


if __name__ == "__main__":
    sample_result = {
        "columns": ["product_name", "total_sales"],
        "rows": [
            {"product_name": "Laptop", "total_sales": 150000},
            {"product_name": "Phone", "total_sales": 90000},
            {"product_name": "Headphones", "total_sales": 25000},
            {"product_name": "Keyboard", "total_sales": 12000},
            {"product_name": "Mouse", "total_sales": 8000},
        ],
    }

    chart = create_chart(sample_result)

    if chart is not None:
        chart.show()
    else:
        print("No suitable chart could be created.")
id="chartgen"

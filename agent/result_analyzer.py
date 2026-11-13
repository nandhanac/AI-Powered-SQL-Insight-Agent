
import pandas as pd


def analyze_results(query_result):
    """
    Analyze query results locally using Pandas.

    Expected input:
    {
        "columns": ["product_name", "price"],
        "rows": [
            {"product_name": "Laptop", "price": 65000},
            {"product_name": "Mouse", "price": 800}
        ],
        "row_count": 2
    }
    """

    if not isinstance(query_result, dict):
        return {
            "success": False,
            "error": "Query result must be a dictionary."
        }

    if "error" in query_result:
        return {
            "success": False,
            "error": "Cannot analyze failed query results."
        }

    columns = query_result.get("columns", [])
    rows = query_result.get("rows", [])

    if not isinstance(columns, list) or not isinstance(rows, list):
        return {
            "success": False,
            "error": "Invalid columns or rows format."
        }

    if not columns:
        return {
            "success": False,
            "error": "No columns are available to analyze."
        }

    try:
        dataframe = pd.DataFrame(rows, columns=columns)

        summary = {
            "row_count": len(dataframe),
            "column_count": len(dataframe.columns),
            "columns": list(dataframe.columns),
            "column_types": {
                column: str(dataframe[column].dtype)
                for column in dataframe.columns
            },
            "missing_values": {
                column: int(dataframe[column].isna().sum())
                for column in dataframe.columns
            },
            "duplicate_rows": int(dataframe.duplicated().sum()),
        }

        # Calculate descriptive statistics for numeric columns.
        numeric_columns = dataframe.select_dtypes(
            include="number"
        ).columns

        numeric_summary = {}

        for column in numeric_columns:
            series = dataframe[column].dropna()

            if not series.empty:
                numeric_summary[column] = {
                    "minimum": float(series.min()),
                    "maximum": float(series.max()),
                    "average": float(series.mean()),
                    "median": float(series.median()),
                }

        summary["numeric_summary"] = numeric_summary

        # Generate simple observations from the returned data.
        observations = []

        if dataframe.empty:
            observations.append(
                "The query returned no rows."
            )
        else:
            observations.append(
                f"The query returned {len(dataframe)} rows "
                f"and {len(dataframe.columns)} columns."
            )

        for column, stats in numeric_summary.items():
            observations.append(
                f"{column}: minimum {stats['minimum']}, "
                f"maximum {stats['maximum']}, "
                f"average {stats['average']:.2f}."
            )

        return {
            "success": True,
            "summary": summary,
            "observations": observations,
        }

    except (TypeError, ValueError, KeyError) as error:
        return {
            "success": False,
            "error": f"Could not analyze results: {error}"
        }


if __name__ == "__main__":
    # Sample data for testing; no database connection is used.
    sample_result = {
        "columns": ["product_name", "price"],
        "rows": [
            {"product_name": "Laptop", "price": 65000},
            {"product_name": "Smartphone", "price": 35000},
            {"product_name": "Headphones", "price": 5000},
            {"product_name": "T-Shirt", "price": 1200},
            {"product_name": "Jeans", "price": 2500},
        ],
        "row_count": 5,
    }

    result = analyze_results(sample_result)

    print("\n--- RESULT ANALYSIS ---")

    if result["success"]:
        print("\nSummary:")
        print(result["summary"])

        print("\nObservations:")
        for observation in result["observations"]:
            print("-", observation)
    else:
        print("Error:", result["error"])
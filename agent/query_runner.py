
from agent.sql_generator import generate_sql
from agent.insight_generator import generate_insights
from tools.database_tools import execute_sql
from visualization.chart_generator import create_chart

def answer_question(question):
    # Step 1: Generate and validate SQL
    generated = generate_sql(question)

    if not generated.get("success"):
        return {
            "success": False,
            "stage": "sql_generation",
            "error": generated.get(
                "error", "SQL generation failed."
            ),
        }

    query = generated["query"]

    # Step 2: Execute SQL through the existing safety checks
    result = execute_sql(query)

    if "error" in result:
        return {
            "success": False,
            "stage": "sql_execution",
            "query": query,
            "error": result["error"],
        }

    # Step 3: Collect the successful query results
    query_result = {
        "columns": result["columns"],
        "rows": result["rows"],
        "row_count": result["row_count"],
        "truncated": result.get("truncated", False),
    }

    # Step 4: Analyze results and generate AI insights
    insight_result = generate_insights(
        question,
        query_result,
    )

    # Step 5: Return the query results and insights
    response = {
        "success": True,
        "question": question,
        "query": query,
        "columns": result["columns"],
        "rows": result["rows"],
        "row_count": result["row_count"],
        "truncated": result.get("truncated", False),
        "insight_success": insight_result.get("success", False),
    }

    if insight_result.get("success"):
        response["analysis"] = insight_result["analysis"]
        response["insights"] = insight_result["insights"]
    else:
        response["insight_error"] = insight_result.get(
            "error", "Insight generation failed."
        )
    # Generate a chart from the actual SQL query results 
    chart = create_chart(query_result) 
    if chart is not None: 
        response["chart"] = chart 
        response["chart_available"] = True 
    else: 
        response["chart_available"] = False

    return response


if __name__ == "__main__":
    question = input(
        "Ask a question about your database: "
    )

    result = answer_question(question)

    if result["success"]:
        print("\n--- GENERATED SQL ---")
        print(result["query"])

        print("\n--- QUERY RESULTS ---")
        print("Rows returned:", result["row_count"])

        for row in result["rows"]:
            print(row)

        if result["truncated"]:
            print("\nShowing only the first 500 rows.")

        if result["insight_success"]:
            print("\n--- AI-GENERATED INSIGHTS ---")
            print(result["insights"])

            print("\n--- LOCAL DATA ANALYSIS ---")
            print(result["analysis"]["summary"])
        else:
            print("\nSQL execution succeeded, but insight generation failed.")
            print("Reason:", result.get("insight_error"))

    else:
        print("\nWorkflow failed at:", result["stage"])
        print("Reason:", result["error"])


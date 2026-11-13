
import json
import os

from dotenv import load_dotenv
from google import genai

from agent.result_analyzer import analyze_results


load_dotenv()

MODEL_NAME = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash-lite"
)


def generate_insights(question, query_result):
    """
    Explain query results using Gemini.

    Pandas performs the calculations locally.
    Gemini receives the question and analysis summary,
    not database credentials or raw database rows.
    """

    if not isinstance(question, str) or not question.strip():
        return {
            "success": False,
            "error": "Please provide the original question."
        }

    # Analyze results locally before contacting Gemini.
    analysis = analyze_results(query_result)

    if not analysis["success"]:
        return {
            "success": False,
            "error": analysis["error"]
        }

    # Send only the computed summary and observations.
    # Do not send the raw database rows.
    safe_summary = {
        "summary": analysis["summary"],
        "observations": analysis["observations"],
    }

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return {
            "success": False,
            "error": "GEMINI_API_KEY is missing from .env."
        }

    prompt = f"""
You are a careful data analyst.

USER QUESTION:
{question.strip()}

LOCALLY CALCULATED DATA SUMMARY:
{json.dumps(safe_summary, indent=2, default=str)}

Instructions:
1. Explain only what the supplied summary supports.
2. Clearly distinguish observations from assumptions.
3. Do not invent values, causes, trends, or business facts.
4. If the summary is insufficient to answer the question,
   say what information is missing.
5. Use simple, beginner-friendly language.
6. Provide a short heading, key observations, and a conclusion.
7. Do not generate SQL or request database credentials.
"""

    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )

        insight_text = response.text

        if not insight_text or not insight_text.strip():
            return {
                "success": False,
                "error": "Gemini returned an empty insight."
            }

        return {
            "success": True,
            "question": question,
            "analysis": analysis,
            "insights": insight_text.strip(),
        }

    except Exception as error:
        return {
            "success": False,
            "error": (
                f"{type(error).__name__}: {error}"
            )
        }


if __name__ == "__main__":
    # Sample results only. This test does not access MySQL.
    sample_question = "Summarize the prices of these products."

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

    result = generate_insights(
        sample_question,
        sample_result,
    )

    print("\n--- GEMINI DATA INSIGHTS ---")

    if result["success"]:
        print(result["insights"])
    else:
        print("Error:", result["error"])
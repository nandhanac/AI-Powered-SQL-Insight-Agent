
import json
import os
import re

from dotenv import load_dotenv
from google import genai

from database.schema_reader import get_database_schema
from tools.database_tools import validate_sql


load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# Keep the model configurable in .env.
MODEL_NAME = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.5-flash-lite"
)


def create_sql_generator_client():
    """Create the Gemini client using the API key in .env."""
    if not API_KEY:
        raise ValueError(
            "GEMINI_API_KEY is missing. "
            "Add it to your .env file."
        )

    return genai.Client(api_key=API_KEY)


def clean_sql_response(response_text):
    """Remove optional Markdown fences from Gemini's response."""
    if not response_text:
        raise ValueError("Gemini returned an empty response.")

    query = response_text.strip()

    # Remove a Markdown code fence if the model adds one.
    query = re.sub(
        r"\A```(?:sql)?\s*",
        "",
        query,
        flags=re.IGNORECASE
    )
    query = re.sub(r"\s*```\Z", "", query)

    return query.strip()


def generate_sql(question):
    """
    Generate one SQL query from a natural-language question.

    This function does not execute the generated query.
    """
    if not isinstance(question, str) or not question.strip():
        return {
            "success": False,
            "error": "Please enter a question."
        }

    try:
        # Read the existing database schema.
        schema = get_database_schema()

        schema_text = json.dumps(
            schema,
            indent=2,
            default=str
        )

        prompt = f"""
You are a SQL query generator for a MySQL database.

DATABASE SCHEMA:
{schema_text}

USER QUESTION:
{question.strip()}

RULES:
1. Generate exactly one read-only SELECT query.
2. Use only tables and columns present in the schema.
3. Do not generate INSERT, UPDATE, DELETE, DROP, ALTER,
   CREATE, TRUNCATE, or other data-changing statements.
4. Do not generate multiple SQL statements.
5. Do not use SELECT INTO or write files.
6. Use MySQL-compatible SQL.
7. Add a reasonable LIMIT when returning detail rows
   without an explicitly requested row count.
8. Return only the SQL query, without explanations
   or Markdown code fences.
"""

        client = create_sql_generator_client()

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        query = clean_sql_response(response.text)

        # Validate the SQL before returning it.
        is_valid, message = validate_sql(query)

        if not is_valid:
            return {
                "success": False,
                "error": "Generated SQL rejected by validator: "
                         + message,
                "query": query
            }

        return {
            "success": True,
            "query": query,
            "message": "SQL generated and passed validation."
        }

    except Exception as error:
        return {
            "success": False,
            "error": (
                f"{type(error).__name__}: {error}"
            )
        }


if __name__ == "__main__":
    question = input(
        "Enter your question about the database: "
    )

    result = generate_sql(question)

    print("\n--- SQL GENERATOR RESULT ---")

    if result["success"]:
        print("Generated SQL:")
        print(result["query"])
        print("\n", result["message"])
        print("The query has NOT been executed.")
    else:
        print("Error:", result["error"])
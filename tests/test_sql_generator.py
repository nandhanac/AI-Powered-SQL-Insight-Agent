
from unittest.mock import patch

from agent.sql_generator import generate_sql


def test_valid_query():
    """A valid SELECT query should pass validation."""
    fake_response = type(
        "FakeResponse",
        (),
        {
            "text": (
                "SELECT product_name, price "
                "FROM products ORDER BY price DESC LIMIT 5"
            )
        },
    )()

    with patch(
        "agent.sql_generator.get_database_schema",
        return_value={"products": ["product_name", "price"]},
    ), patch(
        "agent.sql_generator.create_sql_generator_client"
    ) as mock_client_factory:

        mock_client = mock_client_factory.return_value
        mock_client.models.generate_content.return_value = fake_response

        result = generate_sql(
            "Show me the five most expensive products."
        )

    assert result["success"] is True
    assert "SELECT" in result["query"].upper()
    print("PASS: Valid SELECT query")


def test_empty_question():
    """An empty question should be rejected."""
    result = generate_sql("")

    assert result["success"] is False
    assert result["error"] == "Please enter a question."
    print("PASS: Empty question rejected")


def test_unsafe_generated_query():
    """A generated DELETE query should be rejected."""
    fake_response = type(
        "FakeResponse",
        (),
        {"text": "DELETE FROM products"},
    )()

    with patch(
        "agent.sql_generator.get_database_schema",
        return_value={"products": ["product_name", "price"]},
    ), patch(
        "agent.sql_generator.create_sql_generator_client"
    ) as mock_client_factory:

        mock_client = mock_client_factory.return_value
        mock_client.models.generate_content.return_value = fake_response

        result = generate_sql("Delete all products")

    assert result["success"] is False
    assert "rejected by validator" in result["error"].lower()
    print("PASS: Unsafe generated query rejected")


def main():
    test_valid_query()
    test_empty_question()
    test_unsafe_generated_query()
    print("\nAll SQL generator tests passed.")


if __name__ == "__main__":
    main()
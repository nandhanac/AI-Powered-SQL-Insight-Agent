
from sqlalchemy import inspect, text
from sqlglot import parse
from sqlglot.errors import ParseError

from database.connection import engine
from database.schema_reader import get_database_schema


def get_schema():
    """Return the schema of the complete database."""
    return get_database_schema()


def get_table_schema(table_name):
    """Return columns and keys for one table."""
    inspector = inspect(engine)
    available_tables = inspector.get_table_names()

    if table_name not in available_tables:
        return {
            "error": f"Table '{table_name}' does not exist.",
            "available_tables": available_tables,
        }

    return {
        table_name: {
            "columns": [
                {
                    "name": column["name"],
                    "type": str(column["type"]),
                    "nullable": column["nullable"],
                }
                for column in inspector.get_columns(table_name)
            ],
            "primary_key": inspector.get_pk_constraint(
                table_name
            ).get("constrained_columns", []),
            "foreign_keys": inspector.get_foreign_keys(table_name),
        }
    }



def validate_sql(query):
    """Allow one SELECT query and reject prohibited SQL operations."""
    from sqlglot import exp, parse
    from sqlglot.errors import ParseError

    if not isinstance(query, str) or not query.strip():
        return False, "SQL query cannot be empty."

    try:
        statements = parse(query, read="mysql")
    except ParseError:
        return False, "Invalid SQL syntax."
    except Exception:
        return False, "SQL could not be parsed safely."

    statements = [statement for statement in statements if statement]

    if len(statements) != 1:
        return False, "Only one SQL statement is allowed."

    statement = statements[0]

    # The top-level statement must be a SELECT.
    if not isinstance(statement, exp.Select):
        return False, "Only SELECT queries are allowed."

    # Reject prohibited operations anywhere in the parsed SQL tree.
    forbidden_operations = {
        "insert",
        "update",
        "delete",
        "create",
        "drop",
        "alter",
        "truncate",
        "command",
        "into",
        "merge",
        "copy",
        "grant",
        "revoke",
        "transaction",
        "use",
        "set",
        "execute",
        "call",
        "load",
    }

    for node in statement.walk():
        if node.key.lower() in forbidden_operations:
            return False, (
                "Query contains a prohibited SQL operation."
            )

    return True, "Query validated."

def execute_sql(query):
    """Validate and execute one read-only SQL query."""

    is_valid, message = validate_sql(query)

    if not is_valid:
        return {"error": message}

    try:
        with engine.connect() as connection:
            result = connection.execute(text(query))

            columns = list(result.keys())
            rows = [
                dict(row._mapping)
                for row in result.fetchmany(500)
            ]

            return {
                "columns": columns,
                "rows": rows,
                "row_count": len(rows),
                "truncated": len(rows) == 500,
            }

    except Exception as error:
        return {"error": str(error)}


if __name__ == "__main__":
    test_queries = [
        "SELECT * FROM products LIMIT 5",
        "DELETE FROM products",
        "DROP TABLE products",
        "SELECT 1; SELECT 2",
    ]

    for query in test_queries:
        print(f"\nQuery: {query}")
        print("Validation:", validate_sql(query))
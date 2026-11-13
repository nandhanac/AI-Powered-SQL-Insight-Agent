
from sqlalchemy import inspect

from database.connection import engine


def get_database_schema():
    """Read tables, columns, primary keys, and foreign keys."""

    inspector = inspect(engine)
    schema = {}

    # Get all table names
    table_names = inspector.get_table_names()

    for table_name in table_names:
        # Get column information
        columns = inspector.get_columns(table_name)

        # Get primary key information
        primary_key = inspector.get_pk_constraint(table_name)

        # Get foreign key information
        foreign_keys = inspector.get_foreign_keys(table_name)

        schema[table_name] = {
            "columns": [
                {
                    "name": column["name"],
                    "type": str(column["type"]),
                    "nullable": column["nullable"],
                }
                for column in columns
            ],
            "primary_key": primary_key.get("constrained_columns", []),
            "foreign_keys": [
                {
                    "columns": fk["constrained_columns"],
                    "references_table": fk["referred_table"],
                    "references_columns": fk["referred_columns"],
                }
                for fk in foreign_keys
            ],
        }

    return schema


if __name__ == "__main__":
    database_schema = get_database_schema()

    for table_name, details in database_schema.items():
        print(f"\nTable: {table_name}")

        print("Columns:")
        for column in details["columns"]:
            print(
                f"  - {column['name']} "
                f"({column['type']}, nullable={column['nullable']})"
            )

        print("Primary Key:", details["primary_key"])
        print("Foreign Keys:", details["foreign_keys"])
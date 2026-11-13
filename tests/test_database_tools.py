
from tools.database_tools import validate_sql, execute_sql


def main():
    test_queries = [
        ("SELECT * FROM products LIMIT 5", True),
        ("SELECT COUNT(*) FROM customers", True),
        ("DELETE FROM products", False),
        ("UPDATE products SET price = 0", False),
        ("DROP TABLE products", False),
        ("ALTER TABLE products ADD COLUMN test_col INT", False),
        ("TRUNCATE TABLE products", False),
        ("SELECT 1; SELECT 2", False),
    ]

    for query, expected in test_queries:
        valid, message = validate_sql(query)
        passed = valid == expected

        print(f"\nQuery: {query}")
        print(f"Expected valid: {expected}")
        print(f"Actual valid: {valid}")
        print(f"Result: {'PASS' if passed else 'FAIL'}")
        print(f"Message: {message}")

    print("\nTesting query execution:")
    print(execute_sql("SELECT product_name, price FROM products LIMIT 3"))


if __name__ == "__main__":
    main()
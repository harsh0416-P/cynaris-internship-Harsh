
TRAINING_DATA = [
    {
        "question": "Show all sales records",
        "sql": "SELECT * FROM sales;"
    },
    {
        "question": "Calculate total sales revenue",
        "sql": "SELECT SUM(amount) AS total_revenue FROM sales;"
    },
    {
        "question": "Show total sales revenue by city",
        "sql": """
            SELECT city, SUM(amount) AS total_revenue
            FROM sales
            GROUP BY city
            ORDER BY total_revenue DESC;
        """
    },
    {
        "question": "Find the top five products by revenue",
        "sql": """
            SELECT product, SUM(amount) AS total_revenue
            FROM sales
            GROUP BY product
            ORDER BY total_revenue DESC
            LIMIT 5;
        """
    },
    {
        "question": "Show customers who spent more than 30000",
        "sql": """
            SELECT customer_name, SUM(amount) AS total_spent
            FROM sales
            GROUP BY customer_name
            HAVING SUM(amount) > 30000;
        """
    }
]

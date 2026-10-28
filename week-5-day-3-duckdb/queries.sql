-- Total Sales
SELECT SUM(amount) AS total_sales
        FROM sales;

-- Sales by City
SELECT city, SUM(amount) AS revenue
        FROM sales
        GROUP BY city
        ORDER BY revenue DESC, city;

-- Sales by Category
SELECT category, SUM(amount) AS revenue
        FROM sales
        GROUP BY category
        ORDER BY revenue DESC, category;

-- High Value Sales
SELECT COUNT(*) AS sale_count
        FROM sales
        WHERE amount >= 30000;

-- Top Products
SELECT product, SUM(quantity) AS units_sold
        FROM sales
        GROUP BY product
        ORDER BY units_sold DESC, product;


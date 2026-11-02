-- W6D3: Cynaris Sales Analytics Dashboard

-- 1. Revenue by City (Bar Chart)
SELECT city, SUM(amount) AS total_revenue
FROM sales
GROUP BY city
ORDER BY total_revenue DESC;

-- 2. Revenue by Sale ID (Line Chart)
SELECT sale_id, SUM(amount) AS revenue
FROM sales
GROUP BY sale_id
ORDER BY sale_id;

-- 3. Revenue by Category (Pie Chart)
SELECT category, SUM(amount) AS total_revenue
FROM sales
GROUP BY category;

-- 4. Total Revenue (Big Number)
SELECT SUM(amount) AS total_revenue
FROM sales;

-- 5. Sales Details (Table)
SELECT sale_id, customer_name, product, category,
       amount, city, quantity
FROM sales
ORDER BY sale_id;

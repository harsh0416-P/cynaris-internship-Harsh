-- Cynaris Internship - Week 1 Day 1
-- SQL Fundamentals: SELECT, FROM, WHERE
-- Practice database with fictional sales data

CREATE DATABASE IF NOT EXISTS cynaris_day1;
USE cynaris_day1;

-- Create the sales table
CREATE TABLE IF NOT EXISTS sales (
    sale_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    category VARCHAR(50),
    product VARCHAR(100),
    amount DECIMAL(10,2),
    city VARCHAR(50),
    quantity INT,
    discount DECIMAL(5,2),
    phone VARCHAR(15)
);

-- Check database and table
SHOW TABLES;
DESCRIBE sales;

-- View all existing sales data
SELECT * FROM sales;

-- Add the practice record used during Day 1
-- Run this INSERT only if sale_id 11 does not already exist.
INSERT INTO sales
(sale_id, customer_name, product, category, amount, city, quantity, discount, phone)
VALUES
(11, 'Harsh Sanchaniya', 'Laptop', 'Electronics', 5500, 'Bangalore', 1, 5, '9876543215');

-- =========================================================
-- 10 SELECT QUERIES - DAY 1
-- =========================================================

-- Query 1: Display all sales records
SELECT *
FROM sales;

-- Query 2: Display selected columns
SELECT customer_name, amount
FROM sales;

-- Query 3: Sales with amount greater than 5000
SELECT *
FROM sales
WHERE amount > 5000;

-- Query 4: Sales above 5000 from Bangalore
SELECT *
FROM sales
WHERE amount > 5000
  AND city = 'Bangalore';

-- Query 5: Sales from Bangalore or Mumbai
SELECT *
FROM sales
WHERE city = 'Bangalore'
   OR city = 'Mumbai';

-- Query 6: Sales that are not Electronics
SELECT *
FROM sales
WHERE NOT category = 'Electronics';

-- Query 7: Customers whose name starts with A
SELECT *
FROM sales
WHERE customer_name LIKE 'A%';

-- Query 8: Sales from selected cities
SELECT *
FROM sales
WHERE city IN ('Bangalore', 'Mumbai', 'Delhi');

-- Query 9: Sales amount between 1000 and 10000
SELECT *
FROM sales
WHERE amount BETWEEN 1000 AND 10000;

-- Query 10: Sales where phone number is missing
SELECT *
FROM sales
WHERE phone IS NULL;

-- Final check
SHOW TABLES;
DESCRIBE sales;

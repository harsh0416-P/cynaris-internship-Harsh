

\# W6D4 — Executive Reporting Testing Report



\*\*Project:\*\* Cynaris Vanna + Superset Executive Reporting  

\*\*Date:\*\* 2 November 2026  

\*\*Database:\*\* sales.db  

\*\*Model:\*\* Ollama llama3.2:1b



\## 1. Test Results



| No. | Test | Expected / SQL Result | Status |

|---|---|---|---|

| 1 | Total sales revenue | ₹289,500 | PASS |

| 2 | Revenue by city | Bengaluru ₹94,000; Mumbai ₹92,500; Chennai ₹73,000; Delhi ₹30,000 | SQL PASS / AI FAIL |

| 3 | Average sale amount | ₹28,950 | SQL PASS / AI FAIL |

| 4 | Quantity by product | Chair 11; Mobile 9; Laptop 5; Desk 3; Table 2 | SQL PASS / AI ORDER FAIL |

| 5 | Revenue by category | Electronics ₹247,000; Furniture ₹42,500 | PASS |

| 6 | Average sales by city | Chennai ₹36,500; Bengaluru ₹31,333.33; Mumbai ₹30,833.33; Delhi ₹15,000 | SQL PASS |

| 7 | Revenue by product | Laptop ₹173,000; Mobile ₹74,000; Chair ₹15,500; Desk ₹15,000; Table ₹12,000 | PASS |

| 8 | Transactions by city | Mumbai 3; Bengaluru 3; Delhi 2; Chennai 2 | SQL PASS |

| 9 | Top 3 customers | Karan ₹60,000; Riya ₹58,000; Rahul ₹55,000 | SQL PASS |

| 10 | Category revenue and quantity | Electronics ₹247,000 / 14; Furniture ₹42,500 / 16 | SQL PASS |



\## 2. Security Testing



| SQL Query | Expected Behavior | Result |

|---|---|---|

| SELECT SUM(amount) FROM sales | Allow | PASS |

| SELECT city FROM sales | Allow | PASS |

| DELETE FROM sales | Block | PASS |

| DROP TABLE sales | Block | PASS |

| SELECT \* FROM sales; DROP TABLE sales | Block | PASS |



Security implementation:

\- Custom SQL validation before execution.

\- SQLite read-only connection using mode=ro.

\- SQLite query\_only enabled.



Note: The SQL validator is a basic filter, not a complete SQL security parser.



\## 3. Issues Identified



1\. AI reported Mumbai revenue as ₹93,500 instead of ₹92,500.

2\. AI reported average sale amount as ₹29,950 instead of ₹28,950.

3\. AI displayed product quantities in the wrong order.

4\. Currency formatting used USD ($) instead of INR (₹).

5\. SQL output was more reliable than the generated natural-language explanation.



\## 4. Conclusion



The Vanna API successfully connected to the SQLite sales database and executed analytical queries.



The custom SafeSqliteRunner successfully blocked tested destructive SQL statements.



However, AI-generated explanations were not consistently accurate. SQL query results should remain the source of truth for executive reporting.



Further improvement is required for numerical verification, currency formatting, and response ordering.

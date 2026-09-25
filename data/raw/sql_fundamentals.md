# SQL Fundamentals

## Basic queries
```sql
SELECT name, email FROM users;
SELECT * FROM users WHERE age > 25;
SELECT DISTINCT country FROM users;
SELECT * FROM users ORDER BY created_at DESC LIMIT 10;
SELECT * FROM users WHERE name LIKE 'A%';           -- starts with A
SELECT * FROM users WHERE age BETWEEN 20 AND 30;
SELECT * FROM users WHERE country IN ('IN', 'US', 'UK');
SELECT * FROM users WHERE deleted_at IS NULL;
```

## Aggregation
```sql
SELECT COUNT(*) FROM users;
SELECT AVG(age), MIN(age), MAX(age) FROM users;
SELECT country, COUNT(*) AS user_count
FROM users
GROUP BY country
HAVING COUNT(*) > 100
ORDER BY user_count DESC;
```
**WHERE vs HAVING**: `WHERE` filters rows before grouping; `HAVING` filters groups
after aggregation. You can't use an aggregate function (like `COUNT(*)`) in `WHERE`.

## Joins
```sql
-- INNER JOIN: only matching rows from both tables
SELECT o.id, u.name
FROM orders o
INNER JOIN users u ON o.user_id = u.id;

-- LEFT JOIN: all rows from the left table, matched rows from the right (NULL if none)
SELECT u.name, o.id
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;

-- Find users with NO orders (a classic use of LEFT JOIN)
SELECT u.name
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE o.id IS NULL;

-- SELF JOIN: joining a table to itself (e.g. employees and their managers)
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;
```

## Subqueries
```sql
SELECT name FROM users
WHERE id IN (SELECT user_id FROM orders WHERE total > 1000);

SELECT name, (SELECT COUNT(*) FROM orders WHERE orders.user_id = users.id) AS order_count
FROM users;
```

## Window functions
```sql
SELECT name, salary,
       ROW_NUMBER() OVER (ORDER BY salary DESC) AS rank_num
FROM employees;

SELECT name, department, salary,
       RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dept_rank
FROM employees;

-- Nth highest salary (classic interview question)
SELECT DISTINCT salary
FROM (
    SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
    FROM employees
) ranked
WHERE rnk = 2;   -- 2nd highest salary
```

## Data modification
```sql
INSERT INTO users (name, email) VALUES ('Richard', 'r@example.com');
UPDATE users SET age = 23 WHERE id = 1;
DELETE FROM users WHERE id = 1;
```

## Key theory
- **Primary key vs unique key**: a primary key uniquely identifies each row and can't
  be NULL; a table can have only one. A unique key also enforces uniqueness but CAN be
  NULL (in most databases) and a table can have multiple unique keys.
- **DELETE vs TRUNCATE vs DROP**: `DELETE` removes rows (can be filtered with WHERE,
  can be rolled back, slower, fires triggers); `TRUNCATE` removes ALL rows instantly
  (can't filter, faster, resets auto-increment, harder to roll back); `DROP` removes
  the entire table structure, not just its data.
- **Normalization**: organizing tables to reduce redundancy. 1NF: atomic values, no
  repeating groups. 2NF: 1NF + no partial dependency on part of a composite key. 3NF:
  2NF + no transitive dependency (non-key columns depend only on the key, not on
  other non-key columns).
- **Index**: a data structure (usually a B-tree) that speeds up lookups on a column at
  the cost of slower writes and extra storage — like a book's index vs reading page by
  page.
- **ACID**: Atomicity (all-or-nothing transactions), Consistency (valid state
  before/after), Isolation (concurrent transactions don't interfere), Durability
  (committed data survives crashes).

## SQL vs NoSQL
SQL databases (PostgreSQL, MySQL) enforce a fixed schema and relationships, strong for
consistency and complex queries/joins. NoSQL databases (MongoDB, DynamoDB) offer
flexible schemas and horizontal scalability, often trading strict consistency for
availability/speed on very large or fast-changing datasets.

## Common errors & fixes
- **"column must appear in the GROUP BY clause"**: every non-aggregated column in
  SELECT must also be in GROUP BY.
- **Slow query on a large table**: check `EXPLAIN ANALYZE <query>` to see if it's doing
  a full table scan — likely missing an index on the filtered/joined column.
- **Duplicate rows after a JOIN**: usually a one-to-many relationship producing a row
  per match — use `DISTINCT`, aggregate, or restructure the query depending on intent.
- **"deadlock detected"**: two transactions are waiting on each other's locks — retry
  logic and consistent lock ordering across the application reduce this.

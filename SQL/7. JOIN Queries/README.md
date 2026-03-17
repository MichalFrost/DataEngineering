## JOIN Queries ##

JOIN queries are used to combine rows from two or more tables based on a related column between them. This allows you to retrieve data from multiple tables in a single query, forming a more comprehensive dataset than you could get from a single table alone. Different types of joins, like INNER, LEFT, RIGHT, and FULL OUTER, determine how rows are included in the result based on whether matching values exist in the related columns.


1. INNER JOIN - combine rows from two or more tables based on a related column. They return only the rows where there is a match in the specified columns of all tables involved in the join. If there's no matching value in the joined columns, that row is excluded from the result set.

2. LEFT JOIN -returns all rows from the left table (the table listed before the LEFT JOIN keyword) and the matching rows from the right table (the table listed after the LEFT JOIN keyword). If there is no match in the right table for a row in the left table, the result will contain NULL values for the columns from the right table. Effectively, it ensures all rows from the left table are included in the result set, regardless of whether there's a corresponding row in the right table.

3. RIGHT JOIN - combines rows from two tables based on a related column. It returns all rows from the right table (the table specified after the RIGHT JOIN keyword), and the matching rows from the left table. If there's no match in the left table for a row in the right table, NULL values are returned for the columns from the left table in the result set.

4. FULL OUTER JOIN - combines the results of both LEFT and RIGHT OUTER JOINs. It returns all rows from both tables, matching records where the join condition is met and including unmatched rows from both tables with NULL values in place of missing data. This join type is useful when you need to see all data from both tables, regardless of whether there are matching rows, and is particularly valuable for identifying missing relationships or performing data reconciliation between two tables.

5. Self Join - is a query in SQL that joins a table to itself. This is useful when you want to compare rows within the same table, often based on a hierarchical relationship or other connection between the data points within that table. Think of it as creating two copies of the same table and then joining them based on a shared column, allowing you to relate data from the same source in a new way.

6. Cross Join -  produces a result set that is the number of rows in the first table multiplied by the number of rows in the second table. If a WHERE clause is used in conjunction with a CROSS JOIN, it functions like an INNER JOIN. However, using an INNER JOIN is generally preferred to using a CROSS JOIN with a WHERE clause for readability and performance reasons. It essentially creates all possible combinations of rows from the tables involved.

## Subqueries ##

Subqueries, also known as nested queries or inner queries, are SQL queries embedded within another query. They can be used in various parts of SQL statements, such as SELECT, FROM, WHERE, and HAVING clauses. Subqueries allow for complex data retrieval and manipulation by breaking down complex queries into more manageable parts. They're particularly useful for creating dynamic criteria, performing calculations, or comparing sets of results.


1. Nested Subqueries - Nested subqueries are queries embedded within another SQL query. Think of it as a query inside a query, where the inner query's result is used by the outer query. This allows you to perform more complex data retrieval and filtering operations by breaking down a larger problem into smaller, more manageable steps. Essentially, the outer query depends on the result returned by the inner query to complete its own operation.

2. Correlated Subqueries - is a subquery that uses values from the outer query in its WHERE clause. The correlated subquery is evaluated once for each row processed by the outer query. It exists because it depends on the outer query and it cannot execute independently of the outer query because the subquery is correlated with the outer query as it uses its column in its WHERE clause.

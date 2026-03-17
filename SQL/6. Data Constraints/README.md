## Daata Constraints ##

Data constraints in SQL are rules applied to columns or tables to enforce data integrity and consistency. They include primary key, foreign key, unique, check, and not null constraints. These constraints define limitations on the data that can be inserted, updated, or deleted in a database, ensuring that the data meets specific criteria and maintains relationships between tables. By implementing data constraints, database designers can prevent invalid data entry, maintain referential integrity, and enforce business rules directly at the database level.


1. Primary Key - is a unique identifier for each record in a database table. It ensures that each row in the table is uniquely identifiable, meaning no two rows can have the same primary key value. A primary key is composed of one or more columns, and it must contain unique values without any NULL entries. The primary key enforces entity integrity by preventing duplicate records and ensuring that each record can be precisely located and referenced, often through foreign key relationships in other tables. Using a primary key is fundamental for establishing relationships between tables and maintaining the integrity of the data model.

2. Foreign Key - is a column or group of columns in one table that refers to the primary key of another table. It establishes a link between two tables, enforcing referential integrity and maintaining relationships between related data. Foreign keys ensure that values in the referencing table correspond to valid values in the referenced table, preventing orphaned records and maintaining data consistency across tables. They are crucial for implementing relational database designs and supporting complex queries that join multiple tables.
 
3. Unique - ensures that all values in a column (or a group of columns) are different. It prevents duplicate entries, maintaining data integrity by enforcing uniqueness for the specified field(s). This is useful for fields like email addresses or usernames, where each record should have a distinct value.

4. NOT NULL - ensures that a column does not accept null values. When a column is defined with this constraint, every row in the table must have a value for that specific column. Attempting to insert or update a row with a null value in a NOT NULL column will result in an error, maintaining data integrity by preventing missing or undefined entries.

5. CHECK - is used to enforce data integrity by specifying a condition that must be true for each row in a table. It allows you to define custom rules or restrictions on the values that can be inserted or updated in one or more columns. CHECK constraints help maintain data quality by preventing invalid or inconsistent data from being added to the database, ensuring that only data meeting specified criteria is accepted.


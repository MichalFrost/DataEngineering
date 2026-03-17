__Data Definition Language (DDL)__

DDL is a subset of SQL used to define and manage the structure of database objects. DDL commands include CREATE, ALTER, DROP, and TRUNCATE, which are used to create, modify, delete, and empty database structures such as tables, indexes, views, and schemas. These commands allow database administrators and developers to define the database schema, set up relationships between tables, and manage the overall structure of the database. DDL statements typically result in immediate changes to the database structure and can affect existing data.


__TRUNCATE TABLE__

Truncate Table is a command in SQL used to remove all rows from a table. It's like resetting the table to its initial, empty state. The table structure itself (columns, data types, constraints) remains intact. TRUNCATE TABLE is generally faster than DELETE because it deallocates the data pages used by the table, rather than individually logging each row deletion.


__ALTER TABLE__

The ALTER TABLE statement in SQL is used to modify the structure of an existing table. This includes adding, dropping, or modifying columns, changing the data type of a column, setting default values, and adding or dropping primary or foreign keys.


__CREATE TABLE__

CREATE TABLE is an SQL statement used to define and create a new table in a database. It specifies the table name, column names, data types, and optional constraints such as primary keys, foreign keys, and default values. This statement establishes the structure of the table, defining how data will be stored and organized within it. CREATE TABLE is a fundamental command in database management, essential for setting up the schema of a database and preparing it to store data.


__DROP TABLE__

The DROP TABLE statement removes a table and its data entirely from a database. It's a permanent operation; once a table is dropped, its structure and all the data it contained are lost unless you have a backup. This command should be used with caution, as it can have significant consequences for your database.

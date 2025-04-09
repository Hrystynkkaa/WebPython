import sqlite3
import psycopg2

# Підключення до SQLite
sqlite_conn = sqlite3.connect('sqlite_database.db')
sqlite_cursor = sqlite_conn.cursor()

# Підключення до PostgreSQL
pg_conn = psycopg2.connect(
    dbname="lab2",
    user="postgres",
    password="Hristina",
    host="localhost",
    port="5432"
)
pg_cursor = pg_conn.cursor()

# Отримуємо всі таблиці з SQLite
sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = sqlite_cursor.fetchall()

# Міграція кожної таблиці
for table in tables:
    table_name = table[0]
    print(f"Міграція таблиці {table_name}...")

    # Отримуємо структуру таблиці
    sqlite_cursor.execute(f"PRAGMA table_info({table_name});")
    columns = sqlite_cursor.fetchall()

    # Створюємо таблицю в PostgreSQL
    column_definitions = []
    for column in columns:
        column_name = column[1]
        column_type = column[2]
        column_definitions.append(f"{column_name} {column_type}")
    create_table_query = f"CREATE TABLE {table_name} ({', '.join(column_definitions)});"
    pg_cursor.execute(create_table_query)

    # Копіюємо дані з SQLite в PostgreSQL
    sqlite_cursor.execute(f"SELECT * FROM {table_name};")
    rows = sqlite_cursor.fetchall()
    for row in rows:
        placeholders = ', '.join(['%s'] * len(row))
        insert_query = f"INSERT INTO {table_name} VALUES ({placeholders});"
        pg_cursor.execute(insert_query, row)

# Застосовуємо зміни
pg_conn.commit()
sqlite_conn.close()
pg_conn.close()

print("Міграція завершена")

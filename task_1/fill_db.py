import os
import psycopg2
from sys import argv


CONNECTION_CONFIG = "dbname=b1_task_1 user=b1 password=12345678 host=127.0.0.1 port=5432"


def create_table(table_name, connection, cursor):
    query = f"""CREATE TABLE {table_name} (
                date CHAR(10),
                en_string CHAR(10),
                ru_string CHAR(10),
                int_number INT,
                float_number DECIMAL(10, 8)
                );"""

    cursor.execute(query)
    connection.commit()


def drop_table(table_name, connection, cursor):
    query = f"DROP TABLE {table_name};"
    cursor.execute(query)
    connection.commit()


def insert_rows_into_table(table_name: str, rows: list, connection, cursor):
    query = f"""INSERT INTO {table_name} VALUES {", ".join(rows)};"""
    cursor.execute(query)
    connection.commit()


def fill_table_from_files(files_dir, table_name, connection, cursor):
    file_names_list = os.listdir(files_dir)
    num_of_files = len(file_names_list)
    for i, file_name in enumerate(file_names_list):
        file_path = os.path.join(files_dir, file_name)
        with open(file_path, "r", encoding="utf-8") as fr:
            print(f"Importing file {file_path}.")
            print(f"Files scanned: {i + 1}\t\tFiles remaining: {num_of_files - i - 1}")
            file_len = sum(1 for _ in fr)
        with open(file_path, "r", encoding="utf-8") as fr:
            rows = []
            counter = 1
            for row in fr:
                row = row.split("||")
                row_str = f"('{row[0]}', '{row[1]}', '{row[2]}', {row[3]}, {row[4].replace(',', '.')})"
                rows.append(row_str)

                if counter % 100000 == 0 and counter >= 100000:
                    insert_rows_into_table(table_name, rows, connection, cursor)
                    print(f"Rows imported: {counter}\t\tRows remaining: {file_len - counter}")
                    rows = []
                counter += 1
            del rows


def fill_db(files_dir, table_name):
    if not os.path.isdir(files_dir) or len(os.listdir(files_dir)) == 0:
        raise FileNotFoundError(f"There is no directory with name {files_dir}.")

    with psycopg2.connect(CONNECTION_CONFIG) as conn:
        with conn.cursor() as crs:
            operation_canceled = False
            try:
                create_table(table_name, conn, crs)
                print(f"Creating new table {table_name}")
            except psycopg2.errors.DuplicateTable:
                crs.execute("ROLLBACK")
                print("Table with this name already exists. You have the following options:")
                print(f"Enter 1 to delete old table and create new one.")
                print(f"Enter 2 to append new file rows from {files_dir}.")
                print(f"Any other key to cancel this operation.")
                choice = input()
                if choice == "1":
                    drop_table(table_name, conn, crs)
                    create_table(table_name, conn, crs)
                    print(f"Creating new table {table_name}")
                elif choice == "2":
                    pass
                else:
                    print("Operation canceled.")
                    operation_canceled = True
            if not operation_canceled:
                fill_table_from_files(files_dir, table_name, conn, crs)


try:
    arg_files_dir = argv[1]
    arg_table_name = argv[2]
except IndexError:
    print("This script requires additional arguments. Default arguments will be used.\n")
    arg_files_dir = "generated_file_unions/"
    arg_table_name = "rand_rows"
print(f"Files directory: {arg_files_dir}\nTable name: {arg_table_name}")

fill_db(arg_files_dir, arg_table_name)
print(f"Table {arg_table_name} filled with data from {arg_files_dir} successfully.")

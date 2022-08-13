import psycopg2


CONNECTION_CONFIG = "dbname=b1_task_1 user=b1 password=12345678 host=127.0.0.1 port=5432"


def execute_procedure(script_path, connection, cursor):
    with open(script_path, "r", encoding="utf-8") as script:
        query = script.read()
        cursor.execute(query)
        result = cursor.fetchall()
        connection.commit()

    return result


with psycopg2.connect(CONNECTION_CONFIG) as conn:
    with conn.cursor() as crs:
        metrics = execute_procedure("procedure_script.sql", conn, crs)

print(f"Sum of all integers: {metrics[0][0]}\nMedian of all floats: {float(metrics[0][1])}")

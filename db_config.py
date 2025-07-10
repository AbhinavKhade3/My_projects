import pyodbc
import pandas as pd
from sqlalchemy import create_engine

# Connection config
DB_CONFIG = {
    "server": "DESKTOP-415OGSA",
    "username": "root@localhost ",
    "password": "abhinav",
    "driver": "{ODBC Driver 17 for SQL Server}",
}


def get_connection(db_name):
    conn_str = (
        f"DRIVER={DB_CONFIG['driver']};"
        f"SERVER={DB_CONFIG['server']};"
        f"DATABASE={db_name};"
        f"UID={DB_CONFIG['username']};"
        f"PWD={DB_CONFIG['password']}"
    )
    return pyodbc.connect(conn_str)


def get_db_schema(db_name):
    conn = get_connection(db_name)
    cursor = conn.cursor()
    schema = ""
    cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        cursor.execute(
            "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = ?", table_name
        )
        columns = cursor.fetchall()
        col_names = ", ".join(col[0] for col in columns)
        schema += f"Table {table_name} with columns: {col_names}\n"

    cursor.close()
    conn.close()
    return schema


def execute_sql(sql: str,db):
    url = f"mssql+pyodbc://root@localhost :abhinav@DESKTOP-415OGSA/{db}?driver=ODBC+Driver+17+for+SQL+Server"
    engine = create_engine(url)
    with engine.connect() as conn:
        return pd.read_sql(sql, conn)

def list_dbs():
    conn = get_connection("master")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sys.databases WHERE database_id > 4")
    databases = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return databases



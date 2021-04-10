import cx_Oracle
import config
import pandas as pd


cx_Oracle.init_oracle_client(lib_dir = "./../instantclient_19_10")


def query(query, colNames):
    # TODO: Include something in config.py that allows the version number to be adjusted here.

    connection = cx_Oracle.connect(
        user = config.username,
        password = config.password,
        dsn = config.dsn,
        encoding = config.encoding)

    cursor = connection.cursor()

    cursor.execute(query)

    data = cursor.fetchall()

    if connection:
        connection.close()

    return pd.DataFrame(data, columns = colNames)
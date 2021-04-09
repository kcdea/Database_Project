import cx_Oracle
import config
import os

# Before this works, you need to unzip instantclient_19_8.zip.

cx_Oracle.init_oracle_client(lib_dir=os.environ.get("HOME")+"/Downloads/instantclient_19_8")

connection = cx_Oracle.connect(
        user = config.username,
        password = config.password,
        dsn = config.dsn,
        encoding = config.encoding)

cursor = connection.cursor()

# Example query
cursor.execute("select * from DMIX.BTC")
for row in cursor:
    print(row)

if connection:
    connection.close()
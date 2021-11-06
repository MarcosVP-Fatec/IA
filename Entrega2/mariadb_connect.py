###############################################
## Author: Marcos Vinicio Pereira - 6º BD
##
## Exemplos em https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/

import mariadb
import sys

# Conectando com o MariaDB
def mariadb_connect():

    try:
        conn = mariadb.connect(
            user="iasys",
            password="123",
            host="127.0.0.1",
            port=3307,
            database="IA"

        )
        # Cursor
        return conn

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

def mariadb_connect_cursor():
    return mariadb_connect().cursor()

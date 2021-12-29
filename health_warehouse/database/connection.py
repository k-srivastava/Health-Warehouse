from typing import TYPE_CHECKING, Any

import mysql.connector
from mysql.connector.connection import MySQLConnection

from . import *

if TYPE_CHECKING:
    from mysql.connector.cursor import MySQLCursor


def connect(host: str = HOST, user: str = USER, password: str = PASSWORD, database: str = DATABASE) -> MySQLConnection:
    """
    Establish a connection with the MySQL database. Used as a wrapper of mysql.connector.connect() to avoid verbose
    function calls everytime a database is to be connected. Functionally similar to the mentioned function.

    :param host: Name of the host of the database; optional, defaults to 'localhost'.
    :type host: str
    :param user: Name of the user of the database; optional, defaults to 'root'.
    :type user: str
    :param password: Password for the database; optional, defaults to the correct password.
    :type password: str
    :param database: Name of the database to which the connection is made; optional, defaults to 'health_warehouse_db'.
    :type database: str
    :return: Database to which the connection has been established.
    :rtype: MySQLConnection
    """
    return mysql.connector.connect(host=host, user=user, password=password, database=database)


def add_to_database(command: str):
    health_warehouse_database = connect()
    cursor: 'MySQLCursor' = health_warehouse_database.cursor()

    cursor.execute(command)

    health_warehouse_database.commit()
    health_warehouse_database.close()


def get_from_database(query: str) -> list[tuple[Any, ...]]:
    health_warehouse_database = connect()
    cursor: 'MySQLCursor' = health_warehouse_database.cursor()

    cursor.execute(query)

    query_result: list[tuple[Any, ...]] = cursor.fetchall()

    health_warehouse_database.close()

    return query_result

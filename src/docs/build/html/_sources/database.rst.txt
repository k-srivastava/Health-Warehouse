Database
========

Connection
----------

.. py:data:: File Description

    File to manage all connections and queries made to the MySQL database.

.. py:function:: database.connect(host: str = HOST, user: str = USER, password: str = PASSWORD, database: str = DATABASE) -> MySQLConnection

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

.. py:function:: database.add_to_database(command: str)

    Run a MySQL command on the database to add new data to it. Commits and closes the database after the operation
    is complete.

    :param command: MySQL command to be run on the database.
    :type command: str

.. py:function:: database.get_from_database(query: str) -> list[tuple[Any, ...]]

    Run a MySQL query on the database and retrieve all results from it. Closes the database after the operation is
    complete.

    :param query: MySQL query to be run on the database.
    :type query: str
    :return: Results of the query from the database. If only one result is retrieved, return type is a singleton list.
    :rtype: list[tuple[Any, ...]]

Models
======

Card Classes
------------

.. py:data:: File Description

    File to create the base information card class.

.. py:class:: card_classes.CardType(Enum)

    Enum specifying whether the card is a text card or data card.

.. py:class:: card_classes.CardQuantityType(Enum)

    Enum specifying whether the quantity the card talks about is "most" or "least". Useful to create custom card
    descriptions easily.

.. py:class:: card_classes.Card

    Base card class for the GUI information card elements.

    .. py:classmethod:: card_classes.Card.display_number(self) -> str

        Property that modifies the cards serial number to have a leading zero if the number is a single digit to make
        it more presentable in a larger font.

        :return: Display number of the card, modified with the required leading zeroes.
        :rtype: str

.. py:class:: card_classes.TextCard(Card):

    Subclass of the Card class that only contains textual information.

    .. py:classmethod:: card_classes.TextCard.__post_init__(self)

        Automatically set the type of the card to a text card after the class is initialised.

    .. py:staticmethod:: card_classes.TextCard.sale_card(serial_number: int, medicine: Medicine | None, sale_type: CardQuantityType) -> TextCard

        Create a new sale related text card using a fixed template to avoid having to write the card information every
        time.

        :param serial_number: Serial number of the card.
        :type serial_number: int
        :param medicine: Medicine which the card is talking about, or None.
        :type medicine: Medicine | None
        :param sale_type: Whether the sale of the medicine was the most or the least out of all.
        :type sale_type: CardQuantityType
        :return: Customised text card about the medicine sale if the medicine is given else, a default blank card.
        :rtype: TextCard

    .. py:staticmethod:: card_classes.TextCard.stock_card(serial_number: int, medicine: Medicine, stock_type: CardQuantityType) -> TextCard

        Create a new stock related text card using a fixed template to avoid having to write the card information every
        time.

        :param serial_number: Serial number of the card.
        :type serial_number: int
        :param medicine: Medicine which the card is talking about.
        :type medicine: Medicine | None
        :param stock_type: Whether the sale of the medicine was the most or the least out of all.
        :type stock_type: CardQuantityType
        :return: Customised text card about the medicine stock.
        :rtype: TextCard

.. py:class:: card_classes.DataCard(Card)

    Subclass of the Card class that contains textual and graphical information. The graph is the pie chart.

    .. py:classmethod:: card_classes.DataCard.__post_init__(self)

        Automatically set the type of the card to a data card after the class is initialised.

Cards
-----

.. py:data:: File Description

    File to create and manage all of the information cards for the dashboard and manage all its surrounding data.

Employee
--------

.. py:data:: File Description

    Main employee file. Generate all the database models for the employees in the MySQL database.

.. py:class:: employee.Employee

    Employee dataclass representing a medicine store employee.

    .. py:classmethod:: employee.Employee.__post_init__(self)

        Generate a random unique employee ID and assign the gender to be the first letter, capitalised after the class
        is initialised.

    .. py:classmethod:: employee.Employee.full_name(self) -> str

        Property that sets the full name of the employee as a formatted string to make it more readable when it is
        very long, for instance.

        :return: Full name of the employee, truncated to the first 17 characters.
        :rtype: str

    .. py:classmethod:: employee.Employee.add_to_database(self)

        Add the employee data to the database using a MySQL command.

    .. py:staticmethod:: employee.Employee.get_all() -> list[Employee]

        Get all the employees from the database using a MySQL query.

        :return: List of all the employees in the database.
        :rtype: list[Employee]

    .. py:staticmethod:: employee.Employee.get_all_ids() -> list[int]

        Get all the employee IDs from the database using a MySQL query.

        :return: List of all the employee IDs in the database.
        :rtype: list[int]

    .. py:staticmethod:: employee.Employee.get_by_id(id_: int) -> Employee | None

        Retrieve a specific employee from the database using a MySQL query with the employee's ID as primary key.

        :param id_: Employee ID for the specific employee, primary key.
        :type id_: int
        :return: Employee data if an employee with the given ID exists in the database else None.
        :rtype: Employee | None

    .. py:staticmethod:: employee.Employee.get_by_email_address(email_address: str) -> Employee | None

        Retrieve a specific employee from the database using a MySQL query with the employee's email address which
        should be unique, although, it is not the primary key. Used when authenticating the employee during login.

        :param email_address: Email address of the specific employee.
        :type email_address: str
        :return: Employee data if an employee with the given email address exists in the database else None.
        :rtype: Employee | None

    .. py:staticmethod:: employee.Employee.generate_random_id() -> int

        Generate a new unique random ID for a new employee.

        :return: New random, unique employee ID.
        :rtype: int

    .. py:staticmethod:: employee.Employee.match_password(email_address: str, password: str) -> bool

        Used during login to confirm the employee's email address and password against the database records.

        :param email_address: Email address entered on the login page.
        :type email_address: str
        :param password: Password entered on the login page.
        :type password: str
        :return: True if the email address and password match those on the database else False.
        :rtype: bool

Medicine
--------

.. py:data:: File Description

    Main medicine file. Generate all the database models for the medicines in the MySQL database.

.. py:class:: medicine.Medicine

    Medicine dataclass for the inventory. Dates are stored as strings to be compatible with the MySQL date datatype.

    .. py:classmethod:: medicine.Medicine.__post_init__(self)

        Assign a new unique random ID for the medicine if not provided in the constructor.

    .. py:classmethod:: medicine.Medicine._salts_str(self) -> str

        Convert the list of salts (str) into a single string with comma separated values which is easier to load into
        MySQL.

        :return: All the medicine salts in one comma-separated string.
        :rtype: str

    .. py:classmethod:: medicine.Medicine.add_to_database(self)

        Add the medicine data to the database using a MySQL command.

    .. py:staticmethod:: medicine.Medicine.update_in_database(medicine_id: int, field_name: str, new_value: Any)

        Update a particular piece of medicine data in the database with updated data using a MySQL command.

    .. py:staticmethod:: medicine.Medicine.get_all() -> list[Medicine]

        Get all the medicines from the database using a MySQL query.

        :return: List of all the medicines in the database.
        :rtype: list[Medicine]

    .. py:staticmethod:: medicine.Medicine.get_as_json() -> str

        Get all the medicines from the database using a MySQL query and parse their id, name, manufacturer and stock
        as JSON. Useful to transfer medicine data from Python to JavaScript.

        :return: Medicine data as JSON.
        :rtype: str

    .. py:staticmethod:: medicine.Medicine.get_all_ids() -> list[int]

        Get all the medicine IDs from the database using a MySQL query.

        :return: List of all the medicine IDs in the database.
        :rtype: list[int]

    .. py:staticmethod:: medicine.Medicine.get_by_id(id_: int) -> Medicine | None

        Retrieve a specific medicine from the database using a MySQL query with the medicine's ID as primary key.

        :param id_: Medicine ID for the specific medicine, primary key.
        :type id_: int
        :return: Medicine data if a medicine with the given ID exists in the database else None.
        :rtype: Medicine | None

    .. py:staticmethod:: medicine.Medicine.get_quantities_sorted(reverse: bool = False) -> list[Medicine]

        Retrieve all of the medicines from the database using a MySQL query and sort them on the basis of their
        quantities.

        :param reverse: Reverse the order of the sorting, defaults to False.
        :type reverse: bool
        :return: List of all medicines sorted by their quantities.
        :rtype: list[Medicine]

    .. py:staticmethod:: medicine.Medicine.get_stock_sorted(reverse: bool = False) -> list[Medicine]

        Retrieve all of the medicines from the database using a MySQL query and sort them on the basis of their stocks.

        :param reverse: Reverse the order of the sorting, defaults to False.
        :type reverse: bool
        :return: List of all medicines sorted by their stocks.
        :rtype: list[Medicine]

    .. py:staticmethod:: medicine.Medicine.generate_random_id() -> int

        Generate a new unique random ID for a new medicine.

        :return: New random, unique medicine ID.
        :rtype: int

Sale
----

.. py:data:: File Description

    Main sales file. Generate all the database models for the sales in the MySQL database.

.. py:class:: sale.Sale

    Sale dataclass for the inventory. Dates are stored as strings to be compatible with the MySQL date datatype.

    .. py:classmethod:: sale.Sale.__post_init__(self)

        Assign a new unique random ID for the medicine if not provided in the constructor.

    .. py:classmethod:: sale.Sale.add_to_database(self)

        Add the medicine data to the database using a MySQL command.

    .. py:staticmethod:: sale.Sale.get_all() -> list[Sale]

        Get all the sales from the database using a MySQL query.

        :return: List of all the sales in the database.
        :rtype: list[Sale]

    .. py:staticmethod:: sale.Sale.get_all_ids() -> list[int]

        Get all the sale IDs from the database using a MySQL query.

        :return: List of all the sale IDs in the database.
        :rtype: list[int]

    .. py:staticmethod:: sale.Sale.get_by_id(id_: int) -> Sale | None

        Retrieve a specific sale from the database using a MySQL query with the sale's ID as primary key.

        :param id_: Sale ID for the specific sale, primary key.
        :type id_: int
        :return: Sale data if a sale with the given ID exists in the database else None.
        :rtype: Sale | None

    .. py:staticmethod:: sale.Sale.get_all_this_week() -> list[Sale]

        Retrieve all the sales made in the current week from the database using a MySQL query.

        :return: List of all sales made in the current week.
        :rtype: list[Sale]

    .. py:staticmethod:: sale.Sale.get_all_last_week() -> list[Sale]

        Retrieve all the sales made in the last week from the database using a MySQL query.

        :return: List of all sales made in the last week.
        :rtype: list[Sale]

    .. py:staticmethod:: sale.Sale.get_week_over_week() -> int

        Get the number of sales made this week over the number of sales made last week.

        :return: Number of sales week-over-week.
        :rtype: int

    .. py:staticmethod:: sale.Sale.generate_random_id() -> int

        Generate a new unique random ID for a new sale.

        :return: New random, unique sale ID.
        :rtype: int

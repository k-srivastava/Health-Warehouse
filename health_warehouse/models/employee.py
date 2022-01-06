"""
Main employee file. Generate all the database models for the employees in the MySQL database.
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import date
from typing import Any

import health_warehouse.database.connection


@dataclass
class Employee:
    id: int | None
    first_name: str
    last_name: str
    email_address: str

    age: int
    gender: str
    date_of_joining: date

    designation: str
    monthly_salary: int

    home_address: str
    password: str

    def __post_init__(self):
        """
        Generate a random unique employee ID and assign the gender to be the first letter, capitalised after the class
        is initialised.
        """
        if self.id is None:
            self.id = Employee.generate_random_id()

        self.gender = self.gender[0].title()

    @property
    def full_name(self) -> str:
        """
        Property that sets the full name of the employee as a formatted string to make it more readable when it is
        very long, for instance.

        :return: Full name of the employee, truncated to the first 17 characters.
        :rtype: str
        """
        full_name_ = f'{self.first_name} {self.last_name}'

        return f'{full_name_[:17]}...' if len(full_name_) >= 20 else full_name_

    def add_to_database(self):
        """
        Add the employee data to the database using a MySQL command.
        """
        command = f'''
            INSERT INTO health_warehouse_db.employees
            VALUES ({self.id}, '{self.first_name}', '{self.last_name}', '{self.email_address}', {self.age}, '{self.gender}', '{self.date_of_joining}', '{self.designation}', {self.monthly_salary}, '{self.home_address}', '{self.password}')
        '''

        health_warehouse.database.connection.add_to_database(command)

    @staticmethod
    def get_all() -> list[Employee]:
        """
        Get all the employees from the database using a MySQL query.

        :return: List of all the employees in the database.
        :rtype: list[Employee]
        """
        query = f'''
                SELECT *
                FROM health_warehouse_db.employees
            '''

        all_employees: list[Employee] = []

        query_result: list[tuple[Any, ...]] = health_warehouse.database.connection.get_from_database(query)

        for employee_constructor_args in query_result:
            all_employees.append(Employee(*employee_constructor_args))

        return all_employees

    @staticmethod
    def get_all_ids() -> list[int]:
        """
        Get all the employee IDs from the database using a MySQL query.

        :return: List of all the employee IDs in the database.
        :rtype: list[int]
        """
        query = f'''
                SELECT id
                FROM health_warehouse_db.employees
            '''

        query_result: list[tuple[Any, ...]] = health_warehouse.database.connection.get_from_database(query)

        return [int(id_[0]) for id_ in query_result]

    @staticmethod
    def get_by_id(id_: int) -> Employee | None:
        """
        Retrieve a specific employee from the database using a MySQL query with the employee's ID as primary key.

        :param id_: Employee ID for the specific employee, primary key.
        :type id_: int
        :return: Employee data if an employee with the given ID exists in the database else None.
        :rtype: Employee | None
        """
        query = f'''
                SELECT *
                FROM health_warehouse_db.employees
                WHERE id = {id_}
            '''

        query_result: list[tuple[Any, ...]] = health_warehouse.database.connection.get_from_database(query)

        return Employee(*query_result[0]) if query_result else None

    @staticmethod
    def get_by_email_address(email_address: str) -> Employee | None:
        """
        Retrieve a specific employee from the database using a MySQL query with the employee's email address which
        should be unique, although, it is not the primary key. Used when authenticating the employee during login.

        :param email_address: Email address of the specific employee.
        :type email_address: str
        :return: Employee data if an employee with the given email address exists in the database else None.
        :rtype: Employee | None
        """
        query = f'''
            SELECT *
            FROM health_warehouse_db.employees
            WHERE email_address = '{email_address}'
        '''

        query_result: list[tuple[Any, ...]] = health_warehouse.database.connection.get_from_database(query)

        return Employee(*query_result[0]) if query_result else None

    @staticmethod
    def generate_random_id() -> int:
        """
        Generate a new unique random ID for a new employee.

        :return: New random, unique employee ID.
        :rtype: int
        """
        all_ids = Employee.get_all_ids()

        while True:
            random_id = int(random.random() * 100_000)

            if random_id not in all_ids:
                return random_id

    @staticmethod
    def match_password(email_address: str, password: str) -> bool:
        """
        Used during login to confirm the employee's email address and password against the database records.

        :param email_address: Email address entered on the login page.
        :type email_address: str
        :param password: Password entered on the login page.
        :type password: str
        :return: True if the email address and password match those on the database else False.
        :rtype: bool
        """
        current_employee = Employee.get_by_email_address(email_address)

        if current_employee is None:
            return False

        return password == current_employee.password

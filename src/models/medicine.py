"""
Main medicine file. Generate all the database models for the medicines in the MySQL database.
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import date
from typing import Any

import src.database.connection
from src.models.sale import Sale


@dataclass
class Medicine:
    """
    Medicine dataclass for the inventory. Dates are stored as strings to be compatible with the MySQL date datatype.
    """
    id: int | None
    name: str
    manufacturer: str

    cost_price: int
    sale_price: int

    potency: int
    quantity: int

    manufacturing_date: date
    purchase_date: date
    expiry_date: date

    salts: str
    stock: int = 0

    def __post_init__(self):
        """
        Assign a new unique random ID for the medicine if not provided in the constructor.
        """
        if self.id is None:
            self.id = Medicine.generate_random_id()

    def _salts_str(self) -> str:
        """
        Convert the list of salts (str) into a single string with comma separated values which is easier to load into
        MySQL.

        :return: All the medicine salts in one comma-separated string.
        :rtype: str
        """
        if len(self.salts) == 1:
            return self.salts[0].title()

        salts_as_string = ''

        for idx, salt in enumerate(self.salts):
            if idx != len(self.salts):
                salts_as_string += f'{salt.title()}, '
            else:
                salts_as_string += salt

        return salts_as_string

    def add_to_database(self):
        """
        Add the medicine data to the database using a MySQL command.
        """
        command = f'''
            INSERT INTO health_warehouse_db.medicines
            VALUES (
                {self.id},
                '{self.name}',
                '{self.manufacturer}',
                {self.cost_price},
                {self.sale_price},
                {self.potency},
                {self.quantity},
                '{self.manufacturing_date}',
                '{self.purchase_date}',
                '{self.expiry_date}',
                '{self._salts_str()}',
                {self.stock}
            )
        '''

        src.database.connection.add_to_database(command)

    def drop_from_database(self):
        """
        Remove the sale data from the database using a MySQL command.
        """
        command = f'''
            DELETE
            FROM health_warehouse_db.medicines
            WHERE id = {self.id}
        '''

        sales: list[Sale] = Sale.get_all()

        # Remove all related medicine sales from the database as well.
        for sale in sales:
            if sale.medicine_id == self.id:
                sale.drop_from_database()

        src.database.connection.add_to_database(command)

    def get_salt_alternatives(self) -> list[Medicine]:
        """
        Get all the medicines that can be used as alternatives based on common salts.

        :return: List of all medicines that share at least one common salt.
        :rtype: list[Medicine]
        """
        medicines: list[Medicine] = Medicine.get_all()
        alternatives: list[Medicine] = []

        medicines.remove(self)

        for salt in self.salts.lower().split(', '):
            for medicine in medicines:
                if salt in medicine.salts.lower().split(', '):
                    alternatives.append(medicine)

        return alternatives

    @staticmethod
    def update_in_database(medicine_id: int, field_name: str, new_value: Any):
        """
        Update a particular piece of medicine data in the database with updated data using a MySQL command.
        """
        formatter = "'" if type(new_value) is str else ''

        command = f'''
            UPDATE health_warehouse_db.medicines
            SET
                {field_name} = {formatter}{new_value}{formatter}
            WHERE id = {medicine_id}
        '''

        src.database.connection.add_to_database(command)

    @staticmethod
    def get_all() -> list[Medicine]:
        """
        Get all the medicines from the database using a MySQL query.

        :return: List of all the medicines in the database.
        :rtype: list[Medicine]
        """
        query = f'''
            SELECT *
            FROM health_warehouse_db.medicines
        '''

        all_medicines: list[Medicine] = []

        query_result: list[tuple[Any, ...]] = src.database.connection.get_from_database(query)

        for medicine_constructor_args in query_result:
            all_medicines.append(Medicine(*medicine_constructor_args))

        return all_medicines

    @staticmethod
    def get_as_json() -> str:
        """
        Get all the medicines from the database using a MySQL query and parse their id, name, manufacturer and stock
        as JSON. Useful to transfer medicine data from Python to JavaScript.

        :return: Medicine data as JSON.
        :rtype: str
        """
        medicines = Medicine.get_all()
        json = '['

        for medicine in medicines:
            json += f'{{"id": {medicine.id}, "name": "{medicine.name}", "manufacturer": "{medicine.manufacturer}", ' \
                    f'"stock": {medicine.stock}}},'

        json = json[:-1]  # remove the last trailing comma
        json += ']'

        return json

    @staticmethod
    def get_all_ids() -> list[int]:
        """
        Get all the medicine IDs from the database using a MySQL query.

        :return: List of all the medicine IDs in the database.
        :rtype: list[int]
        """
        query = f'''
            SELECT id
            FROM health_warehouse_db.medicines
        '''

        query_result: list[tuple[Any, ...]] = src.database.connection.get_from_database(query)
        return [id_[0] for id_ in query_result]

    @staticmethod
    def get_by_id(id_: int) -> Medicine | None:
        """
        Retrieve a specific medicine from the database using a MySQL query with the medicine's ID as primary key.

        :param id_: Medicine ID for the specific medicine, primary key.
        :type id_: int
        :return: Medicine data if a medicine with the given ID exists in the database else None.
        :rtype: Medicine | None
        """
        query = f'''
            SELECT *
            FROM health_warehouse_db.medicines
            WHERE id = {id_}
        '''

        query_result: list[tuple[Any, ...]] = src.database.connection.get_from_database(query)
        return Medicine(*query_result[0]) if query_result else None

    @staticmethod
    def get_quantities_sorted(reverse: bool = False) -> list[Medicine]:
        """
        Retrieve all of the medicines from the database using a MySQL query and sort them on the basis of their
        quantities.

        :param reverse: Reverse the order of the sorting, defaults to False.
        :type reverse: bool
        :return: List of all medicines sorted by their quantities.
        :rtype: list[Medicine]
        """
        return list(sorted(Medicine.get_all(), key=lambda medicine: medicine.quantity, reverse=reverse))

    @staticmethod
    def get_stock_sorted(reverse: bool = False) -> list[Medicine]:
        """
        Retrieve all of the medicines from the database using a MySQL query and sort them on the basis of their stocks.

        :param reverse: Reverse the order of the sorting, defaults to False.
        :type reverse: bool
        :return: List of all medicines sorted by their stocks.
        :rtype: list[Medicine]
        """
        return list(sorted(Medicine.get_all(), key=lambda medicine: medicine.stock, reverse=reverse))

    @staticmethod
    def generate_random_id() -> int:
        """
        Generate a new unique random ID for a new medicine.

        :return: New random, unique medicine ID.
        :rtype: int
        """
        all_ids = Medicine.get_all_ids()

        while True:
            random_id = int(random.random() * 100_000)

            if random_id not in all_ids:
                return random_id

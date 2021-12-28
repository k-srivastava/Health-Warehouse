"""
Main products class file. Generate all the database models for the items in the MySQL database.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from datetime import date
from typing import Any

import health_warehouse.database.connection


@dataclass
class Medicine:
    """
    Main medicine class for the inventory. Dates are stored as strings to be compatible with the MySQL date datatype.
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

    salts: list[str] = field(default_factory=list)
    stock: int = 0

    def __post_init__(self):
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
        command = f'''
            INSERT INTO health_warehouse_db.medicines
            VALUES ({self.id}, '{self.name}', '{self.manufacturer}', {self.cost_price}, {self.sale_price}, {self.potency}, {self.quantity}, '{self.manufacturing_date}', '{self.purchase_date}', '{self.expiry_date}', '{self._salts_str()}', {self.stock})
        '''

        health_warehouse.database.connection.add_to_database(command)

    @staticmethod
    def get_all_ids() -> list[int]:
        query = f'''
            SELECT id
            FROM health_warehouse_db.medicines
        '''

        query_result: list[tuple[Any, ...]] = health_warehouse.database.connection.get_from_database(query)

        return [int(id_[0]) for id_ in query_result]

    @staticmethod
    def get_all() -> list[Medicine]:
        query = f'''
            SELECT *
            FROM health_warehouse_db.medicines
        '''
        all_medicines: list[Medicine] = []

        query_result: list[tuple[Any, ...]] = health_warehouse.database.connection.get_from_database(query)

        for medicine_constructor_args in query_result:
            all_medicines.append(Medicine(*medicine_constructor_args))

        return all_medicines

    @staticmethod
    def get_by_id(id_: int) -> Medicine | None:
        query = f'''
            SELECT *
            FROM health_warehouse_db.medicines
            WHERE id = {id_}
        '''

        query_result: list[tuple[Any, ...]] = health_warehouse.database.connection.get_from_database(query)

        return Medicine(*query_result[0]) if query_result else None

    @staticmethod
    def generate_random_id() -> int:
        all_ids = Medicine.get_all_ids()

        while True:
            random_id = int(random.random() * 100_000)

            if random_id not in all_ids:
                return random_id

from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Any

import health_warehouse.database.connection


@dataclass
class Sale:
    id: int | None
    date: date
    medicine_id: int
    quantity: int

    def __post_init__(self):
        if self.id is None:
            self.id = Sale.generate_random_id()

    def add_to_database(self):
        command = f'''
            INSERT INTO health_warehouse_db.sales
            VALUES ({self.id}, '{self.date}', {self.medicine_id}, {self.quantity})
        '''

        health_warehouse.database.connection.add_to_database(command)

    @staticmethod
    def get_all() -> list[Sale]:
        query = f'''
            SELECT *
            FROM health_warehouse_db.sales
        '''

        all_sales: list[Sale] = []

        query_result: list[tuple[Any, ...]] = health_warehouse.database.connection.get_from_database(query)

        for sale_constructor_args in query_result:
            all_sales.append(Sale(*sale_constructor_args))

        return all_sales

    @staticmethod
    def get_all_ids() -> list[int]:
        query = f'''
            SELECT id
            FROM health_warehouse_db.sales
        '''

        query_result: list[tuple[Any, ...]] = health_warehouse.database.connection.get_from_database(query)
        return [id_[0] for id_ in query_result]

    @staticmethod
    def get_by_id(id_: int) -> Sale | None:
        query = f'''
            SELECT *
            FROM health_warehouse_db.sales
            WHERE id = {id_}
        '''

        query_result: list[tuple[Any, ...]] = health_warehouse.database.connection.get_from_database(query)
        return Sale(*query_result[0] if query_result else None)

    @staticmethod
    def get_all_this_week() -> list[Sale]:
        today: date = date.today()
        week_start: date = today - timedelta(today.weekday())

        return [sale for sale in Sale.get_all() if week_start <= sale.date <= today]

    @staticmethod
    def get_all_last_week() -> list[Sale]:
        this_week_start: date = date.today() - timedelta(date.today().weekday())
        previous_week_start: date = this_week_start - timedelta(days=7)
        previous_week_end: date = this_week_start - timedelta(days=1)

        return [sale for sale in Sale.get_all() if previous_week_start <= sale.date <= previous_week_end]

    @staticmethod
    def get_week_over_week() -> int:
        total_sales_this_week: int = sum([sale.quantity for sale in Sale.get_all_this_week()])
        total_sales_last_week: int = sum([sale.quantity for sale in Sale.get_all_last_week()])

        return total_sales_this_week - total_sales_last_week

    @staticmethod
    def generate_random_id() -> int:
        all_ids = Sale.get_all_ids()

        while True:
            random_id = int(random.random() * 100_000)

            if random_id not in all_ids:
                return random_id

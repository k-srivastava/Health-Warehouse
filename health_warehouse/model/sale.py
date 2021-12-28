from dataclasses import dataclass
from datetime import date


@dataclass
class Sale:
    id: int | None
    date: date
    medicine_id: int
    quantity: int

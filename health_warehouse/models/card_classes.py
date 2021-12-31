from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from enum import Enum, auto

from .medicine import Medicine


class CardType(Enum):
    TEXT = auto()
    DATA = auto()


class CardQuantityType(Enum):
    MOST = 'most'
    LEAST = 'least'


@dataclass
class Card:
    type: CardType = field(init=False)
    serial_number: int
    title: str
    hidden_content: str

    @property
    def display_number(self) -> str:
        serial_str = str(self.serial_number)
        return serial_str if len(serial_str) > 1 else f'0{serial_str}'


@dataclass
class TextCard(Card):
    content: str
    summary_title: str

    def __post_init__(self):
        self.type = CardType.TEXT

    @staticmethod
    def sale_card(serial_number: int, medicine: Medicine | None, sale_type: CardQuantityType) -> TextCard:
        if medicine is not None:
            return TextCard(
                serial_number,
                title=f'{sale_type.value.title()} Sold',

                content=f'The {sale_type.value} sold medicine yesterday ({date.today() - timedelta(days=1)}) was '
                        f'{medicine.name} by {medicine.manufacturer}.',

                hidden_content=f'It sold {medicine.quantity} units for a total price of '
                               f'₹{medicine.sale_price * medicine.quantity} giving a profit of '
                               f'₹{(medicine.sale_price - medicine.cost_price) * medicine.quantity}. Its current stock '
                               f'is {medicine.stock} units.',

                summary_title=f'{medicine.name} {medicine.potency}'
            )

        return TextCard(
            serial_number,
            title=f'{sale_type.value.title()} Sold',
            content='No medicine was sold yesterday.',
            hidden_content='To get information, make a sale.',
            summary_title='No Sale'
        )

    @staticmethod
    def stock_card(serial_number: int, medicine: Medicine, stock_type: CardQuantityType) -> TextCard:
        least_stock = stock_type == CardQuantityType.LEAST

        return TextCard(
            serial_number,
            title=f'{stock_type.value.title()} Stock',

            content=f'Stocks of the medicine {medicine.name} by {medicine.manufacturer} are the '
                    f'{"lowest" if least_stock else "highest"} in the warehouse.',

            hidden_content=f'Currently, there are {"only" if least_stock else ""} {medicine.stock} units in the '
                           f'warehouse totalling a price of ₹{medicine.sale_price * medicine.stock}.'
                           f'{" Reorder as soon as possible." if least_stock else ""}',

            summary_title=f'{medicine.name} {medicine.potency}'
        )


@dataclass
class DataCard(Card):
    graph_title: str
    graph_percentage: int

    def __post_init__(self):
        self.type = CardType.DATA

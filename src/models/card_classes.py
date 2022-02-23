"""
File to create the base information card class.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from enum import Enum, auto

from .medicine import Medicine


class CardType(Enum):
    """
    Enum specifying whether the card is a text card or data card.
    """
    TEXT = auto()
    DATA = auto()


class CardQuantityType(Enum):
    """
    Enum specifying whether the quantity the card talks about is "most" or "least". Useful to create custom card
    descriptions easily.
    """
    MOST = 'most'
    LEAST = 'least'


@dataclass
class Card:
    """
    Base card class for the GUI information card elements.
    """
    type: CardType = field(init=False)
    serial_number: int
    title: str
    hidden_content: str

    @property
    def display_number(self) -> str:
        """
        Property that modifies the cards serial number to have a leading zero if the number is a single digit to make
        it more presentable in a larger font.

        :return: Display number of the card, modified with the required leading zeroes.
        :rtype: str
        """
        serial_str = str(self.serial_number)
        return serial_str if len(serial_str) > 1 else f'0{serial_str}'


@dataclass
class TextCard(Card):
    """
    Subclass of the Card class that only contains textual information.
    """
    content: str
    summary_title: str

    def __post_init__(self):
        """
        Automatically set the type of the card to a text card after the class is initialised.
        """
        self.type = CardType.TEXT

    @staticmethod
    def sale_card(serial_number: int, medicine: Medicine | None, sale_type: CardQuantityType) -> TextCard:
        """
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
        """
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
        """
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
        """
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
    """
    Subclass of the Card class that contains textual and graphical information. The graph is the pie chart.
    """
    graph_title: str
    graph_percentage: int

    def __post_init__(self):
        """
        Automatically set the type of the card to a data card after the class is initialised.
        """
        self.type = CardType.DATA

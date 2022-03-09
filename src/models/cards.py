"""
File to create and manage all of the information cards for the dashboard and manage all its surrounding data.
"""
import datetime
from collections import defaultdict

from .card_classes import CardQuantityType, TextCard, DataCard
from .medicine import Medicine
from .sale import Sale


def _generate_sale_cards() -> tuple[TextCard, TextCard] | None:
    """
    Private function to generate two sale quantity text cards that show the most and least sold medicines during the
    current week.

    :return: Cards with most and least sold medicine during the current week.
    :rtype: tuple[TextCard, TextCard]
    """
    sales_this_week: list[Sale] = Sale.get_all_this_week()
    medicines_by_sale: defaultdict[int, int] = defaultdict(lambda: 0)

    for sale in sales_this_week:
        medicines_by_sale[sale.medicine_id] += sale.quantity

    # Sort all the medicine IDs by their sale during the current week and save as list of medicines.
    medicines_sorted_by_sale: list[Medicine] = [
        Medicine.get_by_id(key) for key, _ in sorted(medicines_by_sale.items(), key=lambda item: item[1])
    ]

    if not sales_this_week:
        return None

    return (
        TextCard.sale_card(1, medicines_sorted_by_sale[0], CardQuantityType.LEAST),
        TextCard.sale_card(4, medicines_sorted_by_sale[-1], CardQuantityType.MOST)
    )


def _generate_stock_card() -> tuple[TextCard, TextCard]:
    """
    Private function to generate two current stock text cards that show the most and least stocked medicines.

    :return: Cards with the most and last stocked medicines.
    :rtype: tuple[TextCard, TextCard]
    """
    stocks: list[Medicine] = Medicine.get_stock_sorted()

    return (
        TextCard.stock_card(5, stocks[0], CardQuantityType.LEAST),
        TextCard.stock_card(6, stocks[-1], CardQuantityType.MOST)
    )


def _generate_expired_card() -> TextCard | None:
    medicines = Medicine.get_all()
    expired_medicines = [medicine for medicine in medicines if medicine.expiry_date < datetime.date.today()]

    if not expired_medicines:
        return None

    total_cost = sum(medicine.sale_price * medicine.stock for medicine in expired_medicines)
    num_expired = len(expired_medicines)

    return TextCard(
        7, 'Expired Medicines',
        f'There are expired medicines in the warehouse! The total value of these medicines is ₹{total_cost}. '
        f'Gid rid of and replace these immediately.',
        f'{num_expired} medicine{"s" if num_expired > 1 else ""} {"have" if num_expired > 1 else "has"} expired in the '
        f'warehouse. Urgent attention required.',
        f'{num_expired} Expired'
    )


def _generate_sales_comparison() -> DataCard:
    """
    Private function to generate a sales comparison data card that compares the number of units sold week over week
    from the current week to the previous week.

    :return: Card with the sales comparison of the current and previous week.
    :rtype: DataCard
    """
    sales_this_week: list[Sale] = Sale.get_all_this_week()
    sales_last_week: list[Sale] = Sale.get_all_last_week()

    serial_number = 2
    title = 'Sales'

    if not sales_this_week and not sales_last_week:
        card = DataCard(serial_number, title, 'No sales made this week or last week.', 'Sales', 0)

    elif sales_this_week and not sales_last_week:
        num_sales_this_week: int = sum(sale.quantity for sale in sales_this_week)

        card = DataCard(
            serial_number, title,
            f'No sales were made last week. But, {num_sales_this_week} units have been sold this week.',
            'Sales', 100
        )

    elif not sales_this_week and sales_last_week:
        num_sales_last_week: int = sum(sale.quantity for sale in sales_last_week)

        card = DataCard(
            serial_number, title,
            f'No sales made this week. But, {num_sales_last_week} units were sold last week.',
            'Sales', 0
        )

    else:
        num_sales_this_week: int = sum(sale.quantity for sale in sales_this_week)
        num_sales_last_week: int = sum(sale.quantity for sale in sales_last_week)

        sales_week_over_week: int = abs(num_sales_this_week - num_sales_last_week)
        more_sales_this_week: bool = num_sales_this_week > num_sales_last_week

        if more_sales_this_week:
            sales_percentage = int(sales_week_over_week / num_sales_this_week * 100)
        else:
            sales_percentage = - int(sales_week_over_week / num_sales_last_week * 100)

        card = DataCard(
            serial_number, title,
            f'{num_sales_this_week} units sold this week and {num_sales_last_week} units sold last week. '
            f'{"An increase" if more_sales_this_week else "A decrease"} of {sales_week_over_week} over last week.',
            'Sales WoW', sales_percentage
        )

    return card


def generate_all_text_cards() -> list[TextCard]:
    """
    Generate all of the text cards for the dashboard view.

    :return: All of the text cards.
    :rtype: list[TextCard]
    """
    sale_cards: tuple[TextCard, TextCard] | None = _generate_sale_cards()
    stock_cards: tuple[TextCard, TextCard] = _generate_stock_card()
    expiry_card: TextCard | None = _generate_expired_card()

    text_cards: list[TextCard] = []

    if sale_cards is not None:
        text_cards.extend(sale_cards)

    text_cards.extend(stock_cards)

    if expiry_card is not None:
        text_cards.append(expiry_card)

    return text_cards


def generate_all_data_cards() -> list[DataCard]:
    """
    Generate all of the data cards for the dashboard view.

    :return: All of the data cards.
    :rtype: list[DataCard]
    """
    return [
        _generate_sales_comparison(),

        # Sample data card.
        DataCard(
            3, 'Test Data',
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt.',
            'Graph Title', 75
        )
    ]

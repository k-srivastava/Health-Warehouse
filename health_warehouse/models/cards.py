from datetime import date, timedelta

from .card_classes import CardQuantityType, TextCard, DataCard
from .medicine import Medicine
from .sale import Sale

_today = date.today()
_yesterday = _today - timedelta(days=1)

_medicine_quantities: list[Medicine] = Medicine.get_quantities_sorted()
_medicine_stock: list[Medicine] = Medicine.get_stock_sorted()

_all_sales_this_week: list[Sale] = Sale.get_all_this_week()
_all_sales_last_week: list[Sale] = Sale.get_all_last_week()
_sales_week_over_week: int = Sale.get_week_over_week()

_most_sold_medicine: Medicine | None = _medicine_quantities[-1] if _medicine_quantities else None
_least_sold_medicine: Medicine | None = _medicine_quantities[0] if _medicine_quantities else None

_least_stocked_medicine: Medicine = _medicine_stock[0]
_most_stocked_medicine: Medicine = _medicine_stock[-1]

_num_sales_this_week: int = sum([sale.quantity for sale in _all_sales_this_week])
_num_sales_last_week: int = sum([sale.quantity for sale in _all_sales_last_week])

if _num_sales_last_week == 0 and _num_sales_this_week == 0:
    _sales_percentage_week_over_week_change = 0
    _sales_comparison_card_text1 = f'We sold no medicines this week or the last week.'
    _sales_comparison_card_text2 = '.'

elif _num_sales_last_week == 0:
    _sales_percentage_week_over_week_change = 0
    _sales_comparison_card_text1 = f'We sold {_num_sales_this_week} medicines this week.'
    _sales_comparison_card_text2 = 'We sold no medicines last week.'

elif _num_sales_this_week == 0:
    _sales_percentage_week_over_week_change = 0
    _sales_comparison_card_text1 = f'We sold {_num_sales_last_week} medicines last week.'
    _sales_comparison_card_text2 = 'We sold no medicines this week.'

elif _num_sales_this_week > _num_sales_last_week:
    _sales_percentage_week_over_week_change = round((_num_sales_this_week / _num_sales_last_week) * 100)
    _sales_comparison_card_text1 = f'We sold {_sales_week_over_week} more medicines this week than last week.'
    _sales_comparison_card_text2 = f', an increase of {_sales_percentage_week_over_week_change}% over last week.'

else:
    _sales_percentage_week_over_week_change = round((_num_sales_this_week / _num_sales_last_week) * 100)
    _sales_comparison_card_text1 = f'We sold {-_sales_week_over_week} less medicines this week than last week.'
    _sales_comparison_card_text2 = f', a decrease of {_sales_percentage_week_over_week_change}% over last week.'

_most_sold_card = TextCard.sale_card(1, _most_sold_medicine, CardQuantityType.MOST)
_least_sold_card = TextCard.sale_card(4, _least_sold_medicine, CardQuantityType.LEAST)

_least_stocked_card = TextCard.stock_card(5, _least_stocked_medicine, CardQuantityType.LEAST)
_most_stocked_card = TextCard.stock_card(6, _most_stocked_medicine, CardQuantityType.MOST)

_sales_comparison_card = DataCard(
    3, 'Weekly Sales',
    f'{_sales_comparison_card_text1} We managed to sell {_num_sales_this_week} medicines this week and '
    f'{_num_sales_last_week} medicines last week{_sales_comparison_card_text2}',
    'WoW Increase',
    int(abs(_sales_percentage_week_over_week_change))
)

text_cards: list[TextCard] = [_most_sold_card, _least_sold_card, _least_stocked_card, _most_stocked_card]
data_cards: list[DataCard] = [_sales_comparison_card, _sales_comparison_card]

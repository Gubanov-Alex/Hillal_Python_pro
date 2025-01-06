from typing import Any
from decimal import*


spec_currency = ['usd', 'uah', 'gbp', 'eur']

def currency_converter_chf(value: Decimal, currency: str):
    """Converts currency to intermediate result """

    match currency:
        case 'usd':
            return  value * 2
        case 'uah':
            return value / 2
        case 'gbp':
            return  value * 4
        case 'eur':
            return  value * 3

def currency_converter_spec_currency(value: Decimal, currency: str):
    """Converts currency to actual result"""

    match currency:
        case 'usd':
            return  value / 2
        case 'uah':
            return value * 2
        case 'gbp':
            return  value / 4
        case 'eur':
            return  value / 3

def convert_and_combine(value1: Decimal, currency1: str,
                        value2: Decimal, currency2: str, operation: str) -> Decimal:
    """Make operation to convert currency and combine values"""

    if currency1 not in spec_currency or currency2 not in spec_currency:
        raise ValueError("Can perform operation only for Specific currencies")
    else:
        converted_value1 = currency_converter_chf(Decimal(value1), currency1)
        converted_value2 = currency_converter_chf(Decimal(value2), currency2)

        if operation == "add":
            combined_value = converted_value1 + converted_value2
        elif operation == "sub":
            combined_value = converted_value1 - converted_value2
        else:
            raise ValueError("Unsupported operation")

        result_value = currency_converter_spec_currency(combined_value, currency1)
        return Decimal(result_value)


class Price:
    """
    A class to represent a monetary price with currency.

    Attributes:
    ----------
    value : decimal.Decimal
        The amount of money for the given currency.
    currency : str
        The code of the currency (e.g., 'usd', 'uah') in which the price is specified.

    Methods:
    -------
    __str__() -> str:
        Returns a string representation of the Price object.

    __add__(other: Any) -> "Price":
        Adds the value of this Price object to another Price object if they share the same currency,
        or converts and combines the values of different currencies.

    __sub__(other: Any) -> "Price":
        Subtracts the value of another Price object from this Price object if they share the same currency,
        or converts and calculates the difference of values in different currencies.
    """

    def __init__(self, value: Decimal, currency: str):
        self.value: Decimal = value
        self.currency: str = currency

    def __str__(self) -> str:
        return f"Price: {self.value} {self.currency}"

    def __add__(self, other: Any) -> "Price":
        if not isinstance(other, Price):
            raise ValueError("Can perform operation only with Prices objects")
        elif self.currency == other.currency:
            result_value = self.value + other.value
        else:
            result_value = convert_and_combine(self.value, self.currency, other.value, other.currency, "add")
        return Price(value=result_value, currency=self.currency)

    def __sub__(self, other: Any) -> "Price":
        if not isinstance(other, Price):
            raise ValueError("Can perform operation only with Prices objects")
        elif self.currency == other.currency:
            result_value = self.value - other.value
        else:
            result_value = convert_and_combine(self.value, self.currency, other.value, other.currency, "sub")
        return Price(value=result_value, currency=self.currency)


phone = Price(value=Decimal(1234), currency="uah")
tablet = Price(value=Decimal(786), currency="usd")

total: Price = phone + tablet
print(total)

total: Price = tablet - phone
print(total)
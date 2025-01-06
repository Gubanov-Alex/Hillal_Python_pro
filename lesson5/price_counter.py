from typing import Any

class Price:
    def __init__(self, value: int, currency: str):
        self.value: int = value
        self.currency: str = currency

    def __str__(self) -> str:
        return f"Price: {self.value} {self.currency}"

    def __add__(self, other: Any) -> "Price":
        if not isinstance(other, Price):
            raise ValueError("Can perform operation only with Prices objects")
        else:
            if self.currency != other.currency:
                raise ValueError("Can perform operation only for same currencies")

            return Price(value=self.value + other.value, currency=self.currency)

    def __sub__(self, other: Any) -> "Price":
        if not isinstance(other, Price):
            raise ValueError("Can perform operation only with Prices objects")
        else:
            if self.currency != other.currency:
                raise ValueError("Can perform operation only for same currencies")

            return Price(value=self.value - other.value, currency=self.currency)


phone = Price(value=200, currency="usd")
tablet = Price(value=400, currency="usd")

total: Price = phone + tablet
print(total)

total: Price =tablet - phone
print(total)
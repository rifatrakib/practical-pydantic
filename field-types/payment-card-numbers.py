from datetime import date

from pydantic import BaseModel
from pydantic.types import PaymentCardBrand, PaymentCardNumber, constr


class Card(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)
    number: PaymentCardNumber
    exp: date

    @property
    def brand(self) -> PaymentCardBrand:
        return self.number.brand

    @property
    def expired(self) -> bool:
        return self.exp < date.today()


card = Card(
    name="Georg Wilhelm Friedrich Hegel",
    number="4000000000000002",
    exp=date(2023, 9, 30),
)

print(f"{card.number.brand == PaymentCardBrand.visa = }")
print(f'{card.number.bin == "400000" = }')
print(f'{card.number.last4 == "0002" = }')
print(f'{card.number.masked == "400000******0002" = }')

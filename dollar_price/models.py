from dataclasses import dataclass


@dataclass
class Exchange:
    exchange_name: str
    url: str
    buy_price: float
    sell_price: float

    def __repr__(self) -> str:
        return f'({self.exchange_name}, buy: {self.buy_price}, sell: {self.sell_price}, {self.url})'

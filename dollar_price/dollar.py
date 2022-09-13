from dataclasses import dataclass

import requests
from parsel import Selector

URL = 'https://cuantoestaeldolar.pe/'


@dataclass
class Exchange:
    exchange_name: str
    url: str
    buy_price: float
    sell_price: float

    def __repr__(self) -> str:
        return f'({self.exchange_name}, buy: {self.buy_price}, sell: {self.sell_price}, {self.url})'


def get_html() -> str:
    return requests.get(URL).text


class Parser:
    '''Class with all the logic for parsing the html.'''

    def __init__(self, html: str) -> None:
        self.selector = Selector(html)

    def parse(self) -> list[Exchange]:
        '''Parse the html and get a list of Exchanges'''
        exchanges = self.selector.xpath(
            '/html/body/div[3]/section/div[1]/div[3]/div[1]/div/div'
        )
        return [
            Exchange(
                self.get_name(exchange_row),
                self.get_url(exchange_row),
                self.get_buy_price(exchange_row),
                self.get_sell_price(exchange_row),
            )
            for exchange_row in exchanges
            if 'header' not in exchange_row.xpath('./@class').get()
        ]

    @staticmethod
    def get_name(selector: Selector) -> str:
        return selector.xpath('.//h3/a/text()').get()  # type: ignore

    @staticmethod
    def get_url(selector: Selector) -> str:
        url = str(selector.xpath('.//h3/a/@href').get())  # type: ignore
        return ''.join(url.split('?')[:-1])

    @staticmethod
    def get_price(selector: Selector, xpath: str) -> float:
        return float(selector.xpath(xpath).get().strip())  # type: ignore

    def get_buy_price(self, selector: Selector) -> float:
        return self.get_price(selector, './div[1]/div[2]/text()')

    def get_sell_price(self, selector: Selector) -> float:
        return self.get_price(selector, './div[1]/div[3]/text()')


def get_all_exchanges() -> list[Exchange]:
    parser = Parser(get_html())
    return parser.parse()


def main():
    print(get_all_exchanges())


if __name__ == '__main__':
    main()
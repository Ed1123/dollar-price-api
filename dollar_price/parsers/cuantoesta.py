import json

from httpx import AsyncClient
from parsel import Selector

from dollar_price.models import Exchange

URL = 'https://cuantoestaeldolar.pe/'


async def get_html() -> str:
    async with AsyncClient() as client:
        response = await client.get(URL)
        return response.text


class Parser:
    '''Class with all the logic for parsing the html.'''

    def __init__(self, html: str) -> None:
        self.selector = Selector(html)

    def parse(self) -> list[Exchange]:
        '''Parse the html and get a list of Exchanges'''
        exchange_divs = self.selector.css(
            'main > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) >'
            'div:nth-child(1) > div:nth-child(n+3):nth-child(-n+4) >'
            'div:nth-child(2) > div > div'
        )
        exchanges = [
            Exchange(
                exchange_name=self.get_name(exchange_div),
                buy_price=self.get_buy_price(exchange_div),
                sell_price=self.get_sell_price(exchange_div),
                url=self.get_url(exchange_div),
            )
            for exchange_div in exchange_divs
        ]
        return exchanges

    @staticmethod
    def get_name(exchange_selector: Selector) -> str:
        name = exchange_selector.css('img::attr(alt)').get()
        if name is None:
            return ''
        return name

    @staticmethod
    def get_url(exchange_selector: Selector) -> str:
        url = exchange_selector.css('a::attr(href)').get()
        if url is None:
            return ''
        return url.split('?')[0]

    @staticmethod
    def get_buy_price(exchange_selector: Selector) -> float:
        rate = exchange_selector.css('div > p::text').getall()[0]
        if rate is None:
            return 0.0
        return float(rate)

    @staticmethod
    def get_sell_price(exchange_selector: Selector) -> float:
        rate = exchange_selector.css('div > p::text').getall()[2]
        if rate is None:
            return 0.0
        return float(rate)


async def get_cuantoesta_rates() -> list[Exchange]:
    parser = Parser(await get_html())
    return parser.parse()

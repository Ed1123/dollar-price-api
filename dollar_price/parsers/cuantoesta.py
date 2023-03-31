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
        json_text = self.selector.xpath('//*[@id="__NEXT_DATA__"]/text()').get()
        if json_text is None:
            raise Exception('No json found in website.')
        data = json.loads(json_text)
        exchange_houses = data['props']['pageProps']['onlineExchangeHouses']
        return [
            Exchange(
                self.get_name(exchange_house),
                self.get_url(exchange_house),
                self.get_buy_price(exchange_house),
                self.get_sell_price(exchange_house),
            )
            for exchange_house in exchange_houses
        ]

    @staticmethod
    def get_name(exchange_data: dict) -> str:
        return exchange_data['title']

    @staticmethod
    def get_url(exchange_data: dict) -> str:
        url = exchange_data['site']
        return ''.join(url.split('?')[:-1])

    @staticmethod
    def get_buy_price(exchange_data: dict) -> float:
        return float(exchange_data['rates']['buy']['cost'])

    @staticmethod
    def get_sell_price(exchange_data: dict) -> float:
        return float(exchange_data['rates']['sale']['cost'])


async def get_cuantoesta_rates() -> list[Exchange]:
    parser = Parser(await get_html())
    return parser.parse()

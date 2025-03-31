import json

from fastapi.encoders import jsonable_encoder
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
        script_tag = self.selector.css('body > script:nth-child(20)').get()
        if script_tag is None:
            raise Exception('Missing script tag with JSON in the HTML')

        json_text = script_tag.lstrip(
            '<script>self.__next_f.push([1, "d:[\\"$\",\\"$L17\\",null,'
        ).rstrip(']\\n"])</script>')
        json_text = json_text.encode('utf-8').decode(
            'unicode_escape'
        )  # removing escape characters
        data = json.loads(json_text)
        exchange_houses = data['exchangeHouses']
        return [
            Exchange(
                self.get_name(exchange_house),
                self.get_url(exchange_house),
                self.get_buy_price(exchange_house),
                self.get_sell_price(exchange_house),
            )
            for exchange_house in exchange_houses
            if 'cost' in exchange_house['rates']['buy']
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
        rate = exchange_data['rates']['buy']['cost']
        if rate == '':
            return 0.0
        return float(rate)

    @staticmethod
    def get_sell_price(exchange_data: dict) -> float:
        rate = exchange_data['rates']['sale']['cost']
        if rate == '':
            return 0.0
        return float(rate)


async def get_cuantoesta_rates() -> list[Exchange]:
    parser = Parser(await get_html())
    return parser.parse()

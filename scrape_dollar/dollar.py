from dataclasses import dataclass

import requests
from parsel import Selector


@dataclass
class Exchange:
    exchange_name: str
    url: str
    buy_price: float
    sell_price: float


def get_html() -> str:
    url = 'https://cuantoestaeldolar.pe/'
    return requests.get(url).text


def parse(html: str) -> list[Exchange]:
    '''Parse the html and get a list of Exchanges'''
    exchanges = Selector(html).xpath(
        '/html/body/div[3]/section/div[1]/div[3]/div[1]/div/div'
    )
    return [
        Exchange(
            box.xpath('.//h3/a/text()').get(),
            box.xpath('.//h3/a/@href').get(),
            box.xpath('./div[1]/div[2]/text()').get().strip(),
            box.xpath('./div[1]/div[3]/text()').get().strip(),
        )
        for box in exchanges
        if 'header' not in box.xpath('./@class').get()
    ]


if __name__ == '__main__':
    print(parse(get_html()))

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


def get_selector(html: str) -> Selector:
    return Selector(html)


def parse(selector: Selector) -> list[Exchange]:
    casas_de_cambio = selector.xpath(
        '/html/body/div[3]/section/div[1]/div[3]/div[1]/div/div'
    )
    for box in casas_de_cambio:
        if 'header' in box.xpath('./@class').get():
            continue
        yield Exchange(
            box.xpath('.//h3/a/text()').get(),
            box.xpath('.//h3/a/@href').get(),
            box.xpath('./div[1]/div[2]/text()').get().strip(),
            box.xpath('./div[1]/div[3]/text()').get().strip(),
        )


if __name__ == '__main__':
    print(get_html())

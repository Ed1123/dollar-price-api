import asyncio

from dollar_price.models import Exchange
from dollar_price.parsers.cuantoesta import get_cuantoesta_rates
from dollar_price.parsers.kambista import get_kambista_rate


async def get_all_exchanges() -> list[Exchange]:
    r = await asyncio.gather(get_cuantoesta_rates(), get_kambista_rate())
    rates = []
    for element in r:
        if isinstance(element, Exchange):
            rates.append(element)
        elif isinstance(element, list):
            rates.extend(element)
    return rates


async def main():
    print(await get_all_exchanges())

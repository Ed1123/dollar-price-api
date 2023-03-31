import asyncio

from httpx import AsyncClient

from dollar_price.models import Exchange


async def get_kambista_rate() -> Exchange:
    async with AsyncClient() as client:
        response = await client.get(
            'https://api.kambista.com/v1/exchange/kambista/current'
        )
    data = response.json()
    return Exchange(
        exchange_name='Kambista',
        url='https://kambista.com/',
        buy_price=data['bid'],
        sell_price=data['ask'],
    )


# In case we want to add "paralelo":
# https://us-central1.gcp.data.mongodb-api.com/app/production_realm_app-zusjf/endpoint/banks/tc/paralelo


if __name__ == '__main__':
    print(asyncio.run(get_kambista_rate()))

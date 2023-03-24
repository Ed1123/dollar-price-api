import requests

from dollar_price.models import Exchange


def get_kambista_rate() -> Exchange:
    data = requests.get('https://api.kambista.com/v1/exchange/kambista/current').json()
    return Exchange(
        exchange_name='Kambista',
        url='https://kambista.com/',
        buy_price=data['bid'],
        sell_price=data['ask'],
    )


# In case we want to add "paralelo":
# https://us-central1.gcp.data.mongodb-api.com/app/production_realm_app-zusjf/endpoint/banks/tc/paralelo


if __name__ == '__main__':
    print(get_kambista_rate())

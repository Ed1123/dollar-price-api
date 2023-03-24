from dollar_price.models import Exchange
from dollar_price.parsers.cuantoesta import get_cuantoesta_rates
from dollar_price.parsers.kambista import get_kambista_rate


def get_all_exchanges() -> list[Exchange]:
    rates = get_cuantoesta_rates()
    rates.append(get_kambista_rate())
    return rates


def main():
    print(get_all_exchanges())


if __name__ == '__main__':
    main()

from dollar_price.dollar import Exchange, get_all_exchanges


def test_get_all_exchanges():
    '''Test the main function that gets all the scrape data.'''
    rates = get_all_exchanges()
    assert len(rates) > 0
    assert isinstance(rates[0], Exchange)
    assert rates[0].__dict__['buy_price'] > 0

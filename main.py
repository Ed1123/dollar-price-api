from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from dollar_price.dollar import Exchange, get_all_exchanges

app = FastAPI()


@app.get("/")
async def root():
    return RedirectResponse(url='/docs')


@app.get("/rates", response_model=list[Exchange])
def read_exchange_rates() -> list[Exchange]:
    return get_all_exchanges()

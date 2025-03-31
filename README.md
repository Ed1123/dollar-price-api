# Dollar Price

Dollar Price is a scraper for the USD/PEN exchange pair. It can work as a cli app or as an API with docker.

## Installation
```console
git clone https://github.com/Ed1123/dollar-price.git
cd dollar-price
```
> [!NOTE]  
> Project uses uv for packaging and dependency management.
> Follow installation instructions [here](https://docs.astral.sh/uv/#installation)


## Run API server
```console
uv run uvicorn main:app [--reload]
```
Access rates in: http://127.0.0.1:8000/rates
Access documentation in: http://127.0.0.1:8000/docs

## Run locally
```console
uv run -m dollar_price
```

## Test
```console
uv run pytest
```

# Dollar Price

Dollar Price is a scraper for the USD/PEN exchange pair. It can work as a cli app or as an API with docker.

## Installation
```bash
git clone https://github.com/Ed1123/dollar-price.git
cd dollar-price
pip install -r requirements.txt
```

## Run API server
```bash
uvicorn main:app [--reload]
```
Access rates in: http://127.0.0.1:8000/rates
Access documentation in: http://127.0.0.1:8000/docs

## Run locally
```bash
python3 -m dollar_price
```

## Test
```bash
pytest
```

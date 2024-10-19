AASB: As Above So Below - API Documentation

## Table of Contents

1. [Introduction](#introduction)
2. [External APIs](#external-apis)
    - [1. Forex Data API](#1-forex-data-api)
    - [2. Bond Yields API](#2-bond-yields-api)
    - [3. Climate Data API](#3-climate-data-api)
    - [4. Commodity Prices API](#4-commodity-prices-api)
    - [5. Cultural Trends API](#5-cultural-trends-api)
    - [6. Derivatives Market API](#6-derivatives-market-api)
    - [7. Geopolitical Events API](#7-geopolitical-events-api)
    - [8. Global Consciousness API](#8-global-consciousness-api)
    - [9. Interest Rates API](#9-interest-rates-api)
    - [10. Social Media Sentiment API](#10-social-media-sentiment-api)
    - [11. Stock Indices API](#11-stock-indices-api)
    - [12. Technology Innovations API](#12-technology-innovations-api)
3. [Internal APIs](#internal-apis)
4. [Usage Examples](#usage-examples)
5. [Error Handling](#error-handling)
6. [API Rate Limits](#api-rate-limits)
7. [Security Considerations](#security-considerations)
8. [Conclusion](#conclusion)

---

## Introduction

The **AASB: As Above So Below** project integrates data from various external APIs to model and visualize complex relationships within global financial markets. This document provides detailed information about the APIs used for data collection and any internal APIs exposed by the project. Proper understanding and utilization of these APIs are crucial for maintaining the integrity and functionality of the data pipeline.

---

## External APIs

### 1. Forex Data API

**Provider:** [Open Exchange Rates](https://openexchangerates.org/)

**Description:**  
Provides real-time and historical foreign exchange (forex) rates for global currencies.

**Base URL:**  
```
https://openexchangerates.org/api/
```

**Authentication:**  
API Key passed as a query parameter (`app_id`).

**Endpoints:**

- **Latest Rates**
    - **URL:** `/latest.json`
    - **Method:** `GET`
    - **Parameters:**
        - `app_id` (string, required): Your API key.
        - `symbols` (string, optional): Comma-separated list of currency codes to limit results.
    - **Response Format:** JSON
    - **Example Request:**
        ```
        https://openexchangerates.org/api/latest.json?app_id=YOUR_API_KEY&symbols=USD,EUR,GBP
        ```
    - **Example Response:**
        ```json
        {
            "disclaimer": "Usage subject to terms: https://openexchangerates.org/terms",
            "license": "https://openexchangerates.org/license",
            "timestamp": 1616688000,
            "base": "USD",
            "rates": {
                "USD": 1,
                "EUR": 0.842,
                "GBP": 0.732
            }
        }
        ```

- **Historical Rates**
    - **URL:** `/historical/YYYY-MM-DD.json`
    - **Method:** `GET`
    - **Parameters:**
        - `app_id` (string, required): Your API key.
        - `symbols` (string, optional): Comma-separated list of currency codes to limit results.
    - **Response Format:** JSON
    - **Example Request:**
        ```
        https://openexchangerates.org/api/historical/2021-03-25.json?app_id=YOUR_API_KEY&symbols=USD,EUR,GBP
        ```
    - **Example Response:**
        ```json
        {
            "disclaimer": "Usage subject to terms: https://openexchangerates.org/terms",
            "license": "https://openexchangerates.org/license",
            "timestamp": 1616630400,
            "base": "USD",
            "rates": {
                "USD": 1,
                "EUR": 0.840,
                "GBP": 0.730
            }
        }
        ```

**Usage Example:**

```python
import requests
import os

API_KEY = os.getenv('FOREX_API_KEY')
BASE_URL = 'https://openexchangerates.org/api/'

def get_latest_rates(symbols=None):
    endpoint = 'latest.json'
    params = {'app_id': API_KEY}
    if symbols:
        params['symbols'] = symbols
    response = requests.get(BASE_URL + endpoint, params=params)
    response.raise_for_status()
    return response.json()

# Fetch latest USD, EUR, and GBP rates
rates = get_latest_rates('USD,EUR,GBP')
print(rates)
```

---

### 2. Bond Yields API

**Provider:** [U.S. Department of the Treasury](https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yield)

**Description:**  
Provides daily Treasury Yield Curve Rates for various maturities.

**Base URL:**  
```
https://home.treasury.gov/resource-center/data-chart-center/interest-rates/
```

**Authentication:**  
No authentication required for accessing publicly available data.

**Endpoints:**

- **Daily Treasury Yield Curve Rates**
    - **URL:** `/data/interest-rates/daily-treasury-yield-curve-rates.htm`
    - **Method:** `GET`
    - **Parameters:**  
        - Access via CSV or Excel download links.
    - **Response Format:** CSV or Excel
    - **Example Request:**
        ```
        https://home.treasury.gov/sites/default/files/interest-rates/yield.xml
        ```
    - **Example Response:**  
        A downloadable CSV file containing yield rates for different maturities.

**Usage Example:**

```python
import pandas as pd

def fetch_bond_yields():
    url = 'https://home.treasury.gov/sites/default/files/interest-rates/yield.xml'
    yield_data = pd.read_xml(url)
    return yield_data

bond_yields = fetch_bond_yields()
print(bond_yields.head())
```

**Note:**  
Since the U.S. Department of the Treasury provides data in XML or Excel formats, `pandas` can be used to parse these formats directly.

---

### 3. Climate Data API

**Provider:** [OpenWeatherMap](https://openweathermap.org/api)

**Description:**  
Offers current weather data, forecasts, and historical data for any location worldwide.

**Base URL:**  
```
https://api.openweathermap.org/data/2.5/
```

**Authentication:**  
API Key passed as a query parameter (`appid`).

**Endpoints:**

- **Current Weather Data**
    - **URL:** `weather`
    - **Method:** `GET`
    - **Parameters:**
        - `q` (string, required): City name.
        - `appid` (string, required): Your API key.
        - `units` (string, optional): Units of measurement (`metric`, `imperial`).
    - **Response Format:** JSON
    - **Example Request:**
        ```
        https://api.openweathermap.org/data/2.5/weather?q=London&appid=YOUR_API_KEY&units=metric
        ```
    - **Example Response:**
        ```json
        {
            "weather": [{"description": "light rain", "icon": "10d"}],
            "main": {"temp": 15.0, "humidity": 82},
            "name": "London",
            ...
        }
        ```

- **Historical Weather Data**
    - **URL:** `onecall/timemachine`
    - **Method:** `GET`
    - **Parameters:**
        - `lat` (float, required): Latitude.
        - `lon` (float, required): Longitude.
        - `dt` (int, required): Unix timestamp for the desired date.
        - `appid` (string, required): Your API key.
    - **Response Format:** JSON
    - **Example Request:**
        ```
        https://api.openweathermap.org/data/2.5/onecall/timemachine?lat=51.5074&lon=-0.1278&dt=1616688000&appid=YOUR_API_KEY
        ```
    - **Example Response:**
        ```json
        {
            "current": {
                "temp": 14.0,
                "humidity": 80,
                ...
            },
            ...
        }
        ```

**Usage Example:**

```python
import requests
import os
from datetime import datetime

API_KEY = os.getenv('CLIMATE_API_KEY')
BASE_URL = 'https://api.openweathermap.org/data/2.5/'

def get_current_weather(city):
    endpoint = 'weather'
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(BASE_URL + endpoint, params=params)
    response.raise_for_status()
    return response.json()

def get_historical_weather(lat, lon, date):
    endpoint = 'onecall/timemachine'
    timestamp = int(datetime.strptime(date, '%Y-%m-%d').timestamp())
    params = {
        'lat': lat,
        'lon': lon,
        'dt': timestamp,
        'appid': API_KEY
    }
    response = requests.get(BASE_URL + endpoint, params=params)
    response.raise_for_status()
    return response.json()

# Fetch current weather for London
current_weather = get_current_weather('London')
print(current_weather)

# Fetch historical weather for London on 2021-03-25
historical_weather = get_historical_weather(51.5074, -0.1278, '2021-03-25')
print(historical_weather)
```

---

### 4. Commodity Prices API

**Provider:** [Quandl](https://www.quandl.com/)

**Description:**  
Provides access to a wide range of financial, economic, and alternative datasets, including commodity prices.

**Base URL:**  
```
https://www.quandl.com/api/v3/
```

**Authentication:**  
API Key passed as a query parameter (`api_key`).

**Endpoints:**

- **Commodity Prices Data**
    - **URL:** `datasets/{dataset_code}/data.json`
    - **Method:** `GET`
    - **Parameters:**
        - `api_key` (string, required): Your API key.
        - `start_date` (string, optional): Start date in `YYYY-MM-DD` format.
        - `end_date` (string, optional): End date in `YYYY-MM-DD` format.
        - `order` (string, optional): Order of results (`asc`, `desc`).
    - **Response Format:** JSON
    - **Example Request:**
        ```
        https://www.quandl.com/api/v3/datasets/CHRIS/CME_CL1/data.json?api_key=YOUR_API_KEY&start_date=2021-01-01&end_date=2021-12-31&order=asc
        ```
    - **Example Response:**
        ```json
        {
            "dataset_data": {
                "id": 12345,
                "dataset_code": "CHRIS/CME_CL1",
                "data": [
                    ["2021-01-04", 50.0, 52.0, 49.0, 51.0, 10000],
                    ...
                ],
                ...
            }
        }
        ```

**Usage Example:**

```python
import requests
import os
import pandas as pd

API_KEY = os.getenv('COMMODITY_API_KEY')
BASE_URL = 'https://www.quandl.com/api/v3/'

def get_commodity_prices(dataset_code, start_date=None, end_date=None, order='asc'):
    endpoint = f'datasets/{dataset_code}/data.json'
    params = {
        'api_key': API_KEY,
        'order': order
    }
    if start_date:
        params['start_date'] = start_date
    if end_date:
        params['end_date'] = end_date
    response = requests.get(BASE_URL + endpoint, params=params)
    response.raise_for_status()
    data = response.json()['dataset_data']['data']
    headers = response.json()['dataset_data']['column_names']
    df = pd.DataFrame(data, columns=headers)
    return df

# Fetch crude oil prices from CME
crude_oil_prices = get_commodity_prices('CHRIS/CME_CL1', '2021-01-01', '2021-12-31')
print(crude_oil_prices.head())
```

---

### 5. Cultural Trends API

**Provider:** [Google Trends](https://trends.google.com/trends/api)

**Description:**  
Provides insights into the popularity of search queries across various regions and languages, reflecting cultural and societal interests.

**Base URL:**  
```
https://trends.google.com/trends/api/
```

**Authentication:**  
No official API key; access requires careful handling of API calls, often using libraries like `pytrends`.

**Endpoints:**

- **Trending Searches**
    - **URL:** `trends/api/dailytrends`
    - **Method:** `GET`
    - **Parameters:**
        - `geo` (string, required): Geographical location (e.g., `US`, `GB`).
        - `ns` (int, optional): Namespace parameter.
    - **Response Format:** JSONP (requires parsing)
    - **Example Request:**
        ```
        https://trends.google.com/trends/api/dailytrends?hl=en-US&tz=-480&geo=US&ns=15
        ```
    - **Example Response:**  
        JSONP response that needs to be stripped of leading characters and parsed as JSON.

**Usage Example:**

```python
from pytrends.request import TrendReq

def get_trending_searches(geo='US'):
    pytrends = TrendReq(hl='en-US', tz=360)
    trending_searches = pytrends.trending_searches(pn=geo)
    return trending_searches

# Fetch trending searches for the US
trends_us = get_trending_searches('united_states')
print(trends_us.head())
```

**Note:**  
Use the `pytrends` library to interact with Google Trends API more effectively, as direct API calls require handling JSONP responses.

---

### 6. Derivatives Market API

**Provider:** [CME DataMine](https://www.cmegroup.com/market-data/datamine.html)

**Description:**  
Provides comprehensive data on derivatives markets, including futures and options across various asset classes.

**Base URL:**  
```
https://datamine.cmegroup.com/api/
```

**Authentication:**  
API Key and OAuth 2.0 authentication required.

**Endpoints:**

- **Contract Specifications**
    - **URL:** `/contracts/specifications`
    - **Method:** `GET`
    - **Parameters:**
        - `symbol` (string, required): Contract symbol (e.g., `CL` for crude oil).
        - `exchange` (string, required): Exchange code (e.g., `NYM`).
    - **Response Format:** JSON
    - **Example Request:**
        ```
        https://datamine.cmegroup.com/api/contracts/specifications?symbol=CL&exchange=NYM
        ```
    - **Example Response:**
        ```json
        {
            "contract": {
                "symbol": "CL",
                "exchange": "NYM",
                "description": "Crude Oil Futures"
                ...
            }
        }
        ```

- **Historical Price Data**
    - **URL:** `/data/historical`
    - **Method:** `GET`
    - **Parameters:**
        - `contract_id` (string, required): Unique identifier for the contract.
        - `start_date` (string, required): Start date in `YYYY-MM-DD` format.
        - `end_date` (string, required): End date in `YYYY-MM-DD` format.
        - `frequency` (string, optional): Data frequency (`daily`, `hourly`).
    - **Response Format:** JSON
    - **Example Request:**
        ```
        https://datamine.cmegroup.com/api/data/historical?contract_id=CLG21&start_date=2021-01-01&end_date=2021-12-31&frequency=daily
        ```
    - **Example Response:**
        ```json
        {
            "data": [
                {"date": "2021-01-04", "open": 50.0, "high": 52.0, "low": 49.0, "close": 51.0, "volume": 10000},
                ...
            ]
        }
        ```

**Usage Example:**

```python
import requests
import os

API_KEY = os.getenv('DERIVATIVES_API_KEY')
OAUTH_TOKEN = os.getenv('DERIVATIVES_OAUTH_TOKEN')
BASE_URL = 'https://datamine.cmegroup.com/api/'

def get_contract_specifications(symbol, exchange):
    endpoint = 'contracts/specifications'
    headers = {'Authorization': f'Bearer {OAUTH_TOKEN}'}
    params = {'symbol': symbol, 'exchange': exchange}
    response = requests.get(BASE_URL + endpoint, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def get_historical_prices(contract_id, start_date, end_date, frequency='daily'):
    endpoint = 'data/historical'
    headers = {'Authorization': f'Bearer {OAUTH_TOKEN}'}
    params = {
        'contract_id': contract_id,
        'start_date': start_date,
        'end_date': end_date,
        'frequency': frequency
    }
    response = requests.get(BASE_URL + endpoint, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

# Example Usage
contract_specs = get_contract_specifications('CL', 'NYM')
print(contract_specs)

historical_prices = get_historical_prices('CLG21', '2021-01-01', '2021-12-31')
print(historical_prices)
```

**Note:**  
Access to CME DataMine requires a subscription and adherence to their data usage policies. Ensure compliance with all terms and conditions when utilizing their APIs.

---

### 7. Geopolitical Events API

**Provider:** [GDELT Project](https://www.gdeltproject.org/)

**Description:**  
Monitors and catalogs global geopolitical events, providing real-time data on various socio-political occurrences worldwide.

**Base URL:**  
```
https://api.gdeltproject.org/api/v2/
```

**Authentication:**  
No authentication required for accessing public endpoints.

**Endpoints:**

- **GDELT Events API**
    - **URL:** `gkg/query`
    - **Method:** `GET`
    - **Parameters:**
        - `query` (string, required): Search query string.
        - `mode` (string, optional): Response mode (`artlist`, `artdump`).
        - `maxrecords` (int, optional): Maximum number of records to return.
    - **Response Format:** JSON or TSV
    - **Example Request:**
        ```
        https://api.gdeltproject.org/api/v2/gkg/query?query=climate+change&mode=artlist&maxrecords=100
        ```
    - **Example Response:**
        ```json
        {
            "query": "climate change",
            "records": [
                {
                    "title": "Climate Change Impact on Global Economy",
                    "url": "https://example.com/article1",
                    "date": "2021-03-25",
                    ...
                },
                ...
            ]
        }
        ```

**Usage Example:**

```python
import requests

def fetch_geopolitical_events(query, max_records=100):
    endpoint = 'gkg/query'
    params = {
        'query': query,
        'mode': 'artlist',
        'maxrecords': max_records
    }
    response = requests.get('https://api.gdeltproject.org/api/v2/gkg/query', params=params)
    response.raise_for_status()
    return response.json()

# Fetch geopolitical events related to climate change
events = fetch_geopolitical_events('climate change')
print(events)
```

**Note:**  
GDELT offers extensive data, but users should be mindful of data volume and ensure efficient querying to manage response sizes effectively.

---

### 8. Global Consciousness API

**Provider:** *Custom/Internal Source*

**Description:**  
Tracks and measures global consciousness metrics, such as collective sentiment, awareness levels, and societal engagement indicators. This data is internally generated or sourced from specialized providers.

**Base URL:**  
*Not applicable if data is internally generated.*

**Authentication:**  
*Depends on data source. For internal data, ensure secure access protocols.*

**Endpoints:**

- **Data Access (Internal)**
    - **URL:** `/api/global_consciousness/data`
    - **Method:** `GET`
    - **Parameters:**
        - `date` (string, optional): Specific date for data retrieval.
        - `region` (string, optional): Geographic region filter.
    - **Response Format:** JSON
    - **Example Request:**
        ```
        https://your-internal-domain.com/api/global_consciousness/data?date=2021-03-25&region=global
        ```
    - **Example Response:**
        ```json
        {
            "date": "2021-03-25",
            "region": "global",
            "sentiment_score": 0.75,
            "awareness_level": 0.65,
            ...
        }
        ```

**Usage Example:**

```python
import requests
import os

INTERNAL_API_BASE_URL = os.getenv('INTERNAL_API_BASE_URL')
API_TOKEN = os.getenv('INTERNAL_API_TOKEN')

def get_global_consciousness_data(date=None, region=None):
    endpoint = 'api/global_consciousness/data'
    headers = {'Authorization': f'Bearer {API_TOKEN}'}
    params = {}
    if date:
        params['date'] = date
    if region:
        params['region'] = region
    response = requests.get(f'{INTERNAL_API_BASE_URL}/{endpoint}', headers=headers, params=params)
    response.raise_for_status()
    return response.json()

# Fetch global consciousness data for March 25, 2021
consciousness_data = get_global_consciousness_data('2021-03-25', 'global')
print(consciousness_data)
```

**Note:**  
If the Global Consciousness data is sourced from an external provider, replace the placeholders with actual API details. Ensure that any internal APIs are secured and comply with organizational security policies.

---

### 9. Interest Rates API

**Provider:** [Federal Reserve Economic Data (FRED)](https://fred.stlouisfed.org/docs/api/fred/)

**Description:**  
Provides access to a vast repository of economic data, including various interest rates, maintained by the Federal Reserve Bank of St. Louis.

**Base URL:**  
```
https://api.stlouisfed.org/fred/
```

**Authentication:**  
API Key passed as a query parameter (`api_key`).

**Endpoints:**

- **Release List**
    - **URL:** `release/list`
    - **Method:** `GET`
    - **Parameters:**
        - `api_key` (string, required): Your API key.
        - `file_type` (string, optional): Response format (`json`, `xml`).
    - **Response Format:** JSON or XML
    - **Example Request:**
        ```
        https://api.stlouisfed.org/fred/release/list?api_key=YOUR_API_KEY&file_type=json
        ```
    - **Example Response:**
        ```json
        {
            "releases": [
                {
                    "id": "RELEASE_ID",
                    "name": "Interest Rates Release",
                    "release_date": "2021-03-25",
                    ...
                },
                ...
            ]
        }
        ```

- **Series Data**
    - **URL:** `series/observations`
    - **Method:** `GET`
    - **Parameters:**
        - `series_id` (string, required): Identifier for the interest rate series (e.g., `FEDFUNDS`).
        - `api_key` (string, required): Your API key.
        - `file_type` (string, optional): Response format (`json`, `xml`).
        - `observation_start` (string, optional): Start date in `YYYY-MM-DD` format.
        - `observation_end` (string, optional): End date in `YYYY-MM-DD` format.
    - **Response Format:** JSON or XML
    - **Example Request:**
        ```
        https://api.stlouisfed.org/fred/series/observations?series_id=FEDFUNDS&api_key=YOUR_API_KEY&file_type=json&observation_start=2021-01-01&observation_end=2021-12-31
        ```
    - **Example Response:**
        ```json
        {
            "observations": [
                {"date": "2021-01-01", "value": "0.08"},
                ...
            ]
        }
        ```

**Usage Example:**

```python
import requests
import os
import pandas as pd

API_KEY = os.getenv('INTEREST_RATES_API_KEY')
BASE_URL = 'https://api.stlouisfed.org/fred/'

def get_interest_rate_series(series_id, start_date=None, end_date=None):
    endpoint = 'series/observations'
    params = {
        'series_id': series_id,
        'api_key': API_KEY,
        'file_type': 'json'
    }
    if start_date:
        params['observation_start'] = start_date
    if end_date:
        params['observation_end'] = end_date
    response = requests.get(BASE_URL + endpoint, params=params)
    response.raise_for_status()
    data = response.json()['observations']
    df = pd.DataFrame(data)
    return df

# Fetch Federal Funds Rate for 2021
fed_funds_rate = get_interest_rate_series('FEDFUNDS', '2021-01-01', '2021-12-31')
print(fed_funds_rate.head())
```

---

### 10. Social Media Sentiment API

**Provider:** [Twitter API v2](https://developer.twitter.com/en/docs/twitter-api)

**Description:**  
Provides access to real-time and historical tweets, enabling sentiment analysis and trend monitoring across various topics.

**Base URL:**  
```
https://api.twitter.com/2/
```

**Authentication:**  
Bearer Token passed in the `Authorization` header.

**Endpoints:**

- **Recent Search**
    - **URL:** `tweets/search/recent`
    - **Method:** `GET`
    - **Parameters:**
        - `query` (string, required): Search query string.
        - `max_results` (int, optional): Maximum number of results (default: 10, max: 100).
        - `tweet.fields` (string, optional): Additional fields to return (e.g., `created_at`, `lang`).
    - **Response Format:** JSON
    - **Example Request:**
        ```
        https://api.twitter.com/2/tweets/search/recent?query=climate+change&max_results=50&tweet.fields=created_at,lang
        ```
    - **Example Response:**
        ```json
        {
            "data": [
                {
                    "id": "1234567890",
                    "text": "Climate change is accelerating...",
                    "created_at": "2021-03-25T12:34:56.000Z",
                    "lang": "en"
                },
                ...
            ],
            "meta": {
                "result_count": 50,
                ...
            }
        }
        ```

**Usage Example:**

```python
import requests
import os

BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
BASE_URL = 'https://api.twitter.com/2/'

def create_headers(bearer_token):
    headers = {"Authorization": f"Bearer {bearer_token}"}
    return headers

def get_recent_tweets(query, max_results=50, tweet_fields='created_at,lang'):
    endpoint = 'tweets/search/recent'
    params = {
        'query': query,
        'max_results': max_results,
        'tweet.fields': tweet_fields
    }
    headers = create_headers(BEARER_TOKEN)
    response = requests.get(BASE_URL + endpoint, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

# Fetch recent tweets about climate change
tweets = get_recent_tweets('climate change')
print(tweets)
```

**Note:**  
Access to Twitter API v2 requires applying for a developer account and adhering to their usage policies. Rate limits and access levels depend on the subscription tier.

---

### 11. Stock Indices API

**Provider:** [Alpha Vantage](https://www.alphavantage.co/)

**Description:**  
Provides real-time and historical stock market data, including global indices, individual stocks, and other financial metrics.

**Base URL:**  
```
https://www.alphavantage.co/query
```

**Authentication:**  
API Key passed as a query parameter (`apikey`).

**Endpoints:**

Certainly! Continuing from where you left off, here's the complete `api_documentation.md` for your **AASB: As Above So Below** project. This documentation outlines the APIs integrated into your project, detailing each endpoint, its purpose, required parameters, and example requests and responses.

## Global Quote

- **Description:** Retrieves real-time stock data for a specific symbol.
- **URL:** Same as Base URL
- **Method:** GET

### Parameters:

| Parameter | Type   | Required | Description                                      |
|-----------|--------|----------|--------------------------------------------------|
| function  | string | Yes      | Must be `GLOBAL_QUOTE`                           |
| symbol    | string | Yes      | Stock symbol (e.g., `^GSPC` for S&P 500)         |
| apikey    | string | Yes      | Your API key                                     |

### Response Format:

- **Format:** JSON

### Example Request:

```bash
https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=^GSPC&apikey=YOUR_API_KEY
```

### Example Response:

```json
{
    "Global Quote": {
        "01. symbol": "^GSPC",
        "02. open": "4500.00",
        "03. high": "4550.00",
        "04. low": "4490.00",
        "05. price": "4525.00",
        "06. volume": "3500000",
        "07. latest trading day": "2024-04-25",
        "08. previous close": "4500.00",
        "09. change": "25.00",
        "10. change percent": "0.56%"
    }
}
```

---

## Time Series Daily

- **Description:** Provides daily time series data for a specified stock symbol.
- **URL:** Same as Base URL
- **Method:** GET

### Parameters:

| Parameter | Type   | Required | Description                                      |
|-----------|--------|----------|--------------------------------------------------|
| function  | string | Yes      | Must be `TIME_SERIES_DAILY`                      |
| symbol    | string | Yes      | Stock symbol (e.g., `AAPL` for Apple Inc.)        |
| outputsize| string | No       | `compact` (last 100 data points) or `full`       |
| apikey    | string | Yes      | Your API key                                     |

### Response Format:

- **Format:** JSON

### Example Request:

```bash
https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&outputsize=compact&apikey=YOUR_API_KEY
```

### Example Response:

```json
{
    "Meta Data": {
        "1. Information": "Daily Prices (open, high, low, close) and Volumes",
        "2. Symbol": "AAPL",
        "3. Last Refreshed": "2024-04-25",
        "4. Output Size": "Compact",
        "5. Time Zone": "US/Eastern"
    },
    "Time Series (Daily)": {
        "2024-04-25": {
            "1. open": "130.00",
            "2. high": "132.00",
            "3. low": "129.50",
            "4. close": "131.50",
            "5. volume": "75000000"
        },
        "2024-04-24": {
            "1. open": "128.00",
            "2. high": "130.00",
            "3. low": "127.00",
            "4. close": "129.00",
            "5. volume": "68000000"
        }
        // Additional daily data points...
    }
}
```

---

## Sector Performance

- **Description:** Retrieves real-time sector performance data.
- **URL:** Same as Base URL
- **Method:** GET

### Parameters:

| Parameter | Type   | Required | Description                                      |
|-----------|--------|----------|--------------------------------------------------|
| function  | string | Yes      | Must be `SECTOR`                                  |
| apikey    | string | Yes      | Your API key                                     |

### Response Format:

- **Format:** JSON

### Example Request:

```bash
https://www.alphavantage.co/query?function=SECTOR&apikey=YOUR_API_KEY
```

### Example Response:

```json
{
    "Rank A: Real-Time Performance": {
        "Information Technology": "0.56%",
        "Health Care": "0.45%",
        "Financials": "0.30%",
        "Consumer Discretionary": "0.25%",
        "Industrials": "0.20%",
        "Energy": "0.15%",
        "Utilities": "0.10%",
        "Real Estate": "0.05%",
        "Consumer Staples": "0.00%",
        "Materials": "-0.05%"
    },
    "Rank B: 1 Day Percentage Change": {
        // Similar structure...
    },
    // Additional ranking categories...
}
```

---

## Exchange Rates

- **Description:** Provides real-time exchange rate data between two currencies.
- **URL:** Same as Base URL
- **Method:** GET

### Parameters:

| Parameter | Type   | Required | Description                                      |
|-----------|--------|----------|--------------------------------------------------|
| function  | string | Yes      | Must be `CURRENCY_EXCHANGE_RATE`                  |
| from_currency | string | Yes  | The currency symbol to convert from (e.g., `USD`) |
| to_currency   | string | Yes  | The currency symbol to convert to (e.g., `EUR`)   |
| apikey        | string | Yes  | Your API key                                     |

### Response Format:

- **Format:** JSON

### Example Request:

```bash
https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=EUR&apikey=YOUR_API_KEY
```

### Example Response:

```json
{
    "Realtime Currency Exchange Rate": {
        "1. From_Currency Code": "USD",
        "2. From_Currency Name": "United States Dollar",
        "3. To_Currency Code": "EUR",
        "4. To_Currency Name": "Euro",
        "5. Exchange Rate": "0.9200",
        "6. Last Refreshed": "2024-04-25 20:00:00",
        "7. Time Zone": "UTC",
        "8. Bid Price": "0.9195",
        "9. Ask Price": "0.9205"
    }
}
```

---

## Commodity Prices

- **Description:** Retrieves real-time commodity prices.
- **URL:** Same as Base URL
- **Method:** GET

### Parameters:

| Parameter | Type   | Required | Description                                      |
|-----------|--------|----------|--------------------------------------------------|
| function  | string | Yes      | Must be `COMMODITY_EXCHANGE_RATE`                 |
| symbol    | string | Yes      | Commodity symbol (e.g., `WTICOUSD` for Crude Oil) |
| apikey    | string | Yes      | Your API key                                     |

### Response Format:

- **Format:** JSON

### Example Request:

```bash
https://www.alphavantage.co/query?function=COMMODITY_EXCHANGE_RATE&symbol=WTICOUSD&apikey=YOUR_API_KEY
```

### Example Response:

```json
{
    "Realtime Commodity Exchange Rate": {
        "1. From Commodity": "WTI Crude Oil",
        "2. To Currency": "USD",
        "3. Exchange Rate": "75.25",
        "4. Last Refreshed": "2024-04-25 20:00:00",
        "5. Time Zone": "UTC"
    }
}
```

---

## Interest Rates

- **Description:** Provides current interest rates from various central banks.
- **URL:** Same as Base URL
- **Method:** GET

### Parameters:

| Parameter | Type   | Required | Description                                      |
|-----------|--------|----------|--------------------------------------------------|
| function  | string | Yes      | Must be `INTEREST_RATES`                          |
| apikey    | string | Yes      | Your API key                                     |

### Response Format:

- **Format:** JSON

### Example Request:

```bash
https://www.alphavantage.co/query?function=INTEREST_RATES&apikey=YOUR_API_KEY
```

### Example Response:

```json
{
    "Interest Rates": {
        "Federal Reserve": "5.25%",
        "European Central Bank": "4.00%",
        "Bank of England": "4.10%",
        "Bank of Japan": "0.10%",
        "Reserve Bank of Australia": "3.50%"
    }
}
```

---

## Social Media Sentiment

- **Description:** Analyzes sentiment from social media platforms regarding specific stocks or markets.
- **URL:** Custom Endpoint (Assuming a third-party or custom API)
- **Method:** GET

### Parameters:

| Parameter | Type   | Required | Description                                      |
|-----------|--------|----------|--------------------------------------------------|
| function  | string | Yes      | Must be `SOCIAL_MEDIA_SENTIMENT`                  |
| query     | string | Yes      | The search query or keyword (e.g., `AAPL`)        |
| apikey    | string | Yes      | Your API key                                     |

### Response Format:

- **Format:** JSON

### Example Request:

```bash
https://api.socialmediaanalytics.com/query?function=SOCIAL_MEDIA_SENTIMENT&query=AAPL&apikey=YOUR_API_KEY
```

### Example Response:

```json
{
    "Social Media Sentiment": {
        "positive": 65,
        "neutral": 25,
        "negative": 10,
        "total_mentions": 10000
    }
}
```

---

## Climate Data

- **Description:** Retrieves climate-related data impacting financial markets.
- **URL:** Same as Base URL
- **Method:** GET

### Parameters:

| Parameter    | Type   | Required | Description                                      |
|--------------|--------|----------|--------------------------------------------------|
| function     | string | Yes      | Must be `CLIMATE_DATA`                            |
| location     | string | Yes      | Geographic location (e.g., `Global`, `US`)       |
| data_type    | string | Yes      | Type of climate data (e.g., `Temperature`, `CO2`) |
| apikey       | string | Yes      | Your API key                                     |

### Response Format:

- **Format:** JSON

### Example Request:

```bash
https://www.climatedataapi.com/query?function=CLIMATE_DATA&location=Global&data_type=CO2&apikey=YOUR_API_KEY
```

### Example Response:

```json
{
    "Climate Data": {
        "Location": "Global",
        "Data Type": "CO2",
        "Value": "412.5 ppm",
        "Last Updated": "2024-04-20"
    }
}
```

---

## Geopolitical Events

- **Description:** Provides information on recent geopolitical events that may influence financial markets.
- **URL:** Custom Endpoint (Assuming a third-party or custom API)
- **Method:** GET

### Parameters:

| Parameter | Type   | Required | Description                                      |
|-----------|--------|----------|--------------------------------------------------|
| function  | string | Yes      | Must be `GEOPOLITICAL_EVENTS`                     |
| region    | string | Yes      | Geographic region (e.g., `Middle East`)          |
| apikey    | string | Yes      | Your API key                                     |

### Response Format:

- **Format:** JSON

### Example Request:

```bash
https://api.geopoliticalevents.com/query?function=GEOPOLITICAL_EVENTS&region=Middle%20East&apikey=YOUR_API_KEY
```

### Example Response:

```json
{
    "Geopolitical Events": [
        {
            "event_id": "E12345",
            "title": "Oil Embargo Announcement",
            "description": "Country X imposes an oil embargo affecting global supply.",
            "date": "2024-04-22",
            "impact_level": "High"
        },
        {
            "event_id": "E12346",
            "title": "Trade Agreement Signed",
            "description": "Countries Y and Z sign a new trade agreement.",
            "date": "2024-04-20",
            "impact_level": "Medium"
        }
        // Additional events...
    ]
}
```

---

## Global Consciousness Metrics

- **Description:** Measures global awareness and sentiment on various issues that can influence market trends.
- **URL:** Custom Endpoint (Assuming a third-party or custom API)
- **Method:** GET

### Parameters:

| Parameter | Type   | Required | Description                                      |
|-----------|--------|----------|--------------------------------------------------|
| function  | string | Yes      | Must be `GLOBAL_CONSCIOUSNESS_METRICS`           |
| topic     | string | Yes      | Specific topic (e.g., `Sustainability`)          |
| apikey    | string | Yes      | Your API key                                     |

### Response Format:

- **Format:** JSON

### Example Request:

```bash
https://api.globalconsciousness.com/query?function=GLOBAL_CONSCIOUSNESS_METRICS&topic=Sustainability&apikey=YOUR_API_KEY
```

### Example Response:

```json
{
    "Global Consciousness Metrics": {
        "Topic": "Sustainability",
        "Awareness_Level": "75%",
        "Positive_Sentiment": "60%",
        "Negative_Sentiment": "15%",
        "Neutral_Sentiment": "25%",
        "Last Updated": "2024-04-23"
    }
}
```

---

## Technology Innovations

- **Description:** Tracks recent technological innovations and their potential impact on financial markets.
- **URL:** Custom Endpoint (Assuming a third-party or custom API)
- **Method:** GET

### Parameters:

| Parameter | Type   | Required | Description                                      |
|-----------|--------|----------|--------------------------------------------------|
| function  | string | Yes      | Must be `TECHNOLOGY_INNOVATIONS`                  |
| sector    | string | Yes      | Technology sector (e.g., `Artificial Intelligence`)|
| apikey    | string | Yes      | Your API key                                     |

### Response Format:

- **Format:** JSON

### Example Request:

```bash
https://api.techinnovations.com/query?function=TECHNOLOGY_INNOVATIONS&sector=Artificial%20Intelligence&apikey=YOUR_API_KEY
```

### Example Response:

```json
{
    "Technology Innovations": [
        {
            "innovation_id": "T98765",
            "title": "AI-Powered Trading Algorithms",
            "description": "New algorithms leveraging AI to optimize trading strategies.",
            "date_introduced": "2024-04-18",
            "impact_potential": "High"
        },
        {
            "innovation_id": "T98766",
            "title": "Blockchain in Supply Chain",
            "description": "Implementation of blockchain technology to enhance supply chain transparency.",
            "date_introduced": "2024-04-15",
            "impact_potential": "Medium"
        }
        // Additional innovations...
    ]
}
```

---

# Authentication and Security

All API requests require a valid API key (`apikey`) to authenticate and authorize access. Ensure that your API keys are kept secure and are **not** exposed in public repositories or client-side code.

- **Storing API Keys:**
  - Use environment variables or secure configuration files (e.g., `secrets.yaml`) to store API keys.
  - Ensure that files containing sensitive information are included in `.gitignore` to prevent accidental commits.

- **Usage Example in Python:**

```python
import os
from dotenv import load_dotenv
import yaml

# Load environment variables from .env file
load_dotenv()

# Load secrets from secrets.yaml
with open('config/secrets.yaml', 'r') as f:
    secrets = yaml.safe_load(f.read())

forex_api_key = secrets['api_keys']['forex_api']
bond_yields_api_key = secrets['api_keys']['bond_yields_api']
# Use the API keys in your requests
```

# Error Handling

API responses may include error messages or codes indicating issues with requests. Implement robust error handling in your application to gracefully manage such scenarios.

- **Common Error Responses:**

```json
{
    "Error Message": "Invalid API call. Please retry or visit the documentation."
}
```

- **Handling Errors in Python:**

```python
import requests
import logging

def fetch_global_quote(symbol: str, api_key: str):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": api_key
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    if "Error Message" in data:
        logging.error(f"API Error: {data['Error Message']}")
        raise Exception(data["Error Message"])
    
    return data
```

# Rate Limiting

Most APIs enforce rate limits to prevent abuse and ensure fair usage. Be aware of the rate limits imposed by each API and implement strategies to handle them.

- **Alpha Vantage Rate Limits:**
  - Typically allows 5 API requests per minute and 500 requests per day for the free tier.
  
- **Handling Rate Limits:**

```python
import time
import logging

def fetch_with_rate_limiting(url, params, max_retries=5):
    for attempt in range(max_retries):
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            wait_time = 60  # Wait for 60 seconds before retrying
            logging.warning(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        else:
            response.raise_for_status()
    raise Exception("Maximum retry attempts exceeded due to rate limiting.")
```

# Conclusion

This API documentation serves as a comprehensive guide for integrating and utilizing various APIs within the **AASB: As Above So Below** project. Ensure to keep this document updated with any new endpoints or changes to existing APIs. Proper understanding and management of these APIs are crucial for the successful execution of data collection, preprocessing, modeling, and visualization tasks within the project.

For any further assistance or inquiries regarding the APIs or their integration, please refer to the project's [architecture documentation](./architecture.md) or contact the project maintainer.

---

# Additional Notes

- **API Usage Monitoring:** Regularly monitor your API usage to ensure compliance with rate limits and to avoid unexpected service interruptions.

- **API Key Rotation:** Periodically rotate your API keys as a security best practice to minimize potential risks associated with compromised keys.

- **Extensibility:** As your project evolves, you may integrate additional APIs. Ensure to update this documentation accordingly to maintain its accuracy and usefulness.

- **Documentation Links:** Where applicable, include links to the official API documentation provided by the API service for more detailed information and advanced usage.

---

If you need further customization or additional sections in the `api_documentation.md`, feel free to ask!
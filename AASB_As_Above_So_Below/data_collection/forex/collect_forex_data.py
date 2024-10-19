# data_collection/collect_forex_data.py

import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Union

import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Suppress matplotlib font_manager INFO logs if using matplotlib
logging.getLogger('matplotlib.font_manager').setLevel(logging.ERROR)

class PolygonForexAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.polygon.io"
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Accept': 'application/json'
        }

    def _get(self, endpoint: str, params: Dict[str, Any] = {}) -> Optional[Union[Dict, List]]:
        """
        Internal method to perform GET requests to the Polygon.io API.
        Handles both dictionary and list responses.

        Args:
            endpoint (str): API endpoint.
            params (Dict[str, Any]): Query parameters.

        Returns:
            Optional[Union[Dict, List]]: Parsed JSON response or None if failed.
        """
        url = f"{self.base_url}{endpoint}"
        params['apiKey'] = self.api_key  # Include API key in query params
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, dict):
                status = data.get('status', '').lower()
                if status in ['ok', 'success']:
                    return data
                else:
                    message = data.get('message', 'No message provided.')
                    logging.error(f"API Error: {data.get('status')}, Message: {message}")
                    return None
            elif isinstance(data, list):
                return data
            else:
                logging.error("API response is neither dict nor list.")
                return None
        except requests.exceptions.HTTPError as errh:
            logging.error(f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            logging.error(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            logging.error(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            logging.error(f"OOps: Something Else {err}")
        return None

    def get_aggregate_bars(self, forex_ticker: str, multiplier: int, timespan: str,
                           from_date: str, to_date: str, adjusted: bool = True,
                           sort: str = 'asc', limit: int = 5000) -> Optional[pd.DataFrame]:
        """
        Get aggregate bars for a forex pair over a given date range in custom time window sizes.
        """
        endpoint = f"/v2/aggs/ticker/{forex_ticker}/range/{multiplier}/{timespan}/{from_date}/{to_date}"
        params = {
            'adjusted': str(adjusted).lower(),
            'sort': sort,
            'limit': limit
        }
        data = self._get(endpoint, params)
        if data and 'results' in data:
            df = pd.json_normalize(data['results'])
            logging.info(f"Fetched {len(df)} aggregate bars for {forex_ticker}.")
            return df
        else:
            logging.info("No aggregate bars data found.")
            return None

    def get_grouped_daily_bars(self, date: str, adjusted: bool = True) -> Optional[pd.DataFrame]:
        """
        Get the daily open, high, low, and close (OHLC) for the entire forex markets.
        """
        endpoint = f"/v2/aggs/grouped/locale/global/market/fx/{date}"
        params = {
            'adjusted': str(adjusted).lower()
        }
        data = self._get(endpoint, params)
        if data and 'results' in data:
            df = pd.json_normalize(data['results'])
            logging.info(f"Fetched grouped daily bars for {date}.")
            return df
        else:
            logging.info("No grouped daily bars data found.")
            return None

    def get_previous_close(self, forex_ticker: str, adjusted: bool = True) -> Optional[pd.DataFrame]:
        """
        Get the previous day's open, high, low, and close (OHLC) for the specified forex pair.
        """
        endpoint = f"/v2/aggs/ticker/{forex_ticker}/prev"
        params = {
            'adjusted': str(adjusted).lower()
        }
        data = self._get(endpoint, params)
        if data and 'results' in data:
            df = pd.json_normalize(data['results'])
            logging.info(f"Fetched previous close for {forex_ticker}.")
            return df
        else:
            logging.info("No previous close data found.")
            return None

    def get_quotes(self, fx_ticker: str, limit: int = 1000) -> Optional[pd.DataFrame]:
        """
        Get BBO quotes for a ticker symbol.
        """
        endpoint = f"/v3/quotes/{fx_ticker}"
        params = {
            'limit': limit
        }
        data = self._get(endpoint, params)
        if isinstance(data, list):
            df = pd.json_normalize(data)
            logging.info(f"Fetched {len(df)} quotes for {fx_ticker}.")
            return df
        else:
            logging.info("No quotes data found.")
            return None

    def get_last_quote(self, from_currency: str, to_currency: str) -> Optional[Dict]:
        """
        Get the last quote tick for a forex currency pair.
        """
        endpoint = f"/v1/last_quote/currencies/{from_currency}/{to_currency}"
        data = self._get(endpoint)
        if data and 'last' in data:
            logging.info(f"Fetched last quote for {from_currency}/{to_currency}.")
            return data['last']
        else:
            logging.info("No last quote data found.")
            return None

    def real_time_currency_conversion(self, from_currency: str, to_currency: str,
                                     amount: float, precision: int = 2) -> Optional[Dict]:
        """
        Get currency conversions using the latest market conversion rates.
        """
        endpoint = f"/v1/conversion/{from_currency}/{to_currency}"
        params = {
            'amount': amount,
            'precision': precision
        }
        data = self._get(endpoint, params)
        if data and 'converted' in data:
            logging.info(f"Converted {amount} {from_currency} to {to_currency}: {data['converted']}")
            return data
        else:
            logging.info("No conversion data found.")
            return None

    def get_all_tickers(self, tickers: Optional[List[str]] = None) -> Optional[pd.DataFrame]:
        """
        Get snapshots for assets of all types or specified tickers.
        """
        endpoint = "/v3/reference/tickers"
        params = {}
        if tickers:
            params['ticker'] = ",".join(tickers)
        data = self._get(endpoint, params)
        if isinstance(data, list):
            df = pd.json_normalize(data)
            logging.info(f"Fetched {len(df)} tickers.")
            return df
        else:
            logging.info("No tickers data found.")
            return None

    def get_gainers_losers(self, direction: str = 'gainers') -> Optional[pd.DataFrame]:
        """
        Get the current top 20 gainers or losers of the day in forex markets.
        """
        if direction not in ['gainers', 'losers']:
            logging.error("Invalid direction. Choose 'gainers' or 'losers'.")
            return None
        endpoint = f"/v2/snapshot/locale/global/markets/forex/{direction}"
        data = self._get(endpoint)
        if isinstance(data, dict) and 'tickers' in data:
            df = pd.json_normalize(data['tickers'])
            logging.info(f"Fetched top {direction} in forex markets.")
            return df
        else:
            logging.info(f"No {direction} data found.")
            return None

    def get_ticker_snapshot(self, ticker: str) -> Optional[Dict]:
        """
        Get the current minute, day, and previous day’s aggregate, as well as the last trade and quote for a single traded currency symbol.
        """
        endpoint = f"/v2/snapshot/locale/global/markets/forex/tickers/{ticker}"
        data = self._get(endpoint)
        if isinstance(data, dict) and 'ticker' in data:
            logging.info(f"Fetched snapshot for ticker {ticker}.")
            return data['ticker']
        else:
            logging.info(f"No snapshot data found for ticker {ticker}.")
            return None

    def get_market_holidays(self) -> Optional[pd.DataFrame]:
        """
        Get upcoming market holidays and their open/close times.
        """
        endpoint = "/v1/marketstatus/upcoming"
        data = self._get(endpoint)
        if isinstance(data, list):
            df = pd.json_normalize(data)
            logging.info(f"Fetched {len(df)} upcoming market holidays.")
            return df
        else:
            logging.info("No market holidays data found.")
            return None

    def get_market_status_now(self) -> Optional[Dict]:
        """
        Get the current trading status of the exchanges and overall financial markets.
        """
        endpoint = "/v1/marketstatus/now"
        data = self._get(endpoint)
        if data:
            logging.info("Fetched current market status.")
            return data
        else:
            logging.info("No market status data found.")
            return None

    def get_conditions(self, asset_class: str = 'fx') -> Optional[pd.DataFrame]:
        """
        List all conditions that Polygon.io uses for a specific asset class.
        """
        endpoint = "/v3/reference/conditions"
        params = {
            'asset_class': asset_class
        }
        data = self._get(endpoint, params)
        if isinstance(data, list):
            df = pd.json_normalize(data)
            logging.info(f"Fetched {len(df)} conditions for asset class {asset_class}.")
            return df
        else:
            logging.info("No conditions data found.")
            return None

    def get_exchanges(self, asset_class: str = 'fx') -> Optional[pd.DataFrame]:
        """
        List all exchanges that Polygon.io knows about for a specific asset class.
        """
        endpoint = "/v3/reference/exchanges"
        params = {
            'asset_class': asset_class
        }
        data = self._get(endpoint, params)
        if isinstance(data, list):
            df = pd.json_normalize(data)
            logging.info(f"Fetched {len(df)} exchanges for asset class {asset_class}.")
            return df
        else:
            logging.info("No exchanges data found.")
            return None

    # Additional methods for technical indicators
    def get_technical_indicator_sma(self, fx_ticker: str, timespan: str = 'day',
                                    window: int = 50, series_type: str = 'close',
                                    adjusted: bool = True, order: str = 'desc',
                                    limit: int = 10) -> Optional[pd.DataFrame]:
        """
        Get the Simple Moving Average (SMA) for a forex ticker.
        """
        endpoint = f"/v1/indicators/sma/{fx_ticker}"
        params = {
            'timespan': timespan,
            'window': window,
            'series_type': series_type,
            'adjusted': str(adjusted).lower(),
            'order': order,
            'limit': limit
        }
        data = self._get(endpoint, params)
        if isinstance(data, dict) and 'results' in data and 'values' in data['results']:
            df = pd.json_normalize(data['results']['values'])
            logging.info(f"Fetched SMA data for {fx_ticker}.")
            return df
        else:
            logging.info("No SMA data found.")
            return None

    def get_technical_indicator_ema(self, fx_ticker: str, timespan: str = 'day',
                                    window: int = 50, series_type: str = 'close',
                                    adjusted: bool = True, order: str = 'desc',
                                    limit: int = 10) -> Optional[pd.DataFrame]:
        """
        Get the Exponential Moving Average (EMA) for a forex ticker.
        """
        endpoint = f"/v1/indicators/ema/{fx_ticker}"
        params = {
            'timespan': timespan,
            'window': window,
            'series_type': series_type,
            'adjusted': str(adjusted).lower(),
            'order': order,
            'limit': limit
        }
        data = self._get(endpoint, params)
        if isinstance(data, dict) and 'results' in data and 'values' in data['results']:
            df = pd.json_normalize(data['results']['values'])
            logging.info(f"Fetched EMA data for {fx_ticker}.")
            return df
        else:
            logging.info("No EMA data found.")
            return None

    def get_technical_indicator_macd(self, fx_ticker: str, timespan: str = 'day',
                                     short_window: int = 12, long_window: int = 26,
                                     signal_window: int = 9, series_type: str = 'close',
                                     adjusted: bool = True, order: str = 'desc',
                                     limit: int = 10) -> Optional[pd.DataFrame]:
        """
        Get the Moving Average Convergence/Divergence (MACD) for a forex ticker.
        """
        endpoint = f"/v1/indicators/macd/{fx_ticker}"
        params = {
            'timespan': timespan,
            'short_window': short_window,
            'long_window': long_window,
            'signal_window': signal_window,
            'series_type': series_type,
            'adjusted': str(adjusted).lower(),
            'order': order,
            'limit': limit
        }
        data = self._get(endpoint, params)
        if isinstance(data, dict) and 'results' in data and 'values' in data['results']:
            df = pd.json_normalize(data['results']['values'])
            logging.info(f"Fetched MACD data for {fx_ticker}.")
            return df
        else:
            logging.info("No MACD data found.")
            return None

    def get_technical_indicator_rsi(self, fx_ticker: str, timespan: str = 'day',
                                    window: int = 14, series_type: str = 'close',
                                    adjusted: bool = True, order: str = 'desc',
                                    limit: int = 10) -> Optional[pd.DataFrame]:
        """
        Get the Relative Strength Index (RSI) for a forex ticker.
        """
        endpoint = f"/v1/indicators/rsi/{fx_ticker}"
        params = {
            'timespan': timespan,
            'window': window,
            'series_type': series_type,
            'adjusted': str(adjusted).lower(),
            'order': order,
            'limit': limit
        }
        data = self._get(endpoint, params)
        if isinstance(data, dict) and 'results' in data and 'values' in data['results']:
            df = pd.json_normalize(data['results']['values'])
            logging.info(f"Fetched RSI data for {fx_ticker}.")
            return df
        else:
            logging.info("No RSI data found.")
            return None

def collect_forex_data(start_date: str, end_date: str) -> Optional[Dict[str, Any]]:
    """
    Function to collect forex data using the PolygonForexAPI.
    
    Args:
        start_date (str): The start date for data collection in 'YYYY-MM-DD' format.
        end_date (str): The end date for data collection in 'YYYY-MM-DD' format.
    
    Returns:
        Optional[Dict[str, Any]]: A dictionary containing all fetched dataframes and other information.
    """
    logging.info("Starting data collection...")

    # Load API key from environment variable or replace with your API key
    API_KEY = os.getenv('POLYGON_API_KEY', 'YOUR_API_KEY_HERE')
    
    if API_KEY == 'YOUR_API_KEY_HERE':
        logging.error("Please set your Polygon.io API key in the environment variable 'POLYGON_API_KEY'.")
        return None

    # Initialize the API client
    forex_api = PolygonForexAPI(api_key=API_KEY)
    
    # Example Usage:
    
    # 1. Fetch Aggregate Bars
    forex_ticker = "C:EURUSD"
    multiplier = 1
    timespan = "day"
    df_agg = forex_api.get_aggregate_bars(forex_ticker, multiplier, timespan, start_date, end_date)
    
    # 2. Fetch Grouped Daily Bars
    df_grouped_daily = forex_api.get_grouped_daily_bars(start_date)
    
    # 3. Fetch Previous Close
    df_prev_close = forex_api.get_previous_close(forex_ticker)
    
    # 4. Fetch Quotes
    df_quotes = forex_api.get_quotes(forex_ticker)
    
    # 5. Fetch Last Quote
    last_quote = forex_api.get_last_quote("EUR", "USD")
    
    # 6. Real-time Currency Conversion
    conversion = forex_api.real_time_currency_conversion("EUR", "USD", 100)
    
    # 7. Fetch All Tickers
    df_tickers = forex_api.get_all_tickers()
    
    # 8. Fetch Gainers
    df_gainers = forex_api.get_gainers_losers(direction='gainers')
    
    # 9. Fetch Losers
    df_losers = forex_api.get_gainers_losers(direction='losers')
    
    # 10. Fetch Ticker Snapshot
    ticker_snapshot = forex_api.get_ticker_snapshot(forex_ticker)
    
    # 11. Fetch Market Holidays
    df_holidays = forex_api.get_market_holidays()
    
    # 12. Fetch Market Status
    market_status = forex_api.get_market_status_now()
    
    # 13. Fetch Conditions
    df_conditions = forex_api.get_conditions(asset_class='fx')
    
    # 14. Fetch Exchanges
    df_exchanges = forex_api.get_exchanges(asset_class='fx')
    
    # 15. Fetch Technical Indicators
    # SMA
    df_sma = forex_api.get_technical_indicator_sma(forex_ticker)
    
    # EMA
    df_ema = forex_api.get_technical_indicator_ema(forex_ticker)
    
    # MACD
    df_macd = forex_api.get_technical_indicator_macd(forex_ticker)
    
    # RSI
    df_rsi = forex_api.get_technical_indicator_rsi(forex_ticker)
    
    # Example: Save fetched data to CSV files
    data_summary = {}
    
    if df_agg is not None:
        df_agg.to_csv("aggregate_bars.csv", index=False)
        data_summary['aggregate_bars'] = len(df_agg)
    if df_grouped_daily is not None:
        df_grouped_daily.to_csv("grouped_daily_bars.csv", index=False)
        data_summary['grouped_daily_bars'] = len(df_grouped_daily)
    if df_prev_close is not None:
        df_prev_close.to_csv("previous_close.csv", index=False)
        data_summary['previous_close'] = len(df_prev_close)
    if df_quotes is not None:
        df_quotes.to_csv("quotes.csv", index=False)
        data_summary['quotes'] = len(df_quotes)
    if df_tickers is not None:
        df_tickers.to_csv("tickers.csv", index=False)
        data_summary['tickers'] = len(df_tickers)
    if df_gainers is not None:
        df_gainers.to_csv("gainers.csv", index=False)
        data_summary['gainers'] = len(df_gainers)
    if df_losers is not None:
        df_losers.to_csv("losers.csv", index=False)
        data_summary['losers'] = len(df_losers)
    if df_holidays is not None:
        df_holidays.to_csv("market_holidays.csv", index=False)
        data_summary['market_holidays'] = len(df_holidays)
    if df_conditions is not None:
        df_conditions.to_csv("conditions.csv", index=False)
        data_summary['conditions'] = len(df_conditions)
    if df_exchanges is not None:
        df_exchanges.to_csv("exchanges.csv", index=False)
        data_summary['exchanges'] = len(df_exchanges)
    if df_sma is not None:
        df_sma.to_csv("sma.csv", index=False)
        data_summary['sma'] = len(df_sma)
    if df_ema is not None:
        df_ema.to_csv("ema.csv", index=False)
        data_summary['ema'] = len(df_ema)
    if df_macd is not None:
        df_macd.to_csv("macd.csv", index=False)
        data_summary['macd'] = len(df_macd)
    if df_rsi is not None:
        df_rsi.to_csv("rsi.csv", index=False)
        data_summary['rsi'] = len(df_rsi)
    
    # Print fetched data summaries
    logging.info("\n=== Data Fetch Summary ===")
    for key, value in data_summary.items():
        logging.info(f"{key.replace('_', ' ').title()}: {value} records")
    
    # Prepare a dictionary to return all data if needed
    collected_data = {
        'aggregate_bars': df_agg,
        'grouped_daily_bars': df_grouped_daily,
        'previous_close': df_prev_close,
        'quotes': df_quotes,
        'tickers': df_tickers,
        'gainers': df_gainers,
        'losers': df_losers,
        'market_holidays': df_holidays,
        'conditions': df_conditions,
        'exchanges': df_exchanges,
        'sma': df_sma,
        'ema': df_ema,
        'macd': df_macd,
        'rsi': df_rsi,
        'last_quote': last_quote,
        'conversion': conversion,
        'ticker_snapshot': ticker_snapshot,
        'market_status': market_status
    }
    
    return collected_data

# Optional: Keep the existing main function or remove it
def main():
    # Define your start and end dates here
    start_date = "2010-01-01"
    end_date = "2020-12-31"
    
    collected_data = collect_forex_data(start_date, end_date)
    
    if collected_data is not None:
        logging.info("Forex data collected and saved successfully.")
    else:
        logging.error("Failed to collect forex data.")

if __name__ == "__main__":
    main()
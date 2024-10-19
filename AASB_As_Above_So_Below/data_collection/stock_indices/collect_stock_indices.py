# collect_stock_indices.py

import os
import requests
import pandas as pd
from typing import List, Dict, Any, Optional, Union
import logging
import time
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PolygonIndicesAPI:
    """
    A class to interact with the Polygon.io API for fetching stock indices data.
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.polygon.io"
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Accept': 'application/json'
        })

    def _get(self, endpoint: str, params: Dict[str, Any] = {}) -> Optional[Dict]:
        """
        Internal method to perform GET requests to the Polygon.io API.

        Args:
            endpoint (str): API endpoint.
            params (Dict[str, Any]): Query parameters.

        Returns:
            Optional[Dict]: Parsed JSON response or None if failed.
        """
        url = f"{self.base_url}{endpoint}"
        params['apiKey'] = self.api_key  # Include API key in query params

        try:
            logging.info(f"Requesting URL: {url} with params: {params}")
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            # Check for success status
            status = data.get('status', '').lower()
            if status not in ['ok', 'success']:
                message = data.get('message', 'No message provided.')
                logging.error(f"API Error: {status}, Message: {message}")
                return None

            return data

        except requests.exceptions.HTTPError as errh:
            if response.status_code == 403:
                logging.error(f"Access Forbidden (403): {errh}. Check your API key and subscription level.")
            elif response.status_code == 404:
                logging.error(f"Resource Not Found (404): {errh}. Verify the endpoint and parameters.")
            else:
                logging.error(f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            logging.error(f"Connection Error: {errc}")
        except requests.exceptions.Timeout as errt:
            logging.error(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            logging.error(f"Request Exception: {err}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")

        return None

    def fetch_aggregate_bars(self, ticker: str, multiplier: int, timespan: str,
                             from_date: str, to_date: str, sort: str = 'asc',
                             limit: int = 5000) -> Optional[pd.DataFrame]:
        """
        Fetch aggregate bars for a given stock index over a specified date range.

        Args:
            ticker (str): The Polygon.io ticker symbol for the index (e.g., "SPX").
            multiplier (int): The size multiplier for the timespan (e.g., 1 for daily).
            timespan (str): The timespan for each aggregate bar (e.g., "day", "minute", "second").
            from_date (str): The start date in 'YYYY-MM-DD' format.
            to_date (str): The end date in 'YYYY-MM-DD' format.
            sort (str): Sort order, either 'asc' or 'desc'.
            limit (int): Maximum number of aggregate bars to retrieve per page (max 50000).

        Returns:
            Optional[pd.DataFrame]: DataFrame containing the aggregate bars or None if no data is found.
        """
        endpoint = f"/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{from_date}/{to_date}"
        params = {
            'sort': sort,
            'limit': limit,
            'page': 1  # Starting with page 1
        }
        all_results = []
        current_page = 1
        total_pages = 1  # Initialize to enter the loop

        logging.info(f"Fetching aggregate bars for {ticker} from {from_date} to {to_date}")

        while current_page <= total_pages:
            params['page'] = current_page
            data = self._get(endpoint, params)

            if data and 'results' in data:
                results = data.get('results', [])
                if not results:
                    logging.warning(f"No aggregate bars found on page {current_page} for {ticker}.")
                    break

                all_results.extend(results)
                logging.info(f"Fetched {len(results)} aggregate bars on page {current_page}.")

                # Update pagination
                total_count = data.get('count', 0)
                total_pages = (total_count // limit) + (1 if total_count % limit > 0 else 0)
                current_page += 1

                # Respect rate limits
                time.sleep(0.2)  # Adjust based on your rate limit
            else:
                logging.warning(f"No aggregate bars found on page {current_page} for {ticker}.")
                break

        if all_results:
            df = pd.json_normalize(all_results)
            if 't' in df.columns:
                # Convert timestamp to datetime
                df['date'] = pd.to_datetime(df['t'], unit='ms')
                df.drop(columns=['t'], inplace=True)
            else:
                logging.warning(f"No timestamp column 't' found for {ticker}.")
                df['date'] = pd.NaT

            logging.info(f"Successfully fetched {len(df)} aggregate bars for {ticker}.")
            return df
        else:
            logging.warning(f"No aggregate bars data collected for {ticker}.")
            return None

    def fetch_previous_close(self, ticker: str) -> Optional[Dict[str, Any]]:
        """
        Fetch the previous day's OHLC data for a given stock index.

        Args:
            ticker (str): The Polygon.io ticker symbol for the index (e.g., "SPX").

        Returns:
            Optional[Dict[str, Any]]: Dictionary containing the previous close data or None if not found.
        """
        endpoint = f"/v2/aggs/ticker/{ticker}/prev"
        params = {}

        logging.info(f"Fetching previous close for {ticker}")

        data = self._get(endpoint, params)

        if data and 'results' in data and isinstance(data['results'], list) and len(data['results']) > 0:
            prev_close = data['results'][0]
            logging.info(f"Successfully fetched previous close for {ticker}.")
            return prev_close
        else:
            logging.warning(f"No previous close data found for {ticker}.")
            return None

    def fetch_technical_indicator(self, ticker: str, indicator: str, timespan: str,
                                  window: int, series_type: str, from_date: str,
                                  to_date: str, sort: str = 'desc', limit: int = 5000) -> Optional[pd.DataFrame]:
        """
        Fetch technical indicators (SMA, EMA, MACD, RSI) for a given stock index.

        Args:
            ticker (str): The Polygon.io ticker symbol for the index (e.g., "SPX").
            indicator (str): The technical indicator to fetch ('sma', 'ema', 'macd', 'rsi').
            timespan (str): The timespan for each aggregate window (e.g., "day").
            window (int): The window size for the indicator.
            series_type (str): The data series to use ('close').
            from_date (str): The start date in 'YYYY-MM-DD' format.
            to_date (str): The end date in 'YYYY-MM-DD' format.
            sort (str): Sort order, either 'asc' or 'desc'.
            limit (int): Maximum number of results to retrieve (max 5000).

        Returns:
            Optional[pd.DataFrame]: DataFrame containing the technical indicator data or None if no data is found.
        """
        endpoint = f"/v1/indicators/{indicator}/{ticker}"
        params = {
            'timespan': timespan,
            'window': window,
            'series_type': series_type,
            'from': from_date,
            'to': to_date,
            'sort': sort,
            'limit': limit
        }

        logging.info(f"Fetching {indicator.upper()} for {ticker} from {from_date} to {to_date}")

        data = self._get(endpoint, params)

        if data and 'results' in data:
            results = data['results']
            if not isinstance(results, list) or len(results) == 0:
                logging.warning(f"No {indicator.upper()} data found for {ticker}.")
                return None

            df_indicator = pd.json_normalize(results)
            if 'timestamp' in df_indicator.columns and 'value' in df_indicator.columns:
                df_indicator['date'] = pd.to_datetime(df_indicator['timestamp'], unit='ms')
                df_indicator.rename(columns={'value': f"{ticker}_{indicator.upper()}_{window}"}, inplace=True)
                df_indicator = df_indicator[['date', f"{ticker}_{indicator.upper()}_{window}"]]
                logging.info(f"Successfully fetched {indicator.upper()} for {ticker}.")
                return df_indicator
            else:
                logging.warning(f"Expected columns 'timestamp' and 'value' not found in {indicator.upper()} data for {ticker}.")
                return None
        else:
            logging.warning(f"No {indicator.upper()} data found for {ticker}.")
            return None

def collect_stock_indices(start_date: str, end_date: str) -> pd.DataFrame:
    """
    Collects historical data for major stock market indices using Polygon.io's Indices API.

    Indices reflect investor confidence and economic health.
    Movements in these indices influence investment decisions, portfolio valuations,
    and can trigger automated trading mechanisms.

    Parameters:
    - start_date (str): The start date for data collection in 'YYYY-MM-DD' format.
    - end_date (str): The end date for data collection in 'YYYY-MM-DD' format.

    Returns:
    - df_indices (DataFrame): A pandas DataFrame containing the indices data with 'date' and index columns.
    """
    # Option 1: Set API key directly in the script (Not Recommended for Production)
    API_KEY = '3JyYCGAN26Apg_16hwJFJXZqC4PSiKHe'  # Replace with your actual Polygon.io API key

    # Option 2: Use environment variable (Recommended)
    # API_KEY = os.getenv('POLYGON_API_KEY')
    # if not API_KEY:
    #     logging.error("Polygon.io API key not found. Please set the 'POLYGON_API_KEY' environment variable.")
    #     return pd.DataFrame()

    if not API_KEY or API_KEY == 'your_polygon_api_key_here':
        logging.error("Polygon.io API key is not set correctly. Please update the 'API_KEY' variable in the script.")
        return pd.DataFrame()

    # Initialize the Polygon.io Indices API client
    polygon_api = PolygonIndicesAPI(api_key=API_KEY)

    # Dictionary of stock indices and their Polygon.io ticker symbols
    indices = {
        'S&P_500': 'SPX',                  # S&P 500 Index
        'FTSE_100': 'FTSE',                # FTSE 100 Index
        'Nikkei_225': 'N225',              # Nikkei 225 Index
        'Dow_Jones': 'DJI',                # Dow Jones Industrial Average
        'DAX': 'GDAXI',                    # DAX Index
        'Shanghai_Composite': '000001.SS'   # Shanghai Composite Index
    }

    data_indices = {}
    technical_indicators = ['sma', 'ema', 'macd', 'rsi']
    indicator_windows = {
        'sma': 50,
        'ema': 50,
        'macd': 26,  # Typically, MACD uses short and long windows, but for simplicity, using one window
        'rsi': 14
    }

    for name, ticker in indices.items():
        logging.info(f"Processing index: {name} ({ticker})")

        # Fetch aggregate bars (daily)
        df_agg = polygon_api.fetch_aggregate_bars(
            ticker=ticker,
            multiplier=1,
            timespan='day',
            from_date=start_date,
            to_date=end_date,
            sort='asc',
            limit=5000
        )

        if df_agg is None or df_agg.empty:
            logging.warning(f"No aggregate data retrieved for {name} ({ticker}). Skipping.")
            continue

        # Use the 'c' (close) price as the index value
        if 'c' in df_agg.columns:
            df_close = df_agg[['date', 'c']].copy()
            df_close.rename(columns={'c': name}, inplace=True)
            data_indices[name] = df_close.set_index('date')[name]
            logging.info(f"Collected aggregate close data for {name}")
        else:
            logging.warning(f"No 'c' (close) column found in aggregate data for {name} ({ticker}). Skipping.")
            continue

        # Fetch and add technical indicators
        for indicator in technical_indicators:
            window = indicator_windows.get(indicator, 50)
            df_indicator = polygon_api.fetch_technical_indicator(
                ticker=ticker,
                indicator=indicator,
                timespan='day',
                window=window,
                series_type='close',
                from_date=start_date,
                to_date=end_date,
                sort='asc',
                limit=5000
            )

            if df_indicator is not None and not df_indicator.empty:
                # Align the indicator with the main DataFrame based on 'date'
                indicator_col = f"{name}_{indicator.upper()}_{window}"
                data_indices[indicator_col] = df_indicator[indicator_col]
                logging.info(f"Added {indicator.upper()} data for {name}")
            else:
                logging.warning(f"No {indicator.upper()} data found for {name} ({ticker}).")

    if data_indices:
        # Combine all index data into a single DataFrame
        df_indices = pd.DataFrame(data_indices)
        # Reset index to have 'date' as a column
        df_indices.reset_index(inplace=True)
        # Sort by date
        df_indices.sort_values('date', inplace=True)
        logging.info('Successfully collected and merged all stock indices data.')
    else:
        df_indices = pd.DataFrame(columns=['date'] + list(indices.keys()))
        logging.warning('No stock indices data was collected.')

    # Save to CSV
    output_filename = f"stock_indices_{start_date}_to_{end_date}.csv"
    df_indices.to_csv(output_filename, index=False)
    logging.info(f"Saved collected data to {output_filename}.")

    return df_indices

def main():
    # Define the date range for data collection
    start_date = "2010-01-01"
    end_date = "2020-12-31"

    # Collect stock indices data
    df_stock_indices = collect_stock_indices(start_date, end_date)

    # Display the first few rows
    print("\n=== Stock Indices Data ===")
    print(df_stock_indices.head())

if __name__ == "__main__":
    main()
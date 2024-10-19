# collect_commodity_prices.py

import pandas as pd
import yfinance as yf
from datetime import datetime
import sys

def validate_dates(start_date, end_date):
    """
    Validates the format and logical order of the provided dates.

    Parameters:
    - start_date (str): Start date in 'YYYY-MM-DD' format.
    - end_date (str): End date in 'YYYY-MM-DD' format.

    Returns:
    - bool: True if dates are valid, False otherwise.
    """
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        if start > end:
            raise ValueError("start_date must be earlier than end_date.")
    except ValueError as ve:
        print(f"Date validation error: {ve}")
        return False
    return True

def collect_commodity_prices(start_date, end_date):
    """
    Collects prices for various commodities using Yahoo Finance.

    Commodity prices impact the profitability of companies in related sectors (e.g., energy, mining, agriculture).
    They also serve as indicators of global economic activity and inflationary pressures.

    Parameters:
    - start_date (str): The start date for data collection in 'YYYY-MM-DD' format.
    - end_date (str): The end date for data collection in 'YYYY-MM-DD' format.

    Returns:
    - df_commodities (DataFrame): A pandas DataFrame containing the commodity prices with 'date' and commodity columns.
    """
    # Dictionary of commodities and their Yahoo Finance ticker symbols
    commodities = {
        'Gold': 'GC=F',          # Gold Futures
        'Crude_Oil': 'CL=F',     # Crude Oil Futures
        'Silver': 'SI=F',        # Silver Futures
        'Natural_Gas': 'NG=F',   # Natural Gas Futures
        'Corn': 'ZC=F',          # Corn Futures
        'Soybeans': 'ZS=F'       # Soybeans Futures
    }

    data_commodities = {}

    for name, symbol in commodities.items():
        try:
            # Download historical data for each commodity
            data = yf.download(symbol, start=start_date, end=end_date)
            # Check if data is returned
            if data.empty:
                print(f'No data retrieved for {name}.')
                continue
            # Use the 'Close' price as the commodity price
            data_commodities[name] = data['Close']
            print(f'Downloaded data for {name}')
        except Exception as e:
            print(f"An error occurred while fetching data for {name}: {e}")
            continue

    if data_commodities:
        # Combine all commodity data into a single DataFrame
        df_commodities = pd.DataFrame(data_commodities)
        # Reset index to have 'date' as a column
        df_commodities.reset_index(inplace=True)
        # Rename 'Date' column to 'date' for consistency
        df_commodities.rename(columns={'Date': 'date'}, inplace=True)
        print('Collected commodity prices')
    else:
        df_commodities = pd.DataFrame(columns=['date'] + list(commodities.keys()))
        print('No commodity data was collected.')

    return df_commodities

def save_to_csv(df, filename):
    """
    Saves the DataFrame to a CSV file.

    Parameters:
    - df (DataFrame): The pandas DataFrame to save.
    - filename (str): The filename for the CSV file.
    """
    try:
        df.to_csv(filename, index=False)
        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"Failed to save data to {filename}: {e}")

if __name__ == "__main__":
    # Configuration Parameters
    START_DATE = '2020-01-01'
    END_DATE = '2023-12-31'

    # Validate dates
    if not validate_dates(START_DATE, END_DATE):
        sys.exit(1)

    # Collect commodity prices
    commodity_prices_df = collect_commodity_prices(START_DATE, END_DATE)

    if not commodity_prices_df.empty:
        print(commodity_prices_df.head())
        # Save to CSV
        save_to_csv(commodity_prices_df, 'commodity_prices.csv')
    else:
        print("No commodity prices data to display.")
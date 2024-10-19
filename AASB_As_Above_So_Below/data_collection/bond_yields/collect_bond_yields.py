# collect_bond_yields.py

import pandas as pd
import yfinance as yf
from datetime import datetime
import sys

def validate_dates(start_date, end_date):
    """
    Validates the format and logical order of the provided dates.
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

def collect_bond_yields(start_date, end_date):
    """
    Collects U.S. 10-Year Treasury Note yields.

    Parameters:
    - start_date (str): The start date for data collection in 'YYYY-MM-DD' format.
    - end_date (str): The end date for data collection in 'YYYY-MM-DD' format.

    Returns:
    - df_bonds (DataFrame): A pandas DataFrame containing the bond yields with 'date' and 'US10Y' columns.
    """
    symbol = '^TNX'  # U.S. 10-Year Treasury Note symbol in Yahoo Finance
    try:
        data = yf.download(symbol, start=start_date, end=end_date)
    except Exception as e:
        print(f"An error occurred while fetching data: {e}")
        return pd.DataFrame(columns=['date', 'US10Y'])

    # Check if data is returned
    if data.empty:
        print('No data retrieved for bond yields.')
        return pd.DataFrame(columns=['date', 'US10Y'])

    df_bonds = data[['Close']].reset_index()
    df_bonds.rename(columns={'Close': 'US10Y', 'Date': 'date'}, inplace=True)
    print('Collected bond yields')
    return df_bonds

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

    # Collect bond yields
    bond_yields_df = collect_bond_yields(START_DATE, END_DATE)

    if not bond_yields_df.empty:
        print(bond_yields_df.head())
        # Save to CSV
        save_to_csv(bond_yields_df, 'us10y_bond_yields.csv')
    else:
        print("No bond yields data to display.")
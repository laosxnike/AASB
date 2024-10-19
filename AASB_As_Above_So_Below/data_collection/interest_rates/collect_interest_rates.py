# collect_interest_rates.py

import pandas as pd
import pandas_datareader.data as web
from datetime import datetime
import sys
import os

def collect_interest_rates(start_date, end_date, symbol='FEDFUNDS', api_key=None):
    """
    Collects the Federal Funds Effective Rate from the Federal Reserve Economic Data (FRED).

    Interest rates influence borrowing costs, consumer spending, and business investment.
    They play a critical role in shaping economic growth, inflation, and currency strength,
    thereby affecting stock and bond markets.

    Parameters:
    - start_date (str): The start date for data collection in 'YYYY-MM-DD' format.
    - end_date (str): The end date for data collection in 'YYYY-MM-DD' format.
    - symbol (str): The FRED symbol for the desired interest rate series. Default is 'FEDFUNDS'.
    - api_key (str): Your FRED API key. If None, the function will look for the 'FRED_API_KEY' environment variable.

    Returns:
    - df_interest_rates (DataFrame): A pandas DataFrame containing the interest rates with 'date' and 'Fed_Funds_Rate' columns.
    """
    try:
        if api_key:
            os.environ['FRED_API_KEY'] = api_key  # Temporarily set the environment variable
        else:
            api_key = os.getenv('FRED_API_KEY')
            if not api_key:
                raise ValueError("FRED API key not found. Please set the 'FRED_API_KEY' environment variable or pass it as a parameter.")

        # Fetch the Federal Funds Effective Rate from FRED
        df_interest = web.DataReader(symbol, 'fred', start_date, end_date).reset_index()
        df_interest.rename(columns={'DATE': 'date', symbol: 'Fed_Funds_Rate'}, inplace=True)
        
        # Ensure 'date' is in datetime format
        df_interest['date'] = pd.to_datetime(df_interest['date'])
        
        # Handle missing data if any
        if df_interest['Fed_Funds_Rate'].isnull().any():
            print("Warning: Missing data detected. Applying forward fill to handle missing values.")
            df_interest['Fed_Funds_Rate'].fillna(method='ffill', inplace=True)
            df_interest['Fed_Funds_Rate'].fillna(method='bfill', inplace=True)  # In case forward fill doesn't cover initial NaNs
        
        print('Successfully collected interest rates data.')
    
    except web._utils.RemoteDataError as e:
        print(f"RemoteDataError: {e}")
        df_interest = pd.DataFrame(columns=['date', 'Fed_Funds_Rate'])
    except Exception as e:
        print(f"An error occurred while fetching interest rates data: {e}")
        df_interest = pd.DataFrame(columns=['date', 'Fed_Funds_Rate'])
    
    return df_interest

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
    # Example usage
    START_DATE = '2020-01-01'
    END_DATE = '2023-12-31'
    SYMBOL = 'FEDFUNDS'  # Recommended symbol for Effective Federal Funds Rate
    API_KEY = None  # Replace with your API key string if not using environment variable

    # Collect interest rates
    interest_rates_df = collect_interest_rates(START_DATE, END_DATE, SYMBOL, API_KEY)
    
    if not interest_rates_df.empty:
        print(interest_rates_df.head())
        # Save to CSV
        save_to_csv(interest_rates_df, 'fed_funds_rate.csv')
    else:
        print("No data was collected.")
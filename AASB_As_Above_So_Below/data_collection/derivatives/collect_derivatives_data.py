# collect_derivatives_data.py

import pandas as pd
import yfinance as yf
from datetime import datetime
import time
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

def collect_derivatives_data(start_date, end_date):
    """
    Collects options data for major indices like the S&P 500.

    Derivatives allow for hedging and speculation, influencing volatility and liquidity
    in the underlying asset markets. They can amplify market movements and serve as
    indicators of market expectations and risk sentiment.

    Parameters:
    - start_date (str): The start date for data collection in 'YYYY-MM-DD' format.
    - end_date (str): The end date for data collection in 'YYYY-MM-DD' format.

    Returns:
    - df_options (DataFrame): A pandas DataFrame containing the derivatives data with relevant columns.
    """
    # Validate dates
    if not validate_dates(start_date, end_date):
        print("Invalid date range. Exiting.")
        return pd.DataFrame()

    ticker_symbol = 'SPY'
    try:
        ticker = yf.Ticker(ticker_symbol)
        options_dates = ticker.options
        if not options_dates:
            print(f"No options data available for ticker '{ticker_symbol}'.")
            return pd.DataFrame()
    except Exception as e:
        print(f"Error initializing ticker '{ticker_symbol}': {e}")
        return pd.DataFrame()

    try:
        options_dates_dt = [datetime.strptime(date, '%Y-%m-%d') for date in options_dates]
    except ValueError as ve:
        print(f"Date parsing error: {ve}")
        return pd.DataFrame()

    start_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_dt = datetime.strptime(end_date, '%Y-%m-%d')

    filtered_dates = [date.strftime('%Y-%m-%d') for date in options_dates_dt if start_dt <= date <= end_dt]

    if not filtered_dates:
        print("No expiration dates found within the specified date range.")
        return pd.DataFrame()

    options_data = []

    for exp_date in filtered_dates:
        try:
            opt_chain = ticker.option_chain(exp_date)
            calls = opt_chain.calls
            puts = opt_chain.puts
            calls['option_type'] = 'call'
            puts['option_type'] = 'put'
            options = pd.concat([calls, puts], ignore_index=True)
            options['expirationDate'] = exp_date
            options_data.append(options)
            print(f'Collected options data for expiration date {exp_date}')
            # Sleep to avoid rate limiting
            time.sleep(0.5)  # Adjust as needed
        except Exception as e:
            print(f'Error collecting options data for {exp_date}: {e}')
            continue

    if options_data:
        try:
            df_options = pd.concat(options_data, ignore_index=True)
            df_options['lastTradeDate'] = pd.to_datetime(df_options['lastTradeDate'])
            df_options = df_options[(df_options['lastTradeDate'] >= start_date) & (df_options['lastTradeDate'] <= end_date)]
            print('Collected and processed derivatives data')
        except Exception as e:
            print(f"Error processing concatenated options data: {e}")
            df_options = pd.DataFrame()
    else:
        df_options = pd.DataFrame()
        print('No derivatives data was collected.')

    return df_options

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

def main():
    """
    Main function to execute the derivatives data collection.
    """
    # Configuration Parameters
    START_DATE = '2021-01-01'  # Modify as needed
    END_DATE = '2023-12-31'    # Modify as needed
    OUTPUT_FILENAME = 'derivatives_data.csv'  # Modify as needed

    # Collect derivatives data
    derivatives_df = collect_derivatives_data(START_DATE, END_DATE)

    if not derivatives_df.empty:
        print("\nFirst few rows of the collected data:")
        print(derivatives_df.head())
        # Save to CSV
        save_to_csv(derivatives_df, OUTPUT_FILENAME)
    else:
        print("No derivatives data to display.")

if __name__ == "__main__":
    main()
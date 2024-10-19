# collect_cultural_trends.py

import pandas as pd
from pytrends.request import TrendReq
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

def collect_cultural_trends(start_date, end_date):
    """
    Collects data on cultural and social trends using Google Trends.

    Changes in consumer preferences affect demand for products and services,
    influencing the performance of companies and sectors.

    Parameters:
    - start_date (str): The start date for data collection in 'YYYY-MM-DD' format.
    - end_date (str): The end date for data collection in 'YYYY-MM-DD' format.

    Returns:
    - df_cultural (DataFrame): A pandas DataFrame containing the cultural trends data with 'date' and trend columns.
    """
    # Validate dates
    if not validate_dates(start_date, end_date):
        print("Invalid date range. Exiting.")
        return pd.DataFrame()

    try:
        # Initialize pytrends request
        pytrends = TrendReq(hl='en-US', tz=360)
    except Exception as e:
        print(f"Failed to initialize pytrends: {e}")
        return pd.DataFrame()

    # Define keywords in batches (max 5 per batch for efficiency)
    kw_batches = [
        ['sustainability', 'veganism', 'remote work', 'blockchain', 'climate change'],
        ['mental health']
    ]
    
    # Create an empty DataFrame to store the trends data
    df_cultural = pd.DataFrame()
    
    for batch in kw_batches:
        try:
            # Build payload for the current batch
            pytrends.build_payload(batch, cat=0, timeframe=f'{start_date} {end_date}', geo='', gprop='')
            # Retrieve interest over time
            data = pytrends.interest_over_time()
            if not data.empty:
                data = data.reset_index()
                # Drop 'isPartial' column if present
                if 'isPartial' in data.columns:
                    data = data.drop(columns=['isPartial'])
                if df_cultural.empty:
                    df_cultural = data
                else:
                    df_cultural = df_cultural.merge(data, on='date', how='outer')
                print(f'Collected Google Trends data for batch: {batch}')
            else:
                print(f'No data found for batch: {batch}')
            # Sleep to avoid rate limiting
            time.sleep(1)  # Sleep for 1 second between requests
        except Exception as e:
            print(f"An error occurred while fetching data for batch {batch}: {e}")
            continue
    
    if not df_cultural.empty:
        # Handle missing values by filling with 0
        df_cultural.fillna(0, inplace=True)
        print('Collected cultural and social trends data')
    else:
        df_cultural = pd.DataFrame(columns=['date'] + [kw for batch in kw_batches for kw in batch])
        print('No cultural and social trends data was collected.')
    
    return df_cultural

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
    Main function to execute the cultural trends data collection.
    """
    # Configuration Parameters
    START_DATE = '2021-01-01'  # Modify as needed
    END_DATE = '2023-12-31'    # Modify as needed
    OUTPUT_FILENAME = 'cultural_trends.csv'  # Modify as needed

    # Collect cultural trends
    cultural_trends_df = collect_cultural_trends(START_DATE, END_DATE)

    if not cultural_trends_df.empty:
        print("\nFirst few rows of the collected data:")
        print(cultural_trends_df.head())
        # Save to CSV
        save_to_csv(cultural_trends_df, OUTPUT_FILENAME)
    else:
        print("No cultural trends data to display.")

if __name__ == "__main__":
    main()
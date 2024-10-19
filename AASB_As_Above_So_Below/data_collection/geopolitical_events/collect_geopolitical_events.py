# collect_geopolitical_events.py

import pandas as pd
import requests
from datetime import datetime, timedelta
import time

def collect_geopolitical_events(query, start_date, end_date, mode='artlist', max_records=100, format='JSON'):
    """
    Collects data on geopolitical events using the GDELT 2.0 DOC API.

    The DOC 2.0 API allows searching across a rolling window of the last 3 months,
    supports multiple languages, includes image data, and offers various output formats.

    Parameters:
    - query (str): The search query string.
    - start_date (str): The start date for data collection in 'YYYYMMDDHHMMSS' format.
    - end_date (str): The end date for data collection in 'YYYYMMDDHHMMSS' format.
    - mode (str): The output mode (e.g., 'artlist', 'imagecollageinfo').
    - max_records (int): Maximum number of records to retrieve per request (up to 250).
    - format (str): The output format ('JSON', 'CSV', 'RSS', etc.).

    Returns:
    - df_events (DataFrame): A pandas DataFrame containing the geopolitical events data.
    """

    base_url = 'https://api.gdeltproject.org/api/v2/doc/doc'

    params = {
        'query': query,
        'mode': mode,
        'maxrecords': max_records,
        'format': format,
        'startdatetime': start_date,
        'enddatetime': end_date,
        'timespan': '3months',  # Rolling window of the last 3 months
        'sort': 'datedesc'       # Sort by date descending
    }

    headers = {
        'Accept': 'application/json'
    }

    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()

        if format.upper() == 'JSON':
            data = response.json()
            if data and len(data) > 1:
                df_events = pd.json_normalize(data[1])
                print(f"Collected {len(df_events)} geopolitical events data from GDELT DOC 2.0 API.")
            else:
                print("No data returned for the given query and date range.")
                df_events = pd.DataFrame()
        elif format.upper() == 'CSV':
            from io import StringIO
            csv_data = response.content.decode('utf-8')
            df_events = pd.read_csv(StringIO(csv_data))
            print(f"Collected {len(df_events)} geopolitical events data from GDELT DOC 2.0 API.")
        else:
            print(f"Format {format} not supported in this script.")
            df_events = pd.DataFrame()

    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
        df_events = pd.DataFrame()
    except requests.exceptions.RequestException as err:
        print(f"Error: {err}")
        df_events = pd.DataFrame()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        df_events = pd.DataFrame()

    return df_events

def main():
    # Define your search parameters
    query = '"geopolitical event" OR "diplomatic relations" OR "sanctions"'
    start_date = '20230101000000'  # YYYYMMDDHHMMSS
    end_date = '20231231235959'    # YYYYMMDDHHMMSS

    # Collect geopolitical events data
    df_geopolitical = collect_geopolitical_events(
        query=query,
        start_date=start_date,
        end_date=end_date,
        mode='artlist',          # Change mode based on your needs
        max_records=250,         # Maximum allowed per request
        format='JSON'            # You can also use 'CSV', 'RSS', etc.
    )

    if not df_geopolitical.empty:
        # Process the DataFrame as needed
        # For example, select relevant columns
        relevant_columns = ['seendate', 'title', 'sourceurl', 'sourcecountry', 'sourcelang', 'tone', 'relevance']
        df_geopolitical = df_geopolitical[relevant_columns]
        # Rename columns for consistency
        df_geopolitical.rename(columns={
            'seendate': 'date',
            'sourceurl': 'url',
            'sourcecountry': 'source_country',
            'sourcelang': 'source_language'
        }, inplace=True)
        # Convert 'date' to datetime
        df_geopolitical['date'] = pd.to_datetime(df_geopolitical['date'], format='%Y%m%d%H%M%S')
        print("Processed geopolitical events data:")
        print(df_geopolitical.head())
    else:
        print("No geopolitical events data to process.")

if __name__ == '__main__':
    main()
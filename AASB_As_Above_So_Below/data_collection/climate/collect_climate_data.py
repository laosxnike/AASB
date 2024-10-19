# collect_climate_data.py

import pandas as pd
import requests
from datetime import datetime, timedelta
import time
import sys

def collect_climate_data(start_date, end_date, api_key, location, timezone='UTC'):
    """
    Collects climate and weather data from the Tomorrow.io Weather API for a single location.

    Climate patterns can affect agricultural yields, energy consumption, and infrastructure stability.
    Extreme weather events can disrupt supply chains, influence commodity prices, and impact
    insurance and reinsurance markets.

    Parameters:
    - start_date (str): The start date for data collection in 'YYYY-MM-DD' format.
    - end_date (str): The end date for data collection in 'YYYY-MM-DD' format.
    - api_key (str): Your Tomorrow.io API key.
    - location (str): The location for data collection in 'latitude,longitude' format (e.g., '37.7749,-122.4194').
    - timezone (str): The timezone for the data timestamps (default is 'UTC').

    Returns:
    - df_climate (DataFrame): A pandas DataFrame containing the climate data with 'date' and 'temperature' columns.
    """

    # Tomorrow.io Weather API endpoint for timelines
    base_url = 'https://api.tomorrow.io/v4/timelines'

    # Define the parameters for the API request
    fields = ['temperature']  # Add more fields if needed
    units = 'metric'
    timesteps = ['1d']  # Daily data

    # Initialize the DataFrame to store results
    df_list = []

    # Convert start and end dates to datetime objects
    try:
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError as ve:
        print(f"Date format error: {ve}")
        sys.exit(1)

    # Initialize the current_start for pagination
    current_start = start_dt
    delta = timedelta(days=30)  # Adjust based on Tomorrow.io's API limits

    while current_start <= end_dt:
        current_end = min(current_start + delta, end_dt)
        params = {
            'apikey': api_key,
            'location': location,
            'fields': ','.join(fields),
            'units': units,
            'timesteps': ','.join(timesteps),
            'startTime': current_start.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'endTime': current_end.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'timezone': timezone
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()

            # Navigate the JSON structure to extract temperature data
            timelines = data.get('data', {}).get('timelines', [])
            if timelines:
                for timeline in timelines:
                    intervals = timeline.get('intervals', [])
                    for interval in intervals:
                        time_str = interval.get('startTime')
                        temp = interval.get('values', {}).get('temperature')
                        if time_str and temp is not None:
                            date_obj = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%SZ').date()
                            df_list.append({
                                'date': date_obj,
                                'temperature': temp
                            })
                print(f"Collected climate data from {current_start.strftime('%Y-%m-%d')} to {current_end.strftime('%Y-%m-%d')}")
            else:
                print(f"No data available for {current_start.strftime('%Y-%m-%d')} to {current_end.strftime('%Y-%m-%d')}")

        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh}")
            print("Terminating data collection due to HTTP error.")
            break
        except requests.exceptions.RequestException as err:
            print(f"Request Exception: {err}")
            print("Terminating data collection due to request exception.")
            break
        except ValueError as ve:
            print(f"Value Error: {ve}")
            print("Terminating data collection due to value error.")
            break

        # Move to the next time period
        current_start = current_end + timedelta(seconds=1)

        # Optional: Respect API rate limits by adding a short delay
        time.sleep(1)  # Adjust the sleep duration as needed

    if df_list:
        df_climate = pd.DataFrame(df_list)
        # If multiple entries per date, average them
        df_climate = df_climate.groupby('date').mean().reset_index()
        print('Collected and processed climate data for the specified location.')
    else:
        df_climate = pd.DataFrame(columns=['date', 'temperature'])
        print('No climate data was collected for the specified location.')

    return df_climate

def collect_global_climate_data(start_date, end_date, api_key, locations, timezone='UTC'):
    """
    Collects and aggregates climate data from multiple locations to compute a global average temperature.

    Parameters:
    - start_date (str): 'YYYY-MM-DD'
    - end_date (str): 'YYYY-MM-DD'
    - api_key (str): Tomorrow.io API key
    - locations (list): List of 'latitude,longitude' strings
    - timezone (str): Timezone for data timestamps

    Returns:
    - df_global (DataFrame): DataFrame with 'date' and 'global_avg_temp'
    """
    df_list = []
    for loc in locations:
        print(f"Fetching data for location: {loc}")
        df = collect_climate_data(start_date, end_date, api_key, loc, timezone)
        if not df.empty:
            df = df.rename(columns={'temperature': f'temp_{loc.replace(",", "_")}'})
            df_list.append(df)
        else:
            print(f"No data collected for location: {loc}")

    if df_list:
        # Merge all DataFrames on 'date'
        df_merged = df_list[0]
        for df in df_list[1:]:
            df_merged = pd.merge(df_merged, df, on='date', how='outer')

        # Compute the global average temperature across all locations
        temp_columns = [col for col in df_merged.columns if col.startswith('temp_')]
        df_merged['global_avg_temp'] = df_merged[temp_columns].mean(axis=1)

        # Select only the date and global average temperature
        df_global = df_merged[['date', 'global_avg_temp']].sort_values('date').reset_index(drop=True)
        print('Collected and aggregated global climate data.')
    else:
        df_global = pd.DataFrame(columns=['date', 'global_avg_temp'])
        print('No climate data was collected for any of the specified locations.')

    return df_global

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
    START_DATE = '2023-01-01'
    END_DATE = '2023-12-31'
    API_KEY = 'UxhOUlwVDrsbIOf5lkfQTQRXazshz4DP'  # API key set directly

    # Example 1: Single Location
    SINGLE_LOCATION = '37.7749,-122.4194'  # San Francisco, CA
    print("=== Fetching Data for Single Location ===")
    single_location_df = collect_climate_data(
        start_date=START_DATE,
        end_date=END_DATE,
        api_key=API_KEY,
        location=SINGLE_LOCATION
    )
    print(single_location_df.head())
    save_to_csv(single_location_df, 'climate_data_single_location.csv')

    # Example 2: Multiple Locations for Global Average
    LOCATIONS = [
        '37.7749,-122.4194',  # San Francisco, CA
        '40.7128,-74.0060',   # New York, NY
        '51.5074,-0.1278',    # London, UK
        '35.6895,139.6917',   # Tokyo, Japan
        '-33.8688,151.2093',  # Sydney, Australia
        '55.7558,37.6176',    # Moscow, Russia
        '28.6139,77.2090',    # New Delhi, India
        '-23.5505,-46.6333',  # São Paulo, Brazil
        '1.3521,103.8198',    # Singapore
        '34.0522,-118.2437'    # Los Angeles, CA
        # Add more locations as needed
    ]
    print("\n=== Fetching Data for Multiple Locations (Global Average) ===")
    global_climate_df = collect_global_climate_data(
        start_date=START_DATE,
        end_date=END_DATE,
        api_key=API_KEY,
        locations=LOCATIONS
    )
    print(global_climate_df.head())
    save_to_csv(global_climate_df, 'climate_data_global_average.csv')
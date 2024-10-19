# collect_technology_innovations.py

import os
import requests
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any, Optional
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WorldBankAPI:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key  # If required, add API key handling
        self.indicators_base_url = 'http://api.worldbank.org/v2/country/all/indicator/{}'
        self.documents_base_url = 'https://search.worldbank.org/api/v3/wds'
        self.session = requests.Session()
        self.session.headers.update({'Accept': 'application/json'})

    def fetch_indicators(self, indicator_code: str, start_year: int, end_year: int) -> Optional[pd.DataFrame]:
        """
        Fetch data for a specific indicator from the World Bank Indicators API with pagination.

        Parameters:
        - indicator_code (str): The World Bank indicator code.
        - start_year (int): The start year for data collection.
        - end_year (int): The end year for data collection.

        Returns:
        - DataFrame containing the indicator data or None if no data is found.
        """
        url = self.indicators_base_url.format(indicator_code)
        params = {
            'date': f'{start_year}:{end_year}',
            'format': 'json',
            'per_page': 1000,  # Maximum per_page allowed
            'page': 1
        }
        all_data = []

        logging.info(f"Fetching indicator {indicator_code} from {start_year} to {end_year}")

        while True:
            try:
                response = self.session.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                if not data or len(data) < 2:
                    logging.warning(f"No data returned for indicator {indicator_code}")
                    break

                df_indicator = pd.DataFrame(data[1])
                if df_indicator.empty:
                    logging.warning(f"No data found on page {params['page']} for indicator {indicator_code}")
                    break

                all_data.append(df_indicator)
                logging.info(f"Fetched page {params['page']} with {len(df_indicator)} records for indicator {indicator_code}")

                # Check if there are more pages
                total_pages = int(data[0].get('pages', 1))
                if params['page'] >= total_pages:
                    break
                params['page'] += 1
                time.sleep(1)  # To respect API rate limits
            except requests.exceptions.RequestException as e:
                logging.error(f"Error fetching indicator {indicator_code} on page {params['page']}: {e}")
                break

        if all_data:
            df = pd.concat(all_data, ignore_index=True)
            # Keep relevant columns
            df = df[['date', 'value']]
            df.rename(columns={'date': 'year', 'value': indicator_code}, inplace=True)
            # Convert 'year' to integer and 'value' to numeric
            df['year'] = pd.to_numeric(df['year'], errors='coerce').astype('Int64')
            df[indicator_code] = pd.to_numeric(df[indicator_code], errors='coerce')
            # Group by year and calculate the mean (in case of multiple entries per year)
            df = df.groupby('year').mean().reset_index()
            logging.info(f"Collected data for indicator {indicator_code}")
            return df
        else:
            logging.warning(f"No data collected for indicator {indicator_code}")
            return None

    def fetch_documents(self, query: str, fields: List[str], start_year: int, end_year: int,
                        page_size: int = 100, max_pages: int = 10) -> Optional[pd.DataFrame]:
        """
        Fetch documents related to technological innovations using the World Bank Documents & Reports API with pagination.

        Parameters:
        - query (str): The search term related to technological innovations.
        - fields (List[str]): List of fields to retrieve for each document.
        - start_year (int): The start year for the document date.
        - end_year (int): The end year for the document date.
        - page_size (int): Number of records per page.
        - max_pages (int): Maximum number of pages to fetch.

        Returns:
        - DataFrame containing the documents data or None if no data is found.
        """
        params = {
            'format': 'json',
            'qterm': query,
            'fl': ','.join(fields),
            'rows': page_size,
            'os': 0,
            'strdate': f'{start_year}-01-01',
            'enddate': f'{end_year}-12-31',
            'sort': 'docdt',
            'order': 'asc'
        }
        all_documents = []
        current_page = 1

        logging.info(f"Fetching documents related to '{query}' from {start_year} to {end_year}")

        while current_page <= max_pages:
            try:
                response = self.session.get(self.documents_base_url, params=params)
                response.raise_for_status()
                data = response.json()

                if not data or 'results' not in data:
                    logging.warning(f"No documents found on page {current_page} for query '{query}'")
                    break

                df_docs = pd.DataFrame(data['results'])
                if df_docs.empty:
                    logging.warning(f"No documents found on page {current_page} for query '{query}'")
                    break

                all_documents.append(df_docs)
                logging.info(f"Fetched page {current_page} with {len(df_docs)} documents for query '{query}'")

                # Check if there are more pages
                if 'next_url' not in data or not data['next_url']:
                    break

                # Prepare for next page
                params['os'] += page_size
                current_page += 1
                time.sleep(1)  # To respect API rate limits
            except requests.exceptions.RequestException as e:
                logging.error(f"Error fetching documents on page {current_page}: {e}")
                break

        if all_documents:
            df_all_docs = pd.concat(all_documents, ignore_index=True)
            df_all_docs['docdt'] = pd.to_datetime(df_all_docs['docdt'], errors='coerce')
            df_all_docs.sort_values('docdt', inplace=True)
            logging.info(f"Collected a total of {len(df_all_docs)} documents related to '{query}'")
            return df_all_docs
        else:
            logging.warning(f"No documents collected for query '{query}'")
            return None

def collect_technology_innovations(start_year: int, end_year: int) -> pd.DataFrame:
    """
    Collects data on technological innovations and relevant documents from the World Bank APIs.

    Technological progress can disrupt industries, create new market opportunities,
    and render existing business models obsolete. It influences stock valuations
    of tech companies and sectors poised for growth or transformation.

    Parameters:
    - start_year (int): The start year for data collection (e.g., 2010).
    - end_year (int): The end year for data collection (e.g., 2020).

    Returns:
    - df_tech (DataFrame): A pandas DataFrame containing technology innovation indicators and document counts per year.
    """
    # Initialize the World Bank API client
    wb_api = WorldBankAPI()

    # Indicators to fetch
    indicators = {
        'IT.NET.USER.ZS': 'Internet_Users_Percentage',                  # Internet users (% of population)
        'GB.XPD.RSDV.GD.ZS': 'R&D_Expenditure_Percentage_GDP',         # Research and development expenditure (% of GDP)
        'IP.PAT.RESD': 'Patent_Applications_Residents',                # Patent applications, residents
        'IP.PAT.NRES': 'Patent_Applications_Nonresidents',             # Patent applications, nonresidents
        'TX.VAL.TECH.CD': 'High_Tech_Exports_USD',                     # High-technology exports (current US$)
    }

    # Fetch indicators data
    data_frames = []
    for indicator_code, indicator_name in indicators.items():
        df_indicator = wb_api.fetch_indicators(indicator_code, start_year, end_year)
        if df_indicator is not None:
            df_indicator.rename(columns={indicator_code: indicator_name}, inplace=True)
            data_frames.append(df_indicator)

    if data_frames:
        # Merge all indicators on 'year'
        df_tech = data_frames[0]
        for df in data_frames[1:]:
            df_tech = pd.merge(df_tech, df, on='year', how='outer')
        df_tech.sort_values('year', inplace=True)
        logging.info('Successfully collected and merged technology indicators data.')
    else:
        df_tech = pd.DataFrame(columns=['year'] + list(indicators.values()))
        logging.warning('No technology indicators data was collected.')

    # Fetch documents related to technological innovations
    # Define search query and fields
    search_query = "technology innovation OR technological innovation OR tech adoption"
    document_fields = ['docdt', 'count', 'docna', 'repnme', 'docty']

    df_documents = wb_api.fetch_documents(
        query=search_query,
        fields=document_fields,
        start_year=start_year,
        end_year=end_year,
        page_size=100,
        max_pages=20  # Adjust as needed based on expected volume
    )

    if df_documents is not None and not df_documents.empty:
        # Aggregate document counts by year
        df_documents['year'] = df_documents['docdt'].dt.year
        df_doc_counts = df_documents.groupby('year').size().reset_index(name='Document_Count')
        logging.info('Successfully collected and aggregated document data.')
        # Merge document counts with indicators
        df_tech = pd.merge(df_tech, df_doc_counts, on='year', how='left')
    else:
        df_tech['Document_Count'] = 0
        logging.warning('No documents data was collected. Document_Count set to 0 for all years.')

    # Fill NaN Document_Count with 0
    df_tech['Document_Count'] = df_tech['Document_Count'].fillna(0).astype(int)

    # Save to CSV
    output_filename = f"technology_innovations_{start_year}_{end_year}.csv"
    df_tech.to_csv(output_filename, index=False)
    logging.info(f"Saved collected data to {output_filename}")

    return df_tech

def main():
    # Define the range of years for data collection
    start_year = 2010
    end_year = 2020

    # Collect technology innovations data
    df_technology = collect_technology_innovations(start_year, end_year)

    # Display the collected data
    print("\n=== Technology Innovations Data ===")
    print(df_technology.head())

if __name__ == "__main__":
    main()
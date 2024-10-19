import pandas as pd
import os

def collect_global_consciousness_data(csv_file):
    """
    Collects and processes data from the Global Consciousness Project results CSV.

    Data capturing collective human consciousness events and related hypotheses
    are processed to observe trends or significance within the data, such as
    global deviations and Z-scores for major events.

    Parameters:
    - csv_file (str): The file path to the GCP Hypothesis Results CSV.

    Returns:
    - df_gcp (DataFrame): A pandas DataFrame containing processed GCP data.
    """

    # Check if the CSV file exists
    if not os.path.isfile(csv_file):
        print(f"The file {csv_file} does not exist.")
        return pd.DataFrame()

    try:
        # Load the CSV file
        df_gcp = pd.read_csv(csv_file)

        # Check if the required columns exist
        required_columns = ['Event', 'Timeframe', 'Z-score', 'Probability']
        if not all(col in df_gcp.columns for col in required_columns):
            print(f"The required columns {required_columns} are not present in the CSV.")
            return pd.DataFrame()

        # Convert 'Timeframe' to datetime if it's not already
        df_gcp['Timeframe'] = pd.to_datetime(df_gcp['Timeframe'], format='%Y%m%d', errors='coerce')

        # Filter out rows where 'Timeframe' could not be parsed
        df_gcp = df_gcp.dropna(subset=['Timeframe'])

        # Sort by 'Timeframe'
        df_gcp.sort_values('Timeframe', inplace=True)

        # Example processing: Calculate average Z-score and cumulative probability
        avg_z_score = df_gcp['Z-score'].mean()
        cumulative_prob = df_gcp['Probability'].sum()

        print(f"Processed {len(df_gcp)} events from GCP data.")
        print(f"Average Z-score: {avg_z_score}")
        print(f"Cumulative Probability: {cumulative_prob}")

        return df_gcp

    except Exception as e:
        print(f"Error processing the CSV file {csv_file}: {e}")
        return pd.DataFrame()

# Example usage
if __name__ == "__main__":
    # Replace 'GCP_Hypothesis_Results.csv' with the path to your actual CSV file
    csv_file = 'GCP_Hypothesis_Results.csv'
    df_gcp = collect_global_consciousness_data(csv_file)
    print(df_gcp.head())
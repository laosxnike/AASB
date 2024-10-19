# modeling/granger_causality.py

import os
import pandas as pd
import logging
from statsmodels.tsa.stattools import grangercausalitytests
from config_loader import load_config, load_secrets
import warnings

# Suppress warnings from statsmodels
warnings.filterwarnings("ignore")


def setup_logging(config):
    """
    Sets up logging based on the configuration settings.

    Args:
        config (dict): Configuration settings loaded from config.yaml.

    Returns:
        logger (logging.Logger): Configured logger instance.
    """
    logging_config = config['logging']
    logger = logging.getLogger(__name__)
    logger.setLevel(logging_config['level'])

    formatter = logging_config['formatters']['default']

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging_config['handlers']['console']['level'])
    console_handler.setFormatter(logging.Formatter(formatter))
    logger.addHandler(console_handler)

    # File Handler
    file_handler = logging.FileHandler(logging_config['handlers']['file']['filename'])
    file_handler.setLevel(logging_config['handlers']['file']['level'])
    file_handler.setFormatter(logging.Formatter(formatter))
    logger.addHandler(file_handler)

    return logger


def load_merged_data(processed_data_path, logger):
    """
    Loads the merged and preprocessed data from the specified path.

    Args:
        processed_data_path (str): Path to the processed data directory.
        logger (logging.Logger): Logger instance for logging information.

    Returns:
        df (pd.DataFrame): Merged DataFrame.
    """
    merged_file = os.path.join(processed_data_path, "merged_data.csv")
    if not os.path.exists(merged_file):
        logger.error(f"Merged data file not found at '{merged_file}'. Please run the preprocessing script first.")
        raise FileNotFoundError(f"Merged data file not found at '{merged_file}'.")

    try:
        df = pd.read_csv(merged_file)
        logger.info(f"Loaded merged data from '{merged_file}' with shape {df.shape}")
        return df
    except Exception as e:
        logger.error(f"Failed to load merged data: {e}")
        raise


def perform_granger_causality_tests(df, variables, max_lag, significance_level, logger):
    """
    Performs Granger Causality tests on the specified variables.

    Args:
        df (pd.DataFrame): Merged DataFrame containing the time series data.
        variables (list): List of variable names to test for causality.
        max_lag (int): Maximum number of lags to test.
        significance_level (float): Significance level for the tests.
        logger (logging.Logger): Logger instance for logging information.

    Returns:
        results (dict): Dictionary containing the Granger Causality test results.
    """
    results = {}
    logger.info(f"Starting Granger Causality tests with max_lag={max_lag} and significance_level={significance_level}")

    # Ensure the 'date' column is sorted
    if 'date' in df.columns:
        df = df.sort_values('date')
        df.reset_index(drop=True, inplace=True)
        logger.debug("Sorted DataFrame by 'date' column")
    else:
        logger.warning("No 'date' column found. Proceeding without date sorting.")

    # Iterate over all possible pairs
    for caused in variables:
        for causing in variables:
            if caused == causing:
                continue  # Skip self-causality

            test_pair = [caused, causing]
            logger.info(f"Testing if '{causing}' Granger-causes '{caused}'")

            try:
                test_result = grangercausalitytests(df[test_pair].dropna(), maxlag=max_lag, verbose=False)
                p_values = [round(test_result[i+1][0]['ssr_ftest'][1], 4) for i in range(max_lag)]
                min_p_value = min(p_values)

                causality = 'Yes' if min_p_value < significance_level else 'No'
                results[(causing, caused)] = {
                    'p_values': p_values,
                    'min_p_value': min_p_value,
                    'causality': causality
                }

                logger.info(f"Granger Causality Result: {causing} -> {caused} | Min p-value: {min_p_value} | Causality: {causality}")
            except Exception as e:
                logger.error(f"Failed to perform Granger Causality test for {causing} -> {caused}: {e}")
                results[(causing, caused)] = {
                    'p_values': [],
                    'min_p_value': None,
                    'causality': 'Error'
                }

    return results


def save_granger_results(results, output_path, logger):
    """
    Saves the Granger Causality test results to a CSV file.

    Args:
        results (dict): Dictionary containing the Granger Causality test results.
        output_path (str): Path to save the results CSV.
        logger (logging.Logger): Logger instance for logging information.
    """
    logger.info(f"Saving Granger Causality results to '{output_path}'")
    try:
        records = []
        for (causing, caused), result in results.items():
            record = {
                'Causing': causing,
                'Caused': caused,
                'Causality': result['causality'],
                'Min_p_value': result['min_p_value']
            }
            record.update({f'p_value_lag_{i+1}': p for i, p in enumerate(result['p_values'])})
            records.append(record)

        results_df = pd.DataFrame(records)
        results_df.to_csv(output_path, index=False)
        logger.info(f"Granger Causality results saved successfully to '{output_path}'")
    except Exception as e:
        logger.error(f"Failed to save Granger Causality results: {e}")
        raise


def main():
    # Load configuration
    config = load_config()

    # Set up logging
    logger = setup_logging(config)
    logger.info("Starting Granger Causality Analysis")

    # Paths
    processed_data_path = config['paths']['data_processed']
    modeling_output_path = os.path.join(config['paths']['models'])
    os.makedirs(modeling_output_path, exist_ok=True)
    logger.debug(f"Ensured that modeling output directory '{modeling_output_path}' exists")

    # Load merged data
    try:
        df = load_merged_data(processed_data_path, logger)
    except FileNotFoundError as e:
        logger.critical(e)
        return
    except Exception as e:
        logger.critical(f"An unexpected error occurred while loading data: {e}")
        return

    # Retrieve modeling parameters from config
    modeling_config = config['modeling']
    granger_config = modeling_config['granger_causality']
    variables = granger_config.get('variables', [])
    max_lag = granger_config.get('max_lag', 5)
    significance_level = granger_config.get('significance_level', 0.05)

    if not variables:
        logger.error("No variables specified for Granger Causality tests. Please update config.yaml.")
        return

    # Perform Granger Causality Tests
    results = perform_granger_causality_tests(df, variables, max_lag, significance_level, logger)

    # Save Results
    output_file = os.path.join(modeling_output_path, "granger_causality_results.csv")
    try:
        save_granger_results(results, output_file, logger)
    except Exception as e:
        logger.error(f"An error occurred while saving Granger Causality results: {e}")

    logger.info("Granger Causality Analysis completed successfully")


if __name__ == "__main__":
    main()

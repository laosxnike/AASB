# modeling/var_models.py

import os
import pandas as pd
import logging
from statsmodels.tsa.api import VAR
from statsmodels.tsa.stattools import adfuller
from config_loader import load_config
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


def test_stationarity(series, significance_level=0.05):
    """
    Performs the Augmented Dickey-Fuller test to check stationarity of a time series.

    Args:
        series (pd.Series): Time series data.
        significance_level (float): Significance level for the test.

    Returns:
        is_stationary (bool): True if series is stationary, False otherwise.
    """
    result = adfuller(series.dropna())
    p_value = result[1]
    return p_value < significance_level


def make_stationary(df, variables, var_config, logger):
    """
    Ensures that all specified variables are stationary by differencing if necessary.

    Args:
        df (pd.DataFrame): DataFrame containing the time series data.
        variables (list): List of variable names to check for stationarity.
        var_config (dict): VAR modeling configuration settings.
        logger (logging.Logger): Logger instance for logging information.

    Returns:
        df (pd.DataFrame): DataFrame with stationary variables.
    """
    differencing = var_config.get('differencing', 1)
    significance_level = var_config.get('significance_level', 0.05)

    for var in variables:
        if var not in df.columns:
            logger.warning(f"Variable '{var}' not found in DataFrame. Skipping stationarity test.")
            continue

        is_stationary = test_stationarity(df[var], significance_level)
        logger.debug(f"Stationarity test for '{var}': {'Stationary' if is_stationary else 'Non-Stationary'}")

        if not is_stationary:
            logger.info(f"Variable '{var}' is non-stationary. Applying differencing (order={differencing}).")
            df[var] = df[var].diff(differencing)
            # Re-test stationarity after differencing
            is_stationary = test_stationarity(df[var], significance_level)
            if is_stationary:
                logger.info(f"Variable '{var}' is now stationary after differencing.")
            else:
                logger.warning(f"Variable '{var}' remains non-stationary after differencing.")
    return df


def select_optimal_lag(df, max_lag, logger):
    """
    Selects the optimal lag order for the VAR model based on criteria like AIC.

    Args:
        df (pd.DataFrame): DataFrame containing the time series data.
        max_lag (int): Maximum number of lags to consider.
        logger (logging.Logger): Logger instance for logging information.

    Returns:
        selected_lag (int): Optimal number of lags selected.
    """
    model = VAR(df)
    results = model.select_order(maxlags=max_lag)
    selected_lag = results.aic

    if pd.isna(selected_lag):
        selected_lag = 1
        logger.warning("AIC selection returned NaN. Defaulting to lag 1.")
    else:
        selected_lag = results.aic
        logger.info(f"Optimal lag order selected based on AIC: {selected_lag}")
    return selected_lag


def fit_var_model(df, selected_lag, logger):
    """
    Fits the VAR model with the selected lag order.

    Args:
        df (pd.DataFrame): DataFrame containing the time series data.
        selected_lag (int): Number of lags to include in the model.
        logger (logging.Logger): Logger instance for logging information.

    Returns:
        var_model (VARResults): Fitted VAR model results.
    """
    model = VAR(df)
    var_model = model.fit(selected_lag)
    logger.info(f"Fitted VAR model with lag order {selected_lag}")
    logger.debug(var_model.summary())
    return var_model


def save_var_summary(var_model, output_path, logger):
    """
    Saves the VAR model summary to a text file.

    Args:
        var_model (VARResults): Fitted VAR model results.
        output_path (str): Path to save the summary file.
        logger (logging.Logger): Logger instance for logging information.
    """
    logger.info(f"Saving VAR model summary to '{output_path}'")
    try:
        with open(output_path, 'w') as f:
            f.write(var_model.summary().as_text())
        logger.info(f"VAR model summary saved successfully to '{output_path}'")
    except Exception as e:
        logger.error(f"Failed to save VAR model summary: {e}")
        raise


def save_irf(var_model, steps, output_path, logger):
    """
    Saves the Impulse Response Function (IRF) results to a CSV file.

    Args:
        var_model (VARResults): Fitted VAR model results.
        steps (int): Number of steps ahead for IRF.
        output_path (str): Path to save the IRF CSV file.
        logger (logging.Logger): Logger instance for logging information.
    """
    logger.info(f"Generating and saving Impulse Response Function (IRF) for {steps} steps ahead")
    try:
        irf = var_model.irf(steps)
        irf_df = irf.irfs
        irf_df.to_csv(output_path)
        logger.info(f"IRF results saved successfully to '{output_path}'")
    except Exception as e:
        logger.error(f"Failed to generate/save IRF: {e}")
        raise


def save_forecast(var_model, steps, df, output_path, logger):
    """
    Saves the forecasted values from the VAR model to a CSV file.

    Args:
        var_model (VARResults): Fitted VAR model results.
        steps (int): Number of steps ahead to forecast.
        df (pd.DataFrame): Original DataFrame containing the 'date' column.
        output_path (str): Path to save the forecast CSV file.
        logger (logging.Logger): Logger instance for logging information.
    """
    logger.info(f"Generating and saving forecasts for {steps} steps ahead")
    try:
        forecast = var_model.forecast(var_model.y, steps=steps)
        forecast_df = pd.DataFrame(forecast, columns=var_model.names)
        # Ensure 'date' column is in datetime format
        if 'date' in df.columns:
            last_date = pd.to_datetime(df['date'].iloc[-1])
            forecast_dates = pd.date_range(start=last_date, periods=steps + 1, freq='D')[1:]
            forecast_df['forecast_date'] = forecast_dates
            forecast_df = forecast_df[['forecast_date'] + var_model.names]
        else:
            # If no 'date' column, use integer index
            forecast_df.reset_index(drop=True, inplace=True)
        forecast_df.to_csv(output_path, index=False)
        logger.info(f"Forecast results saved successfully to '{output_path}'")
    except Exception as e:
        logger.error(f"Failed to generate/save forecasts: {e}")
        raise


def main():
    # Load configuration
    config = load_config()

    # Set up logging
    logger = setup_logging(config)
    logger.info("Starting VAR Model Analysis")

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
    var_config = modeling_config['var_models']
    variables = var_config.get('variables', [])
    max_lag = var_config.get('max_lag', 5)
    significance_level = var_config.get('significance_level', 0.05)
    test_stationarity_flag = var_config.get('test_stationarity', True)
    differencing = var_config.get('differencing', 1)

    if not variables:
        logger.error("No variables specified for VAR modeling. Please update config.yaml.")
        return

    # Ensure stationarity if required
    if test_stationarity_flag:
        logger.info("Checking and ensuring stationarity of variables")
        df = make_stationary(df, variables, var_config, logger)
    else:
        logger.info("Skipping stationarity tests as per configuration")

    # Drop rows with NaN values resulting from differencing
    df = df.dropna()
    logger.debug(f"DataFrame shape after dropping NaNs: {df.shape}")

    # Select optimal lag
    selected_lag = select_optimal_lag(df, max_lag, logger)

    # Fit VAR model
    try:
        var_model = fit_var_model(df, selected_lag, logger)
    except Exception as e:
        logger.critical(f"Failed to fit VAR model: {e}")
        return

    # Save VAR model summary
    summary_output = os.path.join(modeling_output_path, "var_model_summary.txt")
    try:
        save_var_summary(var_model, summary_output, logger)
    except Exception as e:
        logger.error(f"An error occurred while saving VAR model summary: {e}")

    # Generate and save Impulse Response Function (IRF)
    irf_steps = var_config.get('irf_steps', 10)
    irf_output = os.path.join(modeling_output_path, f"irf_{irf_steps}_steps.csv")
    try:
        save_irf(var_model, irf_steps, irf_output, logger)
    except Exception as e:
        logger.error(f"An error occurred while saving IRF results: {e}")

    # Generate and save Forecasts
    forecast_steps = var_config.get('forecast_steps', 5)
    forecast_output = os.path.join(modeling_output_path, f"forecast_{forecast_steps}_steps.csv")
    try:
        save_forecast(var_model, forecast_steps, df, forecast_output, logger)
    except Exception as e:
        logger.error(f"An error occurred while saving forecast results: {e}")

    logger.info("VAR Model Analysis completed successfully")


if __name__ == "__main__":
    main()

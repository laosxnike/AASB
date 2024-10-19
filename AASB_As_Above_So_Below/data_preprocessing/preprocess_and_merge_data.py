# data_preprocessing/preprocess_and_merge_data.py

import os
import glob
import pandas as pd
import logging
from config_loader import load_config

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

def load_datasets(raw_data_path, logger):
    """
    Loads all CSV datasets from the specified raw data directory.
    
    Args:
        raw_data_path (str): Path to the raw data directory.
        logger (logging.Logger): Logger instance for logging information.
        
    Returns:
        dataframes (dict): Dictionary of DataFrames keyed by dataset name.
    """
    dataframes = {}
    csv_files = glob.glob(os.path.join(raw_data_path, "*.csv"))
    logger.info(f"Found {len(csv_files)} CSV files in {raw_data_path}")
    
    for file in csv_files:
        try:
            dataset_name = os.path.splitext(os.path.basename(file))[0]
            df = pd.read_csv(file)
            logger.info(f"Loaded dataset '{dataset_name}' with {df.shape[0]} records and {df.shape[1]} columns")
            dataframes[dataset_name] = df
        except Exception as e:
            logger.error(f"Failed to load {file}: {e}")
    
    return dataframes

def preprocess_dataset(df, dataset_name, config, logger):
    """
    Preprocesses a single dataset: handles missing data, normalizes, and formats dates.
    
    Args:
        df (pd.DataFrame): DataFrame to preprocess.
        dataset_name (str): Name of the dataset.
        config (dict): Configuration settings.
        logger (logging.Logger): Logger instance for logging information.
        
    Returns:
        df (pd.DataFrame): Preprocessed DataFrame.
    """
    preprocessing_config = config['data_preprocessing']
    
    # Handle missing data
    missing_handling = preprocessing_config['missing_data_handling']
    fill_values = preprocessing_config.get('fill_values', {})
    
    logger.debug(f"Preprocessing dataset '{dataset_name}': Handling missing data with strategy '{missing_handling}'")
    
    if missing_handling == 'drop':
        df = df.dropna()
        logger.debug(f"Dropped rows with missing data. New shape: {df.shape}")
    elif missing_handling == 'fill':
        # Fill numeric columns with specified value or default
        numeric_fill = fill_values.get('numeric', 0)
        categorical_fill = fill_values.get('categorical', 'Unknown')
        
        for column in df.select_dtypes(include=['number']).columns:
            df[column].fillna(numeric_fill, inplace=True)
            logger.debug(f"Filled missing numeric values in '{column}' with {numeric_fill}")
        
        for column in df.select_dtypes(include=['object', 'category']).columns:
            df[column].fillna(categorical_fill, inplace=True)
            logger.debug(f"Filled missing categorical values in '{column}' with '{categorical_fill}'")
    elif missing_handling == 'interpolate':
        df = df.interpolate()
        logger.debug(f"Interpolated missing values. New shape: {df.shape}")
    else:
        logger.warning(f"Unknown missing data handling strategy: '{missing_handling}'. No action taken.")
    
    # Format date columns
    date_format = preprocessing_config.get('date_format', "%Y-%m-%d")
    # Assuming there's a 'date' column; adjust as necessary
    if 'date' in df.columns:
        try:
            df['date'] = pd.to_datetime(df['date']).dt.strftime(date_format)
            logger.debug(f"Formatted 'date' column to '{date_format}'")
        except Exception as e:
            logger.error(f"Failed to format 'date' column in '{dataset_name}': {e}")
    else:
        logger.warning(f"No 'date' column found in '{dataset_name}'. Skipping date formatting.")
    
    # Normalization
    normalization_config = preprocessing_config.get('normalization', {})
    method = normalization_config.get('method', 'min-max')
    range_vals = normalization_config.get('range', [0, 1])
    
    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
    logger.debug(f"Normalizing numeric columns: {numeric_columns} using method '{method}'")
    
    if method == 'min-max':
        for column in numeric_columns:
            min_val = df[column].min()
            max_val = df[column].max()
            if max_val - min_val != 0:
                df[column] = (df[column] - min_val) / (max_val - min_val) * (range_vals[1] - range_vals[0]) + range_vals[0]
                logger.debug(f"Applied min-max normalization to '{column}'")
            else:
                df[column] = range_vals[0]
                logger.debug(f"Set '{column}' to {range_vals[0]} due to zero variance")
    elif method == 'z-score':
        for column in numeric_columns:
            mean = df[column].mean()
            std = df[column].std()
            if std != 0:
                df[column] = (df[column] - mean) / std
                logger.debug(f"Applied z-score normalization to '{column}'")
            else:
                df[column] = 0
                logger.debug(f"Set '{column}' to 0 due to zero standard deviation")
    else:
        logger.warning(f"Unknown normalization method: '{method}'. Skipping normalization.")
    
    return df

def merge_datasets(dataframes, config, logger):
    """
    Merges multiple DataFrames into a single consolidated DataFrame.
    
    Args:
        dataframes (dict): Dictionary of DataFrames to merge.
        config (dict): Configuration settings.
        logger (logging.Logger): Logger instance for logging information.
        
    Returns:
        merged_df (pd.DataFrame): Merged DataFrame.
    """
    merge_strategy = config['data_preprocessing']['merge_strategy']
    logger.info(f"Merging datasets using '{merge_strategy}' strategy")
    
    # Identify the key for merging; assuming 'date' is the common key
    key = 'date'
    for df_name, df in dataframes.items():
        if key not in df.columns:
            logger.error(f"Dataset '{df_name}' does not contain the key '{key}'. Cannot proceed with merging.")
            raise KeyError(f"Missing key '{key}' in dataset '{df_name}'")
    
    # Start merging
    merged_df = None
    for df_name, df in dataframes.items():
        if merged_df is None:
            merged_df = df
            logger.debug(f"Initialized merged DataFrame with '{df_name}'")
        else:
            merged_df = pd.merge(merged_df, df, on=key, how=merge_strategy, suffixes=('', f'_{df_name}'))
            logger.debug(f"Merged '{df_name}' into the consolidated DataFrame")
    
    logger.info(f"Final merged DataFrame shape: {merged_df.shape}")
    return merged_df

def main():
    # Load configuration
    config = load_config()
    
    # Set up logging
    logger = setup_logging(config)
    logger.info("Starting data preprocessing and merging process")
    
    # Paths
    raw_data_path = config['paths']['data_raw']
    processed_data_path = config['paths']['data_processed']
    
    # Ensure processed data directory exists
    os.makedirs(processed_data_path, exist_ok=True)
    logger.debug(f"Ensured that processed data directory '{processed_data_path}' exists")
    
    # Load datasets
    dataframes = load_datasets(raw_data_path, logger)
    
    # Preprocess each dataset
    for dataset_name, df in dataframes.items():
        logger.info(f"Preprocessing dataset '{dataset_name}'")
        preprocessed_df = preprocess_dataset(df, dataset_name, config, logger)
        dataframes[dataset_name] = preprocessed_df
        logger.info(f"Completed preprocessing for '{dataset_name}'")
    
    # Merge datasets
    try:
        merged_df = merge_datasets(dataframes, config, logger)
    except KeyError as e:
        logger.critical(f"Merging failed: {e}")
        return
    
    # Save the merged DataFrame
    output_file = os.path.join(processed_data_path, "merged_data.csv")
    try:
        merged_df.to_csv(output_file, index=False)
        logger.info(f"Saved merged data to '{output_file}'")
    except Exception as e:
        logger.error(f"Failed to save merged data to '{output_file}': {e}")
    
    logger.info("Data preprocessing and merging process completed successfully")

if __name__ == "__main__":
    main()

# main.py

import argparse
import logging
import logging.config
import sys
import yaml
import os

from scripts.run_data_collection import run_data_collection
from scripts.run_preprocessing import run_preprocessing
from scripts.run_modeling import run_modeling
from scripts.run_visualization import run_visualization

def setup_logging(config_path='config/config.yaml'):
    """
    Sets up logging based on the provided configuration file.

    Parameters:
    - config_path (str): Path to the logging configuration YAML file.
    """
    if not os.path.exists(config_path):
        print(f"Logging configuration file '{config_path}' not found.")
        sys.exit(1)
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    logging.config.dictConfig(config['logging'])
    logging.info("Logging has been configured successfully.")

def load_secrets(secrets_path='config/secrets.yaml'):
    """
    Loads secrets (e.g., API keys) from the secrets configuration file.

    Parameters:
    - secrets_path (str): Path to the secrets YAML file.

    Returns:
    - dict: A dictionary containing the loaded secrets.
    """
    if not os.path.exists(secrets_path):
        logging.error(f"Secrets file '{secrets_path}' not found.")
        sys.exit(1)
    
    with open(secrets_path, 'r') as f:
        secrets = yaml.safe_load(f)
    
    logging.info("Secrets have been loaded successfully.")
    return secrets

def main():
    """
    The main function that orchestrates the execution of different stages
    of the data pipeline based on user-provided command-line arguments.
    """
    # Initialize argument parser
    parser = argparse.ArgumentParser(description="AASB: As Above So Below - Pipeline Orchestrator")
    
    # Define command-line arguments
    parser.add_argument(
        '--stage',
        type=str,
        nargs='+',
        choices=['collect', 'preprocess', 'model', 'visualize', 'all'],
        default=['all'],
        help="Stages to run: 'collect', 'preprocess', 'model', 'visualize', or 'all' (default)."
    )
    parser.add_argument(
        '--config',
        type=str,
        default='config/config.yaml',
        help="Path to the logging configuration YAML file (default: 'config/config.yaml')."
    )
    parser.add_argument(
        '--secrets',
        type=str,
        default='config/secrets.yaml',
        help="Path to the secrets YAML file containing API keys (default: 'config/secrets.yaml')."
    )
    
    # Parse command-line arguments
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.config)
    logger = logging.getLogger(__name__)
    
    # Load secrets
    secrets = load_secrets(args.secrets)
    
    # Determine which stages to run
    stages = args.stage
    if 'all' in stages:
        stages = ['collect', 'preprocess', 'model', 'visualize']
    
    logger.info(f"Pipeline initiation with stages: {', '.join(stages)}")
    
    try:
        # Execute Data Collection Stage
        if 'collect' in stages:
            logger.info("Starting Data Collection Stage...")
            run_data_collection(secrets)
            logger.info("Data Collection Stage Completed Successfully.")
        
        # Execute Data Preprocessing Stage
        if 'preprocess' in stages:
            logger.info("Starting Data Preprocessing Stage...")
            run_preprocessing()
            logger.info("Data Preprocessing Stage Completed Successfully.")
        
        # Execute Modeling Stage
        if 'model' in stages:
            logger.info("Starting Modeling Stage...")
            run_modeling()
            logger.info("Modeling Stage Completed Successfully.")
        
        # Execute Visualization Stage
        if 'visualize' in stages:
            logger.info("Starting Visualization Stage...")
            run_visualization()
            logger.info("Visualization Stage Completed Successfully.")
        
        logger.info("All requested pipeline stages have been executed successfully.")
    
    except Exception as e:
        logger.exception(f"An error occurred during pipeline execution: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

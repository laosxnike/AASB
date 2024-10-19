# config_loader.py

import yaml
import os
from dotenv import load_dotenv

def load_yaml(file_path):
    """
    Loads a YAML file and returns its content as a dictionary.

    Args:
        file_path (str): Path to the YAML file.

    Returns:
        dict: Parsed YAML content.
    """
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def load_config(config_path="config/config.yaml"):
    """
    Loads the main configuration file.

    Args:
        config_path (str): Path to config.yaml.

    Returns:
        dict: Configuration settings.
    """
    return load_yaml(config_path)

def load_secrets(secrets_path="config/secrets.yaml"):
    """
    Loads the secrets configuration file.

    Args:
        secrets_path (str): Path to secrets.yaml.

    Returns:
        dict: Secrets and sensitive information.

    Raises:
        FileNotFoundError: If secrets.yaml does not exist.
    """
    if not os.path.exists(secrets_path):
        raise FileNotFoundError(f"Secrets file not found at {secrets_path}")
    return load_yaml(secrets_path)

# Optional: Load environment variables from a .env file
load_dotenv()

# Example of accessing configuration and secrets
if __name__ == "__main__":
    try:
        config = load_config()
        secrets = load_secrets()
        print("Configuration and secrets loaded successfully.")
    except FileNotFoundError as e:
        print(e)

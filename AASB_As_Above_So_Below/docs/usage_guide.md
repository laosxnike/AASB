AASB: As Above So Below - Usage Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Project Structure](#project-structure)
6. [Running the Project](#running-the-project)
    - [1. Data Collection](#1-data-collection)
    - [2. Data Preprocessing](#2-data-preprocessing)
    - [3. Modeling](#3-modeling)
    - [4. Visualization](#4-visualization)
7. [Using the Dash Application](#using-the-dash-application)
8. [Running Tests](#running-tests)
9. [Logging](#logging)
10. [Troubleshooting](#troubleshooting)
11. [Additional Resources](#additional-resources)

---

## Introduction

Welcome to the **AASB: As Above So Below** project! This guide is designed to help you set up, configure, and operate the project efficiently. Whether you're a new contributor or an existing team member, this guide provides the necessary steps to get you started and ensure smooth workflow management.

## Prerequisites

Before you begin, ensure that your development environment meets the following requirements:

- **Operating System:** macOS, Linux, or Windows
- **Python Version:** 3.11
- **Package Manager:** `pip` (included with Python) and `Homebrew` (optional for macOS users)
- **Git:** For version control
- **Docker:** (Optional) For containerization

## Installation

Follow these steps to set up the project on your local machine.

### 1. Clone the Repository

First, clone the project repository to your local machine:

```bash
git clone https://github.com/yourusername/AASB_As_Above_So_Below.git
cd AASB_As_Above_So_Below
```

### 2. Set Up a Virtual Environment

Creating a virtual environment isolates project dependencies and prevents conflicts with other projects.

#### Using `venv` (Python's Built-in Module)

```bash
python3.11 -m venv .venv
```

#### Activate the Virtual Environment

- **macOS/Linux:**

  ```bash
  source .venv/bin/activate
  ```

- **Windows:**

  ```bash
  .venv\Scripts\activate
  ```

### 3. Install Dependencies

With the virtual environment activated, install the required Python packages:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

*Note: Ensure that `requirements.txt` is up-to-date with all necessary packages.*

### 4. (Optional) Install Docker

If you plan to use Docker for containerization, follow the installation instructions for your operating system:

- **macOS:** Install via Homebrew

  ```bash
  brew install --cask docker
  ```

- **Windows/Linux:** Download Docker from the [official website](https://www.docker.com/get-started) and follow the installation guide.

## Configuration

Proper configuration ensures that the project can access necessary APIs and settings. Follow these steps to configure the project.

### 1. Create a `.env` File

The `.env` file stores environment variables, including API keys. Create a `.env` file in the project's root directory:

```bash
touch .env
```

### 2. Populate `secrets.yaml`

Add your API keys and other sensitive information to the `config/secrets.yaml` file. Ensure this file is **never** committed to version control.

```yaml
# config/secrets.yaml

api_keys:
  forex_api: YOUR_FOREX_API_KEY
  bond_yields_api: YOUR_BOND_YIELDS_API_KEY
  climate_api: YOUR_CLIMATE_API_KEY
  commodities_api: YOUR_COMMODITIES_API_KEY
  cultural_trends_api: YOUR_CULTURAL_TRENDS_API_KEY
  derivatives_api: YOUR_DERIVATIVES_API_KEY
  geopolitical_events_api: YOUR_GEOPOLITICAL_EVENTS_API_KEY
  global_consciousness_api: YOUR_GLOBAL_CONSCIOUSNESS_API_KEY
  interest_rates_api: YOUR_INTEREST_RATES_API_KEY
  social_media_api: YOUR_SOCIAL_MEDIA_API_KEY
  stock_indices_api: YOUR_STOCK_INDICES_API_KEY
  technology_innovations_api: YOUR_TECHNOLOGY_INNOVATIONS_API_KEY
```

*Replace `YOUR_*_API_KEY` with your actual API keys.*

### 3. Update `.gitignore`

Ensure that sensitive files are excluded from version control by verifying the `.gitignore` file includes:

```gitignore
# .gitignore

# Virtual environment
.venv/
venv/
ENV/
env/

# Python cache
__pycache__/
*.pyc
*.pyo
*.pyd

# Logs
logs/

# Data files
data/raw/
data/interim/
data/external/
data/processed/

# Secrets
config/secrets.yaml

# Environment variables
.env

# Jupyter Notebook checkpoints
.ipynb_checkpoints/

# IDEs and editors
.vscode/
.idea/
*.swp
```

## Project Structure

Understanding the directory structure is crucial for navigating and managing the project. Below is an overview of the enhanced directory structure:

```
AASB_As_Above_So_Below/
├── README.md
├── main.py
├── requirements.txt
├── config/
│   ├── config.yaml
│   └── secrets.yaml
├── data/
│   ├── raw/
│   │   ├── aggregate_bars.csv
│   │   ├── market_holidays.csv
│   │   ├── ema.csv
│   │   ├── rsi.csv
│   │   ├── gainers.csv
│   │   ├── sma.csv
│   │   ├── grouped_daily_bars.csv
│   │   ├── stock_indices_2010-01-01_to_2020-12-31.csv
│   │   ├── losers.csv
│   │   └── macd.csv
│   ├── processed/
│   │   └── GCP_Hypothesis_Results.csv
│   ├── external/
│   │   └── # External API data
│   └── interim/
│       └── # Temporary processing files
├── data_collection/
│   ├── __init__.py
│   ├── forex/
│   │   ├── __init__.py
│   │   └── collect_forex_data.py
│   ├── bond_yields/
│   │   ├── __init__.py
│   │   └── collect_bond_yields.py
│   ├── climate/
│   │   ├── __init__.py
│   │   └── collect_climate_data.py
│   ├── commodities/
│   │   ├── __init__.py
│   │   └── collect_commodity_prices.py
│   ├── cultural_trends/
│   │   ├── __init__.py
│   │   └── collect_cultural_trends.py
│   ├── derivatives/
│   │   ├── __init__.py
│   │   └── collect_derivatives_data.py
│   ├── geopolitical_events/
│   │   ├── __init__.py
│   │   └── collect_geopolitical_events.py
│   ├── global_consciousness/
│   │   ├── __init__.py
│   │   └── collect_global_consciousness_data.py
│   ├── interest_rates/
│   │   ├── __init__.py
│   │   └── collect_interest_rates.py
│   ├── social_media/
│   │   ├── __init__.py
│   │   └── collect_social_media_data.py
│   ├── stock_indices/
│   │   ├── __init__.py
│   │   └── collect_stock_indices.py
│   └── technology_innovations/
│       ├── __init__.py
│       └── collect_technology_innovations.py
├── data_preprocessing/
│   ├── __init__.py
│   ├── preprocess_and_merge_data.py
│   └── __pycache__/
├── modeling/
│   ├── __init__.py
│   ├── var_models.py
│   ├── granger_causality.py
│   └── __pycache__/
├── visualization/
│   ├── __init__.py
│   ├── visualize_recursive_graph.py
│   └── __pycache__/
├── scripts/
│   ├── run_data_collection.py
│   ├── run_preprocessing.py
│   ├── run_modeling.py
│   └── run_visualization.py
├── notebooks/
│   ├── EDA.ipynb
│   ├── VAR_Modeling.ipynb
│   └── Visualization_Prototyping.ipynb
├── tests/
│   ├── __init__.py
│   ├── test_collect_forex_data.py
│   ├── test_collect_bond_yields.py
│   ├── test_preprocess_and_merge_data.py
│   ├── test_model_relationships.py
│   └── test_visualize_recursive_graph.py
├── logs/
│   ├── data_collection.log
│   ├── data_preprocessing.log
│   ├── modeling.log
│   └── visualization.log
├── docs/
│   ├── architecture.md
│   ├── usage_guide.md
│   └── api_documentation.md
├── .gitignore
└── Dockerfile
```

*Note: Refer to `architecture.md` for a detailed explanation of each component.*

## Running the Project

The project follows a modular pipeline consisting of data collection, preprocessing, modeling, and visualization stages. Each stage can be executed independently or as part of the entire pipeline using the provided scripts.

### 1. Data Collection

**Purpose:** Fetches data from various APIs and sources, storing raw data for preprocessing.

**Script:** `scripts/run_data_collection.py`

**Usage:**

```bash
python scripts/run_data_collection.py
```

**Steps:**

1. **Activate the Virtual Environment:**

   ```bash
   source .venv/bin/activate  # macOS/Linux
   # or
   .venv\Scripts\activate     # Windows
   ```

2. **Run the Data Collection Script:**

   ```bash
   python scripts/run_data_collection.py
   ```

**What It Does:**

- Loads API keys from `config/secrets.yaml`.
- Executes all data collection modules in parallel using `joblib`.
- Saves collected raw data into the `data/raw/` directory.
- Logs the data collection process in `logs/data_collection.log`.

### 2. Data Preprocessing

**Purpose:** Cleans, transforms, and merges raw data to prepare it for modeling.

**Script:** `scripts/run_preprocessing.py`

**Usage:**

```bash
python scripts/run_preprocessing.py
```

**Steps:**

1. **Ensure Raw Data Exists:**

   - Verify that data has been collected and stored in `data/raw/` by running the data collection script.

2. **Run the Data Preprocessing Script:**

   ```bash
   python scripts/run_preprocessing.py
   ```

**What It Does:**

- Reads raw data files from `data/raw/`.
- Cleans and transforms the data (e.g., handling missing values, normalizing).
- Merges data from different sources into a cohesive dataset.
- Saves the processed data into `data/processed/`.
- Logs the preprocessing steps in `logs/data_preprocessing.log`.

### 3. Modeling

**Purpose:** Applies statistical and machine learning models to analyze and uncover relationships within the data.

**Script:** `scripts/run_modeling.py`

**Usage:**

```bash
python scripts/run_modeling.py
```

**Steps:**

1. **Ensure Preprocessed Data Exists:**

   - Verify that data has been preprocessed and saved in `data/processed/` by running the preprocessing script.

2. **Run the Modeling Script:**

   ```bash
   python scripts/run_modeling.py
   ```

**What It Does:**

- Loads processed data from `data/processed/`.
- Fits Vector Autoregression (VAR) models using `modeling/var_models.py`.
- Performs Granger Causality tests using `modeling/granger_causality.py`.
- Saves model results and insights.
- Logs the modeling process in `logs/modeling.log`.

### 4. Visualization

**Purpose:** Generates interactive visualizations to explore and present the modeled data.

**Script:** `scripts/run_visualization.py`

**Usage:**

```bash
python scripts/run_visualization.py
```

**Steps:**

1. **Ensure Modeling Results Exist:**

   - Verify that modeling has been completed and results are available.

2. **Run the Visualization Script:**

   ```bash
   python scripts/run_visualization.py
   ```

**What It Does:**

- Loads modeling results.
- Generates recursive Ramsey graphs using `visualization/visualize_recursive_graph.py`.
- Launches the Dash application for interactive visualization.
- Logs the visualization process in `logs/visualization.log`.

## Using the Dash Application

The Dash application provides an interactive dashboard to explore the relationships and patterns identified through modeling. Follow these steps to access and use the dashboard.

### 1. Launch the Dash Application

After running the visualization script, the Dash app will start and provide a local URL (e.g., `http://127.0.0.1:8050/`). Open this URL in your web browser to access the dashboard.

### 2. Navigating the Dashboard

- **Graph Visualization:**
  - Explore the recursive Ramsey graphs representing relationships within financial markets.
  - Click on nodes to zoom into specific sub-universes and view detailed relationships.
  
- **Interactive Controls:**
  - Use sliders, dropdowns, and other interactive elements to filter and customize the visualization based on criteria like correlation thresholds, time frames, and data categories.
  
- **Details Panel:**
  - View detailed information about selected nodes, including underlying data and model insights.

### 3. Customizing Visualizations

- **Adjust Parameters:**
  - Modify parameters such as correlation thresholds directly within the dashboard to dynamically update the visualizations.
  
- **Exporting Data:**
  - Export visualization data or snapshots for reporting and further analysis.

### 4. Stopping the Dash Application

To stop the Dash server, press `Ctrl+C` in the terminal where the visualization script is running.

## Running Tests

Testing ensures that each component of the project functions as intended. Follow these steps to run unit tests.

### 1. Ensure Dependencies are Installed

Make sure all testing dependencies are installed via `requirements.txt`.

### 2. Run Tests Using `pytest`

With the virtual environment activated, execute the tests:

```bash
pytest
```

*Alternatively, you can run specific test modules:*

```bash
pytest tests/test_collect_forex_data.py
```

### 3. Reviewing Test Results

- **Successful Tests:** Indicated by green dots and `PASSED` statuses.
- **Failed Tests:** Indicated by red `F` characters and detailed error messages.

### 4. Adding New Tests

- Create new test files in the `tests/` directory following the naming convention `test_<module_name>.py`.
- Write test cases using `unittest` or `pytest` frameworks to cover various functionalities and edge cases.

## Logging

Logging provides insights into the application's behavior and aids in debugging.

### 1. Log Files

Log files are stored in the `logs/` directory:

- `data_collection.log`: Logs related to data collection processes.
- `data_preprocessing.log`: Logs from data preprocessing tasks.
- `modeling.log`: Logs from modeling operations.
- `visualization.log`: Logs from visualization processes.

### 2. Configuring Logging

Logging configurations are defined in `config/config.yaml`. You can adjust log levels, formats, and handlers as needed.

**Example Configuration:**

```yaml
# config/config.yaml

logging:
  version: 1
  disable_existing_loggers: False
  handlers:
    console:
      class: logging.StreamHandler
      level: DEBUG
      formatter: simple
    file:
      class: logging.FileHandler
      level: INFO
      formatter: detailed
      filename: logs/app.log
  formatters:
    simple:
      format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    detailed:
      format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  root:
    level: DEBUG
    handlers: [console, file]
```

### 3. Viewing Logs

Use any text editor or command-line tools like `tail` to view log files.

**Example:**

```bash
tail -f logs/data_collection.log
```

*This command continuously displays new log entries as they are written.*

## Troubleshooting

Encountering issues is a normal part of development. Here are common problems and their solutions.

### 1. Virtual Environment Not Activating

**Issue:** Unable to activate the virtual environment.

**Solution:**

- Ensure you're using the correct command for your operating system.
  
  - **macOS/Linux:**
  
    ```bash
    source .venv/bin/activate
    ```
  
  - **Windows:**
  
    ```bash
    .venv\Scripts\activate
    ```
  
- Verify that the virtual environment exists:

  ```bash
  ls .venv/
  ```

### 2. Missing Dependencies

**Issue:** Import errors or missing packages.

**Solution:**

- Ensure you've activated the virtual environment.
- Reinstall dependencies:

  ```bash
  pip install --upgrade pip
  pip install -r requirements.txt
  ```

### 3. API Rate Limits Exceeded

**Issue:** Receiving errors related to API rate limits.

**Solution:**

- Implement delays between API requests.
- Upgrade to a higher API tier if available.
- Monitor API usage to avoid exceeding limits.

### 4. Failed Data Collection

**Issue:** Data collection scripts fail to retrieve data.

**Solution:**

- Check API keys and ensure they are correctly set in `config/secrets.yaml`.
- Verify internet connectivity.
- Review logs in `logs/data_collection.log` for detailed error messages.

### 5. Dash Application Not Launching

**Issue:** Dash server fails to start or is inaccessible.

**Solution:**

- Ensure all dependencies are installed.
- Check for errors in `logs/visualization.log`.
- Verify that the port (default `8050`) is not being used by another application.
- Run the visualization script again and monitor the terminal for error messages.

### 6. Test Failures

**Issue:** Tests are failing unexpectedly.

**Solution:**

- Review the error messages provided by `pytest` to identify the cause.
- Ensure that the environment is correctly set up and dependencies are installed.
- Update or fix the code as needed to pass the tests.

## Additional Resources

- **[Architecture Documentation](./docs/architecture.md):** Detailed overview of the project's architecture.
- **[API Documentation](./docs/api_documentation.md):** Information about integrated APIs.
- **[Contribution Guidelines](./docs/contribution_guidelines.md):** How to contribute to the project.
- **[Frequently Asked Questions (FAQ)](./docs/faq.md):** Common questions and answers.
- **[Project Roadmap](./docs/roadmap.md):** Upcoming features and improvements.

*Note: Ensure that all referenced documentation files exist within the `docs/` directory.*

---

## Conclusion

This usage guide provides the necessary steps to set up, configure, and operate the **AASB: As Above So Below** project effectively. By following the instructions outlined above, you can ensure a smooth workflow, maintain code quality through testing, and leverage interactive visualizations to explore complex financial relationships.

For any further assistance, refer to the project's [API Documentation](./docs/api_documentation.md) or [Architecture Documentation](./docs/architecture.md). If you encounter issues not covered in this guide, please consult the [Troubleshooting](#troubleshooting) section or reach out to the project maintainer.

Happy analyzing!
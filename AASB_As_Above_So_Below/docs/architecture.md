AASB: As Above So Below - Project Architecture

## Table of Contents

1. [Introduction](#introduction)
2. [Project Overview](#project-overview)
3. [High-Level Architecture](#high-level-architecture)
4. [Component Descriptions](#component-descriptions)
    - [1. Data Collection](#1-data-collection)
    - [2. Data Preprocessing](#2-data-preprocessing)
    - [3. Modeling](#3-modeling)
    - [4. Visualization](#4-visualization)
    - [5. Scripts](#5-scripts)
    - [6. Notebooks](#6-notebooks)
    - [7. Testing](#7-testing)
    - [8. Configuration](#8-configuration)
    - [9. Logging](#9-logging)
    - [10. Documentation](#10-documentation)
5. [Data Flow](#data-flow)
6. [Technologies Used](#technologies-used)
7. [Design Decisions](#design-decisions)
8. [Future Enhancements](#future-enhancements)
9. [Conclusion](#conclusion)

---

## Introduction

The **AASB: As Above So Below** project aims to model and visualize intricate relationships within global financial markets by leveraging advanced mathematical theories, comprehensive data integration, and interactive visualization tools. This architecture document provides an in-depth overview of the project's structure, components, and workflows, facilitating better understanding and collaboration.

## Project Overview

The project is structured into distinct modules, each responsible for specific tasks within the data pipeline:

1. **Data Collection**: Gathers diverse financial and external data from various sources.
2. **Data Preprocessing**: Cleans, transforms, and merges collected data for analysis.
3. **Modeling**: Applies statistical and machine learning models to uncover relationships and patterns.
4. **Visualization**: Creates interactive visual representations of the modeled data.
5. **Scripts**: Contains executable scripts to automate different stages of the pipeline.
6. **Notebooks**: Houses Jupyter notebooks for exploratory data analysis and prototyping.
7. **Testing**: Implements unit tests to ensure code reliability.
8. **Configuration**: Manages configuration settings and sensitive information securely.
9. **Logging**: Tracks the execution flow and records important events.
10. **Documentation**: Provides comprehensive guides and API documentation.

## High-Level Architecture

![High-Level Architecture Diagram](./docs/architecture_diagram.png)

*Note: Replace the above placeholder with an actual architecture diagram for visual representation.*

The architecture follows a modular approach, ensuring scalability, maintainability, and ease of collaboration. Data flows seamlessly from collection to preprocessing, modeling, and visualization, with each stage building upon the previous one.

## Component Descriptions

### 1. Data Collection

**Directory:** `data_collection/`

**Description:**

The Data Collection module is responsible for fetching data from various sources, including APIs, databases, and external files. It is organized into submodules based on data categories to enhance modularity and scalability.

**Submodules:**

- `forex/`: Collects foreign exchange data.
- `bond_yields/`: Gathers bond yields information.
- `climate/`: Fetches climate-related data.
- `commodities/`: Retrieves commodity prices.
- `cultural_trends/`: Collects data on cultural trends.
- `derivatives/`: Gathers derivatives market data.
- `geopolitical_events/`: Fetches information on geopolitical events.
- `global_consciousness/`: Collects data on global consciousness metrics.
- `interest_rates/`: Retrieves interest rate data.
- `social_media/`: Gathers social media sentiment data.
- `stock_indices/`: Collects stock indices data.
- `technology_innovations/`: Fetches data on technological innovations.

**Example Module (`collect_bond_yields.py`):**

```python
# data_collection/bond_yields/collect_bond_yields.py

import logging
import pandas as pd

def collect_bond_yields(api_key: str) -> pd.DataFrame:
    """
    Collect Bond Yields data from the specified API.

    Parameters:
    - api_key (str): API key for authentication.

    Returns:
    - pd.DataFrame: Collected Bond Yields data.
    """
    logger = logging.getLogger(__name__)
    try:
        logger.info("Starting Bond Yields data collection...")
        # Implement API call logic here
        data = pd.DataFrame()  # Placeholder for collected data
        if data.empty:
            raise ValueError("Received empty Bond Yields data.")
        logger.info("Bond Yields data collection successful.")
        return data
    except Exception as e:
        logger.error(f"Bond Yields data collection failed: {e}")
        raise
```

### 2. Data Preprocessing

**Directory:** `data_preprocessing/`

**Description:**

This module handles the cleaning, transformation, and merging of raw data collected from various sources. It ensures that the data is in a suitable format for modeling and analysis.

**Key Functions:**

- `preprocess_and_merge_data.py`: Cleans and merges data from different sources.

**Example Script (`preprocess_and_merge_data.py`):**

```python
# data_preprocessing/preprocess_and_merge_data.py

import logging
import pandas as pd
from typing import List

def preprocess_and_merge_data(raw_data_paths: List[str], processed_data_path: str) -> pd.DataFrame:
    """
    Preprocess and merge raw data into a single processed dataset.

    Parameters:
    - raw_data_paths (List[str]): List of file paths to raw data CSVs.
    - processed_data_path (str): File path to save the processed data.

    Returns:
    - pd.DataFrame: The merged and processed DataFrame.
    """
    logger = logging.getLogger(__name__)
    try:
        logger.info("Starting data preprocessing...")
        data_frames = []
        for path in raw_data_paths:
            df = pd.read_csv(path)
            # Implement specific preprocessing steps here
            df_clean = df.dropna()  # Example step
            data_frames.append(df_clean)
        merged_df = pd.concat(data_frames, axis=0, ignore_index=True)
        merged_df.to_csv(processed_data_path, index=False)
        logger.info("Data preprocessing and merging completed successfully.")
        return merged_df
    except Exception as e:
        logger.error(f"Data preprocessing failed: {e}")
        raise
```

### 3. Modeling

**Directory:** `modeling/`

**Description:**

The Modeling module applies statistical and machine learning models to the preprocessed data to uncover relationships, patterns, and insights. It includes functionalities for Vector Autoregressions (VAR) and Granger Causality tests.

**Submodules:**

- `var_models.py`: Implements VAR models.
- `granger_causality.py`: Performs Granger Causality tests.

**Example Script (`var_models.py`):**

```python
# modeling/var_models.py

import logging
import pandas as pd
from statsmodels.tsa.api import VAR

def fit_var_model(data: pd.DataFrame, maxlags: int = 15, ic: str = 'aic') -> VARResults:
    """
    Fit a Vector Autoregression (VAR) model to the data.

    Parameters:
    - data (pd.DataFrame): Preprocessed financial data.
    - maxlags (int): Maximum number of lags to consider.
    - ic (str): Information criterion for lag selection ('aic', 'bic', etc.).

    Returns:
    - VARResults: Fitted VAR model results.
    """
    logger = logging.getLogger(__name__)
    try:
        logger.info("Fitting VAR model...")
        model = VAR(data)
        results = model.fit(maxlags=maxlags, ic=ic)
        logger.info("VAR model fitted successfully.")
        return results
    except Exception as e:
        logger.error(f"VAR model fitting failed: {e}")
        raise
```

### 4. Visualization

**Directory:** `visualization/`

**Description:**

This module creates interactive visual representations of the modeled data, enabling users to explore relationships and patterns effectively. It leverages libraries like Dash, Plotly, and NetworkX to build dynamic dashboards.

**Key Scripts:**

- `visualize_recursive_graph.py`: Generates recursive Ramsey graphs with integrated VAR insights.

**Example Script (`visualize_recursive_graph.py`):**

```python
# visualization/visualize_recursive_graph.py

import logging
import networkx as nx
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

def generate_recursive_graph(data: pd.DataFrame, var_results) -> go.Figure:
    """
    Generate a recursive Ramsey graph with VAR insights.

    Parameters:
    - data (pd.DataFrame): Preprocessed data.
    - var_results: Results from the VAR model.

    Returns:
    - go.Figure: Plotly figure representing the graph.
    """
    logger = logging.getLogger(__name__)
    try:
        logger.info("Generating recursive Ramsey graph...")
        G = nx.complete_graph(len(data.columns))  # Example graph
        pos = nx.spring_layout(G, seed=42)
        
        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x += [x0, x1, None]
            edge_y += [y0, y1, None]
        
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines'
        )
        
        node_x = []
        node_y = []
        node_text = []
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(f'Node {node}')
        
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                size=10,
                color='skyblue',
                line_width=2
            ),
            text=node_text
        )
        
        fig = go.Figure(data=[edge_trace, node_trace],
                        layout=go.Layout(
                            title='<br>Recursive Ramsey Graph with VAR Insights',
                            titlefont_size=16,
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20,l=5,r=5,t=40),
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                        )
        logger.info("Graph generation successful.")
        return fig
    except Exception as e:
        logger.error(f"Graph generation failed: {e}")
        raise

def create_dash_app(fig: go.Figure) -> Dash:
    """
    Create a Dash application for interactive visualization.

    Parameters:
    - fig (go.Figure): Plotly figure to display.

    Returns:
    - Dash: Configured Dash application.
    """
    logger = logging.getLogger(__name__)
    try:
        logger.info("Creating Dash application...")
        app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        
        app.layout = html.Div([
            dbc.Container([
                dbc.Row([
                    dbc.Col(html.H1("AASB: As Above So Below - Visualization", className="text-center text-primary mb-4"), width=12)
                ]),
                dbc.Row([
                    dbc.Col(dcc.Graph(id='graph', figure=fig), width=12)
                ]),
                dbc.Row([
                    dbc.Col(html.Div(id='node-details'), width=12)
                ])
            ])
        ])
        
        @app.callback(
            Output('graph', 'figure'),
            [Input('graph', 'clickData')]
        )
        def update_graph(clickData):
            if clickData is None:
                return fig
            else:
                node_clicked = clickData['points'][0]['text']
                # Implement logic to generate subgraphs based on the clicked node
                # Placeholder: return the same figure
                return fig
        
        @app.callback(
            Output('node-details', 'children'),
            [Input('graph', 'clickData')]
        )
        def display_node_details(clickData):
            if clickData is None:
                return "Click on a node to explore its sub-universe."
            else:
                node_clicked = clickData['points'][0]['text']
                return f"You clicked on {node_clicked}. Zooming into its sub-universe..."
        
        logger.info("Dash application created successfully.")
        return app
    except Exception as e:
        logger.error(f"Failed to create Dash app: {e}")
        raise
```

### 5. Scripts

**Directory:** `scripts/`

**Description:**

Contains executable scripts to automate different stages of the data pipeline, enhancing workflow efficiency and organization.

**Scripts:**

- `run_data_collection.py`: Executes data collection processes.
- `run_preprocessing.py`: Runs data preprocessing tasks.
- `run_modeling.py`: Performs modeling operations.
- `run_visualization.py`: Launches the visualization dashboard.

**Example Script (`run_data_collection.py`):**

```python
# scripts/run_data_collection.py

import logging
import yaml
import os
from joblib import Parallel, delayed
from data_collection.forex.collect_forex_data import collect_forex_data
from data_collection.bond_yields.collect_bond_yields import collect_bond_yields
from data_collection.climate.collect_climate_data import collect_climate_data
from data_collection.commodities.collect_commodity_prices import collect_commodity_prices
from data_collection.cultural_trends.collect_cultural_trends import collect_cultural_trends
from data_collection.derivatives.collect_derivatives_data import collect_derivatives_data
from data_collection.geopolitical_events.collect_geopolitical_events import collect_geopolitical_events
from data_collection.global_consciousness.collect_global_consciousness_data import collect_global_consciousness_data
from data_collection.interest_rates.collect_interest_rates import collect_interest_rates
from data_collection.social_media.collect_social_media_data import collect_social_media_data
from data_collection.stock_indices.collect_stock_indices import collect_stock_indices
from data_collection.technology_innovations.collect_technology_innovations import collect_technology_innovations
from dotenv import load_dotenv

def setup_logging():
    with open('config/config.yaml', 'r') as f:
        config = yaml.safe_load(f.read())
    logging.config.dictConfig(config['logging'])

def load_secrets():
    load_dotenv()
    with open('config/secrets.yaml', 'r') as f:
        secrets = yaml.safe_load(f.read())
    return secrets

def run_data_collection():
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting data collection...")
    
    secrets = load_secrets()
    forex_api_key = secrets['api_keys']['forex_api']
    bond_yields_api_key = secrets['api_keys']['bond_yields_api']
    # Load other API keys as needed
    
    collection_functions = [
        lambda: collect_forex_data(forex_api_key),
        lambda: collect_bond_yields(bond_yields_api_key),
        collect_climate_data,
        collect_commodity_prices,
        collect_cultural_trends,
        collect_derivatives_data,
        collect_geopolitical_events,
        collect_global_consciousness_data,
        collect_interest_rates,
        collect_social_media_data,
        collect_stock_indices,
        collect_technology_innovations
    ]
    
    Parallel(n_jobs=-1)(delayed(func)() for func in collection_functions)
    
    logger.info("Data collection completed successfully.")

if __name__ == "__main__":
    run_data_collection()
```

### 6. Notebooks

**Directory:** `notebooks/`

**Description:**

Contains Jupyter notebooks for exploratory data analysis (EDA), prototyping, and documenting experiments. These notebooks facilitate interactive analysis and visualization, aiding in the development and refinement of models and visualizations.

**Example Notebooks:**

- `EDA.ipynb`: Conducts exploratory data analysis to understand data distributions, correlations, and patterns.
- `VAR_Modeling.ipynb`: Prototypes Vector Autoregression models and conducts Granger Causality tests.
- `Visualization_Prototyping.ipynb`: Tests and develops visualization techniques and dashboards.

### 7. Testing

**Directory:** `tests/`

**Description:**

Implements unit tests for various modules and scripts to ensure code reliability and facilitate maintenance. Utilizing a testing framework like `pytest`, this directory helps in identifying and fixing bugs during development.

**Example Test (`test_collect_bond_yields.py`):**

```python
# tests/test_collect_bond_yields.py

import unittest
from data_collection.bond_yields.collect_bond_yields import collect_bond_yields
import pandas as pd

class TestCollectBondYields(unittest.TestCase):
    def test_collect_bond_yields(self):
        api_key = "test_api_key"  # Use a mock or test API key
        data = collect_bond_yields(api_key)
        self.assertIsInstance(data, pd.DataFrame)
        self.assertFalse(data.empty)
        # Add more assertions based on expected data structure

if __name__ == '__main__':
    unittest.main()
```

### 8. Configuration

**Directory:** `config/`

**Description:**

Stores configuration files and sensitive information, managing settings, API keys, and parameters in a centralized and secure manner.

**Files:**

- `config.yaml`: Contains general configuration settings, such as logging configurations.
- `secrets.yaml`: Stores sensitive information like API keys (ensure this file is added to `.gitignore`).

**Example `config.yaml`:**

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

**Example `secrets.yaml`:**

```yaml
# config/secrets.yaml

api_keys:
  forex_api: YOUR_FOREX_API_KEY
  bond_yields_api: YOUR_BOND_YIELDS_API_KEY
  # Add other API keys here
```

### 9. Logging

**Directory:** `logs/`

**Description:**

Stores log files generated during the execution of different modules and scripts. Logging facilitates monitoring, debugging, and maintaining a record of the application's behavior.

**Log Files:**

- `data_collection.log`: Logs related to data collection processes.
- `data_preprocessing.log`: Logs from data preprocessing tasks.
- `modeling.log`: Logs from modeling operations.
- `visualization.log`: Logs from visualization processes.

**Example Logging Configuration:**

As defined in `config.yaml`, logs are directed both to the console and to respective log files within the `logs/` directory.

### 10. Documentation

**Directory:** `docs/`

**Description:**

Provides comprehensive documentation, including architecture details, usage guides, and API documentation. This directory aids in understanding the project's structure, functionalities, and how to interact with its components.

**Documentation Files:**

- `architecture.md`: (This file) Details the project's architecture.
- `usage_guide.md`: Instructions on how to set up, run, and use the project.
- `api_documentation.md`: Documentation of APIs used or exposed by the project.

**Example `architecture.md`:**

*This is the file you're requesting, so it's provided below.*

## Data Flow

1. **Data Collection:**
    - Scripts within the `data_collection/` module fetch data from various sources using API keys stored in `config/secrets.yaml`.
    - Collected data is saved into the `data/raw/` directory for raw, unaltered data.

2. **Data Preprocessing:**
    - The `data_preprocessing/` module cleans and transforms raw data.
    - Processed data is merged and saved into the `data/processed/` directory, ready for modeling.

3. **Modeling:**
    - The `modeling/` module applies VAR models and performs Granger Causality tests on the processed data.
    - Results are stored for further analysis and visualization.

4. **Visualization:**
    - The `visualization/` module generates interactive graphs and dashboards using Dash and Plotly.
    - Visualizations are accessible via the Dash application, allowing users to explore the data dynamically.

## Technologies Used

- **Programming Language:** Python 3.11
- **Data Manipulation:** Pandas, Dask
- **Statistical Modeling:** Statsmodels, Scikit-learn
- **Visualization:** Plotly, Dash, NetworkX
- **Parallel Processing:** Joblib
- **Configuration Management:** YAML, Python-dotenv
- **Testing:** Unittest, Pytest
- **Logging:** Python's built-in `logging` module
- **Version Control:** Git
- **Containerization:** Docker (with `Dockerfile`)
- **Documentation:** Markdown, Jupyter Notebooks
- **Continuous Integration:** GitHub Actions

## Design Decisions

1. **Modular Architecture:**
    - **Rationale:** Enhances scalability and maintainability by segregating functionalities into distinct modules.
    - **Implementation:** Organized directories for data collection, preprocessing, modeling, visualization, etc.

2. **Submodule Organization:**
    - **Rationale:** Facilitates easier management and extension of data collection scripts based on data categories.
    - **Implementation:** Created subdirectories within `data_collection/` for each data type (e.g., `forex/`, `bond_yields/`).

3. **Configuration Management:**
    - **Rationale:** Centralizes configuration settings and secures sensitive information.
    - **Implementation:** Utilized `config.yaml` for general settings and `secrets.yaml` for API keys, loaded via environment variables.

4. **Logging Implementation:**
    - **Rationale:** Enables tracking of application behavior and aids in debugging.
    - **Implementation:** Configured logging to output to both console and log files for each module.

5. **Automated Scripts:**
    - **Rationale:** Streamlines the execution of different pipeline stages and promotes automation.
    - **Implementation:** Placed executable scripts within the `scripts/` directory to run data collection, preprocessing, modeling, and visualization.

6. **Testing Framework:**
    - **Rationale:** Ensures code reliability and facilitates maintenance by catching bugs early.
    - **Implementation:** Developed unit tests using `unittest` and `pytest` within the `tests/` directory.

7. **Interactive Visualization:**
    - **Rationale:** Provides users with the ability to explore data relationships dynamically.
    - **Implementation:** Leveraged Dash and Plotly to build interactive dashboards, integrated with NetworkX for graph representations.

8. **Containerization:**
    - **Rationale:** Ensures consistent environments across development, testing, and production.
    - **Implementation:** Created a `Dockerfile` to containerize the application, enabling easy deployment.

## Future Enhancements

1. **Advanced Modeling Techniques:**
    - Incorporate machine learning models for predictive analytics.
    - Explore deep learning approaches for complex pattern recognition.

2. **Enhanced Visualization Features:**
    - Implement more interactive elements in Dash dashboards, such as filters, drill-downs, and dynamic graph updates.
    - Develop 3D visualizations for deeper insights.

3. **Real-Time Data Integration:**
    - Set up real-time data streams to enable live updating of models and visualizations.
    - Utilize web sockets or APIs for continuous data ingestion.

4. **User Authentication and Authorization:**
    - Secure the Dash application by implementing user authentication mechanisms.
    - Control access to different parts of the dashboard based on user roles.

5. **Scalability Improvements:**
    - Optimize data processing pipelines to handle larger datasets efficiently.
    - Implement distributed computing frameworks if necessary.

6. **Comprehensive Documentation:**
    - Expand the `docs/` directory with more detailed guides, tutorials, and API references.
    - Include examples and best practices for contributors.

7. **Automated Deployment Pipelines:**
    - Enhance CI/CD workflows to automate testing, building, and deployment processes.
    - Integrate deployment to cloud platforms seamlessly.

8. **Data Versioning and Lineage Tracking:**
    - Utilize tools like DVC (Data Version Control) to manage data versions and track data lineage.
    - Ensure reproducibility by maintaining records of data versions used in modeling.

## Conclusion

The **AASB: As Above So Below** project is meticulously structured to facilitate comprehensive data collection, preprocessing, modeling, and visualization of complex financial relationships. The modular architecture, combined with best practices in configuration management, logging, testing, and documentation, ensures that the project is scalable, maintainable, and secure.

By adhering to the outlined architecture and implementing the recommended enhancements, the project is well-positioned to deliver valuable insights into global financial markets, supporting informed decision-making and strategic planning.

For any further assistance or inquiries regarding the project architecture, please feel free to reach out.

---

# Additional Notes

- **Architecture Diagram:** It's highly recommended to create a visual architecture diagram (e.g., using tools like Draw.io, Lucidchart, or Microsoft Visio) and place it within the `docs/` directory. Update the `architecture.md` file with a link to this diagram for better visualization.

- **Security Considerations:** Always ensure that sensitive information, especially API keys and credentials, are securely managed and not exposed in version control systems. Utilize environment variables and secure storage solutions.

- **Collaboration:** Encourage team members to follow the established directory structure and coding standards to maintain consistency across the project.

- **Continuous Improvement:** Regularly review and update the architecture documentation to reflect any changes or enhancements made to the project over time.

---

If you need assistance with creating specific sections of the `architecture.md` file, generating the architecture diagram, or any other aspect of your project, feel free to ask!
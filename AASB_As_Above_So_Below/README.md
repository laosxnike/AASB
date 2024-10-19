AASB: As Above So Below

![Project Logo](docs/images/project_logo.png) <!-- Replace with your project logo if available -->

## Table of Contents

- [Introduction](#introduction)
- [Purpose and Motivation](#purpose-and-motivation)
- [Potential Implications](#potential-implications)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Clone the Repository](#clone-the-repository)
  - [Setup Virtual Environment](#setup-virtual-environment)
  - [Install Dependencies](#install-dependencies)
- [Running the Application](#running-the-application)
  - [Locally](#locally)
  - [Using Docker](#using-docker)
- [Usage](#usage)
  - [Interacting with the Ramsey Graph](#interacting-with-the-ramsey-graph)
- [Testing](#testing)
- [Logging](#logging)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Acknowledgments](#acknowledgments)

## Introduction

**AASB: As Above So Below** is an innovative data visualization project that employs **Dash** and **Plotly** to create dynamic and interactive Ramsey graphs. These graphs are designed to illustrate the complex relationships between macro and micro-level financial forces influencing global markets. By providing an intuitive interface, **AASB** enables users to explore various financial indicators and their interconnections, facilitating deeper insights into market dynamics and decision-making processes.

## Purpose and Motivation

### Understanding Complex Financial Systems

Global financial markets are intricate ecosystems influenced by a myriad of factors, ranging from economic indicators and geopolitical events to technological innovations and social trends. Traditional analysis methods often isolate these factors, making it challenging to comprehend their interdependencies and collective impact. **AASB: As Above So Below** bridges this gap by providing a holistic visualization of both macro and micro-level forces, offering a comprehensive understanding of how various elements interact within the financial landscape.

### Enhancing Decision-Making Processes

Financial professionals, policymakers, and investors rely heavily on data-driven insights to make informed decisions. However, the sheer volume and complexity of financial data can be overwhelming, leading to analysis paralysis or suboptimal choices. This project leverages **Dash** and **Plotly** to create interactive Ramsey graphs, enabling users to intuitively explore and analyze the interconnectedness of different financial forces. By simplifying complex data relationships, **AASB** empowers stakeholders to make more accurate predictions, assess risks effectively, and identify emerging opportunities.

### Advancing Academic and Practical Research

In academia, understanding causal relationships and dynamic interactions within financial markets is pivotal for developing robust economic theories and models. **AASB** provides a tool that facilitates such research by offering a visual platform to test hypotheses, validate models, and uncover hidden patterns in financial data. For practitioners, the insights derived from this project can inform strategic planning, risk management, and portfolio optimization, contributing to more resilient and adaptive financial strategies.

## Potential Implications

### Improved Risk Assessment and Management

By visualizing the interplay between various financial indicators and external factors, **AASB** enables a deeper understanding of potential risk factors. Organizations can identify critical leverage points, anticipate market shifts, and implement proactive measures to mitigate risks, enhancing overall financial stability.

### Enhanced Policy Formulation and Evaluation

Policymakers can utilize insights from **AASB** to design more effective economic policies. Understanding how different sectors and indicators influence each other allows for more targeted interventions, better regulation, and the ability to foresee the broader economic impact of policy decisions.

### Strategic Investment and Portfolio Optimization

Investors can leverage the Ramsey graphs to identify trends, correlations, and potential investment opportunities. By comprehensively analyzing macro and micro-level forces, investors can diversify their portfolios more effectively, align their strategies with prevailing market conditions, and achieve better returns.

### Facilitating Interdisciplinary Collaboration

The project's comprehensive approach fosters collaboration across various disciplines, including economics, data science, political science, and environmental studies. By integrating diverse data sources and analytical perspectives, **AASB** promotes a more nuanced and multifaceted understanding of financial systems.

### Educational Tool for Academia and Training

**AASB** serves as an educational resource for students and professionals seeking to grasp the complexities of financial markets. Interactive visualizations make learning more engaging and accessible, aiding in the development of analytical and critical thinking skills essential for navigating modern financial landscapes.

### Contribution to Open-Source Community and Knowledge Sharing

By making the tools and methodologies publicly available, **AASB** encourages knowledge sharing and community-driven enhancements. This openness fosters innovation, allows for peer review, and ensures that the project remains adaptable to evolving financial paradigms and technological advancements.

## Features

- **Interactive Ramsey Graphs:** Visualize macro and micro-level financial forces with dynamic relationships.
- **Dynamic Navigation:** Click on nodes to explore sub-forces and delve deeper into specific financial indicators.
- **Fixed Vertex Layout:** Consistent node positions enhance user familiarity and ease of comparison across different data sets.
- **Real-Time and Historical Data Integration:** Analyze how relationships evolve over time and respond to current market conditions.
- **Scenario Simulation:** Perform what-if analyses and stress testing to assess potential market reactions.
- **Zoom and Pan Functionality:** Explore different areas of the graph in detail without losing the overall context.
- **Tooltips and Detailed Insights:** Access additional information about each node and edge through interactive tooltips.
- **Docker Integration:** Easily deploy the application in a consistent environment using Docker containers.
- **Comprehensive Documentation:** Detailed guides and documentation to assist users and contributors.

## Project Structure

```
AASB_As_Above_So_Below/
├── Dockerfile
├── README.md
├── config/
│   ├── config.yaml
│   └── secrets.yaml
├── data/
│   ├── external/
│   ├── interim/
│   ├── processed/
│   │   └── GCP Hypothesis Results - Results.csv
│   └── raw/
├── data_collection/
│   ├── __init__.py
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
│   ├── forex/
│   │   ├── __init__.py
│   │   └── collect_forex_data.py
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
│   ├── __pycache__/
│   │   └── preprocess_and_merge_data.cpython-311.pyc
│   └── preprocess_and_merge_data.py
├── docs/
│   ├── api_documentation.md
│   ├── architecture.md
│   ├── contribution_guidelines.md
│   ├── faq.md
│   ├── images/
│   ├── roadmap.md
│   └── usage_guide.md
├── logs/
│   ├── data_collection.log
│   ├── data_preprocessing.log
│   ├── modeling.log
│   └── visualization.log
├── main.py
├── modeling/
│   ├── __init__.py
│   ├── __pycache__/
│   │   └── model_relationships.cpython-311.pyc
│   ├── granger_causality.py
│   └── var_models.py
├── notebooks/
│   ├── EDA.ipynb
│   ├── Ramsey_Graph_Visualization.ipynb
│   ├── VAR_Modeling.ipynb
│   └── Visualization_Prototyping.ipynb
├── requirements.txt
├── scripts/
│   ├── run_data_collection.py
│   ├── run_modeling.py
│   ├── run_preprocessing.py
│   └── run_visualization.py
├── tests/
│   ├── __init__.py
│   ├── test_collect_bond_yields.py
│   ├── test_collect_forex_data.py
│   ├── test_model_relationships.py
│   ├── test_preprocess_and_merge_data.py
│   └── test_visualize_recursive_graph.py
└── visualization/
    ├── __init__.py
    ├── __pycache__/
    │   ├── __init__.cpython-311.pyc
    │   └── visualize_recursive_graph.cpython-311.pyc
    ├── ramsey_graph_plotly.py
    └── visualize_recursive_graph.py

32 directories, 68 files
```

### Key Directories and Files

- **`Dockerfile`**: Configuration file to build the Docker image for containerized deployment.
- **`config/`**: Contains configuration files and secrets.
- **`data/`**: Organized data directories for external, interim, processed, and raw data.
- **`data_collection/`**: Scripts for collecting various types of data.
- **`data_preprocessing/`**: Scripts for preprocessing and merging collected data.
- **`docs/`**: Comprehensive documentation including API docs, architecture, contribution guidelines, FAQs, and usage guides.
- **`logs/`**: Log files for different components of the project.
- **`modeling/`**: Scripts related to data modeling, including Granger causality and VAR models.
- **`notebooks/`**: Jupyter notebooks for exploratory data analysis and visualization prototyping.
- **`scripts/`**: Executable scripts to run different stages of the data pipeline and visualization.
- **`tests/`**: Unit and integration tests to ensure code reliability.
- **`visualization/`**: Core visualization scripts using Dash and Plotly to create interactive Ramsey graphs.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- **Operating System:** macOS, Windows, or Linux.
- **Python Version:** Python 3.10 or higher.
- **Docker:** (Optional) If you plan to run the application using Docker.
- **Git:** Installed for version control and repository cloning.

## Installation

### Clone the Repository

Start by cloning the repository to your local machine:

```bash
git clone https://github.com/yourusername/AASB_As_Above_So_Below.git
cd AASB_As_Above_So_Below
```

### Setup Virtual Environment

It's recommended to use a virtual environment to manage project dependencies.

1. **Create a Virtual Environment:**

   ```bash
   python -m venv .venv
   ```

2. **Activate the Virtual Environment:**

   - **On macOS and Linux:**

     ```bash
     source .venv/bin/activate
     ```

   - **On Windows:**

     ```bash
     .venv\Scripts\activate
     ```

### Install Dependencies

With the virtual environment activated, install the required Python packages:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Sample `requirements.txt`:**

```plaintext
dash==2.12.1
plotly==5.15.0
numpy==1.24.3
pandas==1.5.3
pytest==7.2.2
python-dotenv==0.21.1
```

*Ensure that your `requirements.txt` includes all necessary dependencies for the project.*

## Running the Application

You can run the application either locally or using Docker. Choose the method that best fits your workflow.

### Locally

1. **Activate the Virtual Environment:**

   Ensure your virtual environment is active:

   ```bash
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Run the Visualization Script:**

   Execute the script to launch the Dash application:

   ```bash
   python scripts/run_visualization.py
   ```

3. **Access the Application:**

   Open your web browser and navigate to:

   ```
   http://localhost:8050/
   ```

   You should see the Ramsey Graph visualization interface.

### Using Docker

If you prefer containerized deployment, follow these steps:

1. **Build the Docker Image:**

   Navigate to the project's root directory and build the Docker image:

   ```bash
   docker build -t aasb_app .
   ```

2. **Run the Docker Container:**

   Launch the container using the built image:

   ```bash
   docker run -d -p 8050:8050 --name aasb_container aasb_app
   ```

   - `-d`: Runs the container in detached mode.
   - `-p 8050:8050`: Maps port 8050 of the host to port 8050 of the container.

3. **Access the Application:**

   Open your web browser and navigate to:

   ```
   http://localhost:8050/
   ```

4. **View Logs (Optional):**

   To monitor the container's logs:

   ```bash
   docker logs -f aasb_container
   ```

5. **Stop and Remove the Container (When Needed):**

   ```bash
   docker stop aasb_container
   docker rm aasb_container
   ```

## Usage

### Interacting with the Ramsey Graph

**AASB: As Above So Below** transforms a static Ramsey graph into a dynamic, data-rich visualization tool. Here's how users can derive value from the interactive features:

1. **Exploring the Main Graph:**

   Upon accessing the application, you'll see the main Ramsey graph depicting macro-level financial forces.

2. **Navigating to Sub-Graphs:**

   - **Click on a Node:** Click on any node representing a main force (e.g., "Forex") to explore its sub-forces.
   - **View Sub-Graph:** A new graph will appear, detailing the micro-level sub-forces related to the selected main force.

3. **Using the "Back" Button:**

   - **Navigate Back:** Click the "Back" button to return to the previous graph level.
   - **Multiple Levels:** The application maintains a navigation history, allowing you to traverse back through multiple graph levels if you've navigated deeper.

4. **Zoom and Pan:**

   - **Zoom In/Out:** Use your mouse scroll or touchpad gestures to zoom in and out of the graph.
   - **Pan:** Click and drag to move around the graph canvas.

5. **Hover Information:**

   - **View Details:** Hover over nodes and edges to view additional information about the forces and their relationships.

6. **Scenario Simulation:**

   - **What-If Analysis:** Modify certain variables or indicators to simulate different market scenarios and observe how relationships evolve.

7. **Filter and Customize Views:**

   - **Filter by Category:** Display only "Direct" or "Indirect" forces to simplify the view based on your focus area.
   - **Adjust Parameters:** Change thresholds or criteria to see how relationships adapt under different conditions.

### Benefits of Adding Data to the Graph

- **Reveals Hidden Patterns and Relationships:** Data integration allows the graph to illustrate not just potential connections but also the strength and nature of these relationships.
- **Enables Informed Decision-Making:** Users can identify key influencers, understand interdependencies, and make strategic decisions based on real-time and historical data insights.
- **Facilitates Research and Analysis:** Researchers can test hypotheses, validate models, and uncover trends that inform academic and practical research.
- **Enhances Collaboration:** Provides a common visual platform for interdisciplinary teams to discuss and strategize based on shared data insights.

## Testing

Ensure the reliability and correctness of your code by running the provided tests.

1. **Navigate to the Project Root Directory:**

   ```bash
   cd path/to/AASB_As_Above_So_Below
   ```

2. **Activate the Virtual Environment:**

   ```bash
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Run Tests:**

   Execute all tests within the `tests/` directory using `pytest`:

   ```bash
   pytest
   ```

   *Ensure that `pytest` is included in your `requirements.txt`.*

4. **Interpreting Results:**

   - **Passing Tests:** Indicates that the corresponding modules are functioning as expected.
   - **Failing Tests:** Review the error messages and debug the relevant modules.

## Logging

All logs are stored in the `logs/` directory, categorized by component:

- **`data_collection.log`**: Logs related to data collection processes.
- **`data_preprocessing.log`**: Logs for data preprocessing activities.
- **`modeling.log`**: Logs generated during modeling phases.
- **`visualization.log`**: Logs pertaining to the visualization application.

*Regularly monitor these logs to identify and address any issues.*

## Contributing

Contributions are welcome! To maintain a high standard of quality and consistency, please follow the guidelines outlined below.

### Guidelines

1. **Fork the Repository:**

   Click on the "Fork" button at the top-right corner of the repository to create your own copy.

2. **Clone Your Fork:**

   ```bash
   git clone https://github.com/yourusername/AASB_As_Above_So_Below.git
   cd AASB_As_Above_So_Below
   ```

3. **Create a New Branch:**

   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Changes:**

   Implement your feature or bug fix.

5. **Run Tests:**

   Ensure all tests pass before committing.

   ```bash
   pytest
   ```

6. **Commit Your Changes:**

   ```bash
   git add .
   git commit -m "Add feature: your feature description"
   ```

7. **Push to Your Fork:**

   ```bash
   git push origin feature/your-feature-name
   ```

8. **Create a Pull Request:**

   Navigate to your fork on GitHub and click "Compare & pull request."

### Code of Conduct

Please adhere to the [Contributor Covenant Code of Conduct](docs/code_of_conduct.md) in all interactions.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any inquiries or support, please reach out to:

- **Name:** Blair Co
- **Email:** blairco@example.com
- **LinkedIn:** [linkedin.com/in/blairco](https://linkedin.com/in/blairco)
- **GitHub:** [github.com/yourusername](https://github.com/yourusername)

## Acknowledgments

- **Plotly and Dash:** For their powerful visualization and web application frameworks.
- **OpenAI:** For providing assistance in project development.
- **Community Contributors:** Thanks to all who contribute to open-source projects that make this application possible.

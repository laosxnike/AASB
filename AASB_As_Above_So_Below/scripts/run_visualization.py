# scripts/run_visualization.py

import sys
import os

def main():
    """
    Entry point to run the Ramsey Graph Visualization Dash application.
    """
    # Determine the absolute path to the project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    # Add the project root to sys.path to ensure modules are importable
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    
    try:
        from visualization.visualize_recursive_graph import app
    except ImportError as e:
        print("Error importing the Dash app. Ensure that the 'visualization' module is in the correct directory.")
        print(e)
        sys.exit(1)
    
    # Run the Dash app
    app.run_server(debug=True, host='0.0.0.0', port=8050)

if __name__ == '__main__':
    main()

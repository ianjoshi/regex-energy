import sys
import os

# Add the parent directory to the system path to allow module imports from the parent folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from analysis.results_loader import ResultsLoader

# Load the results
loader = ResultsLoader()
energy_records = loader.load_results()
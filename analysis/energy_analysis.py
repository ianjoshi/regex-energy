import sys
import os

# Add the parent directory to the system path to allow module imports from the parent folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from analysis.results_loader import ResultsLoader
from analysis.statistics_generator import StatisticsGenerator

# Load the results
loader = ResultsLoader()
energy_records = loader.load_results()

# Compute stats
stats_generator = StatisticsGenerator(energy_records)
stats_generator.generate()
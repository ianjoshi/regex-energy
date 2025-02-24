import sys
import os

# Add the parent directory to the system path to allow module imports from the parent folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from analysis.results_loader import ResultsLoader
from analysis.effect_size_generator import EffectSizeGenerator
from analysis.plot_generator import PlotGenerator
from analysis.statistics_generator import StatisticsGenerator

# Load the results
loader = ResultsLoader()
energy_records = loader.load_results()

# Compute stats
stats_generator = StatisticsGenerator(energy_records)
stats_generator.generate()

# Compute effect sizes
effect_size_generator = EffectSizeGenerator(energy_records)
effect_size_generator.generate()

# Generate plots
plots_generator = PlotGenerator(energy_records)
plots_generator.generate_violin_plots(metric="energy")
plots_generator.generate_violin_plots(metric="time")
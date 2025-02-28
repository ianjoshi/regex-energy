import sys
import os

# Add the parent directory to the system path to allow module imports from the parent folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from analysis.results_loader import ResultsLoader
from analysis.effect_size_generator import EffectSizeGenerator
from analysis.plot_generator import PlotGenerator
from analysis.statistics_generator import StatisticsGenerator

class EnergyAnalysis:

    def __init__(self):
        pass

    def run(self):
        # Load the results
        loader = ResultsLoader()
        energy_records = loader.load_results()
        energy_records_with_outliers = energy_records.copy()

        # Compute stats
        stats_generator = StatisticsGenerator(energy_records, outlier_method="iqr")
        filtered_records = stats_generator.generate()

        # Compute effect sizes
        effect_size_generator = EffectSizeGenerator(filtered_records, parametric=True)
        effect_size_generator.generate()

        # Generate plots with outliers
        plots_generator = PlotGenerator(energy_records_with_outliers)
        plots_generator.generate_violin_plots(metric="energy", output_dir="results/plots_with_outliers")
        plots_generator.generate_violin_plots(metric="time", output_dir="results/plots_with_outliers")

        # Generate plots without outliers
        plots_generator = PlotGenerator(filtered_records)
        plots_generator.generate_violin_plots(metric="energy")
        plots_generator.generate_violin_plots(metric="time")
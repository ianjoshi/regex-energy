import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from typing import List
import os

class PlotGenerator:
    """
    A class to generate plots per regex complexity, and per regex engine.
    Plots are saved to specified directory.
    """

    def __init__(self, records: List):
        """
        Parameters:
            - records (List[EnergyRecord]): A list of EnergyRecord objects with time-energy measurements.
        """
        self.records = records
        self.df = self._create_dataframe()

    def _create_dataframe(self) -> pd.DataFrame:
        """
        Convert the list of record objects into a pandas DataFrame.
        """
        data = {
            "engine": [r.engine for r in self.records],
            "regex_complexity": [r.regex_complexity for r in self.records],
            "run": [r.run for r in self.records],
            "time": [r.time for r in self.records],
            "energy": [r.energy for r in self.records],
        }
        return pd.DataFrame(data)

    def generate_violin_plots(self,
                              metric: str,
                              output_dir: str = "results/plots"):
        """
        Generate violin+box plots for each unique regex_complexity in the dataset,
        with 'engine' on the x-axis and the chosen metric on the y-axis.
        Each plot is saved as a PNG.

        Parameters:
        - metric (str): Which metric to plot on the y-axis (must be "energy" or "time").
        - output_dir (str): Directory to save the resulting PNG files.
        """
        # Validate the metric
        if metric not in ["energy", "time"]:
            raise ValueError(f"Invalid metric '{metric}'. Choose 'energy' or 'time'.")

        # Create the output directory if it does not exist
        os.makedirs(output_dir, exist_ok=True)

        # Get all unique complexities
        complexities = self.df["regex_complexity"].unique()

        # Create and save a plot for each complexity
        for complexity in complexities:
            subset = self.df[self.df["regex_complexity"] == complexity]

            plt.figure(figsize=(8, 6))
            plt.title(f"{metric.capitalize()} Distribution for Regex Complexity: {complexity}")

            # Violin plot
            sns.violinplot(
                data=subset,
                x="engine",
                y=metric,
                inner=None, # Turn off interior bars so they don't conflict with boxplot,
                density_norm="width",
                color="lightblue",
                saturation=0.5
            )

            # Overlay boxplot
            sns.boxplot(
                data=subset,
                x="engine",
                y=metric,
                width=0.3,
                boxprops={'zorder': 2, 'facecolor': 'white'},
                showcaps=True,
                showfliers=False,
                showmeans=True,
                meanprops={
                    "marker": "o",
                    "markerfacecolor": "white",
                    "markeredgecolor": "black",
                    "markersize": "5"
                }
            )

            plt.xlabel("Engine")
            
            if metric == "energy":
                plt.ylabel("Energy (J)")
            else:
                plt.ylabel("Time (s)")

            plt.tight_layout()

            # Build filename and save the figure
            plot_filename = os.path.join(output_dir, f"violin_{metric}_{complexity}.png")
            plt.savefig(plot_filename, dpi=300)
            plt.close()

            print(f"Plot saved to {plot_filename}")

import os
import json
import statistics
from analysis.energy_record import EnergyRecord
from typing import List, Dict, Tuple
from scipy.stats import shapiro

class StatisticsGenerator:
    """
    A class to aggregate and compute statistics for a list of EnergyRecord objects from multiple runs
    that groups by engine and regex_complexity and computes statistics (mean, median, std, min, max, 
    25p, 75p, Shapiro-Wilk p-value) for both time and energy, and outliers.
    Saves results to 'stats.txt' file in the specified results directory.
    """

    def __init__(self, records: List[EnergyRecord], results_dir: str = "results"):
        """
        Parameters:
        - records (List[EnergyRecord]): A list of EnergyRecord objects with time-energy measurements.
        - results_dir (str): Directory to save statistics file.
        """
        self.records = records
        self.results_dir = results_dir

    def generate(self) -> None:
        """
        Orchestrates the statistics generation and saving to file.
        """
        # Generate file path to save stats
        results_file_path = os.path.join(self.results_dir, "stats.txt")
        
        # Group records by engine and regex_complexity
        grouped_records = self._group_records_by_engine_and_complexity()

        # Generate and write stats
        with open(results_file_path, "w", encoding="utf-8") as file:
            for (engine, complexity), recs in grouped_records.items():
                file.write(f"=== Engine: {engine} | Complexity: {complexity} ===\n")

                # Extract time and energy lists
                times = [r.time for r in recs]
                energies = [r.energy for r in recs]

                # Compute statistics
                time_stats, time_outliers_count = self._compute_stats(times)
                energy_stats, energy_outliers_count = self._compute_stats(energies)

                # Build final results structure
                final_results = {
                    "time": time_stats,
                    "energy": energy_stats
                }

                # Write to file
                file.write(json.dumps(final_results, indent=2))
                file.write("\n")
                file.write(f"Outliers for time: {time_outliers_count}\n")
                file.write(f"Outliers for energy: {energy_outliers_count}\n\n")

    def _group_records_by_engine_and_complexity(self) -> Dict[Tuple[str, str], list]:
        """
        Groups input records by engine and regex_complexity.

        Returns:
        - Dict[Tuple[str, str], list]: Dictionary of input records grouped by engine and regex complexity.
        """
        grouped = {}
        for record in self.records:
            key = (record.engine, record.regex_complexity)
            grouped.setdefault(key, []).append(record)
        return grouped

    def _compute_stats(self, values: List[float]) -> Tuple[Dict[str, float], int]:
        """
        Computes stats and outlier counts for a given list of values.

        Parameters:
        - values (List[float]): A list of numerical values (time or energy).
        Returns:
        - Tuple[Dict[str, float], int]: Tuple with dictionary containing computed stats and count of outliers
        """
        if not values:
            return ({
                "shapiro-pvalue": None,
                "mean": None,
                "median": None,
                "std": None,
                "min": None,
                "max": None,
                "25p": None,
                "75p": None
            }, 0)

        # Compute stats
        mean_val = statistics.mean(values)
        median_val = statistics.median(values)
        stdev_val = statistics.pstdev(values) if len(values) > 1 else 0.0
        min_val = min(values)
        max_val = max(values)

        # Compute 25th and 75th percentiles
        q1 = self._percentile(values, 25)
        q3 = self._percentile(values, 75)

        # Perform Shapiro-Wilk test, which requires at least 3 values
        if len(values) >= 3:
            _, shapiro_pvalue = shapiro(values)
        else:
            shapiro_pvalue = None

        # Count outliers
        outliers_count = self._count_outliers_iqr(values)

        stats_dict = {
            "shapiro-pvalue": shapiro_pvalue,
            "mean": mean_val,
            "median": median_val,
            "std": stdev_val,
            "min": min_val,
            "max": max_val,
            "25p": q1,
            "75p": q3
        }

        return stats_dict, outliers_count

    def _count_outliers_iqr(self, values: List[float]) -> int:
        """
        Counts how many outliers are there.

        Paramaters:
        - values (List[float]): A list of numeric values.

        Returns:
        - (int) The number of outliers.
        """
        if len(values) < 4:
            return 0

        q1 = self._percentile(values, 25)
        q3 = self._percentile(values, 75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        outliers = [v for v in values if v < lower_bound or v > upper_bound]
        return len(outliers)

    def _percentile(self, data: List[float], percentile: float) -> float:
        """
        Calculate the given percentile of a list of values.

        Paramaters:
        - data (List[float]): List of numeric values.
        - percentile (float): e.g., 25 for the 25th percentile, 75 for the 75th percentile.
        Returns:
         - float: Percentile value.
        """
        if not data:
            return float('nan')

        sorted_data = sorted(data)
        k = (len(sorted_data) - 1) * (percentile / 100.0)
        f = int(k)
        c = f + 1

        if f == c or c >= len(sorted_data):
            return sorted_data[f]

        # Linear interpolation between points
        d0 = sorted_data[f] * (c - k)
        d1 = sorted_data[c] * (k - f)
        return d0 + d1

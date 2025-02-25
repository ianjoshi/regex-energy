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

    def __init__(self, records: List[EnergyRecord], results_dir: str = "results", outlier_method: str = "zscore"):
        """
        Parameters:
        - records (List[EnergyRecord]): A list of EnergyRecord objects with time-energy measurements.
        - results_dir (str): Directory to save statistics file.
        """
        self.records = records
        self.results_dir = results_dir
        self.outlier_method = outlier_method

    def generate(self) -> None:
        """
        Orchestrates the statistics generation and saving to file.
        """
        # Generate file path to save stats
        results_file_path = os.path.join(self.results_dir, "stats.txt")
        
        # Group records by engine and regex_complexity
        grouped_records = self._group_records_by_engine_and_complexity()

        valid_records = []

        # Generate and write stats
        with open(results_file_path, "w", encoding="utf-8") as file:
            for (engine, complexity), recs in grouped_records.items():
                file.write(f"=== Engine: {engine} | Complexity: {complexity} ===\n")

                # Extract time and energy lists
                times = [r.time for r in recs]
                energies = [r.energy for r in recs]

                if self.outlier_method == "zscore":
                    times_filtered, times_outliers = self.__remove_outliers_zscore(times)
                    energies_filtered, energies_outliers = self.__remove_outliers_zscore(energies)
                elif self.outlier_method == "iqr":
                    times_filtered, times_outliers = self._remove_outliers_iqr(times)
                    energies_filtered, energies_outliers = self._remove_outliers_iqr(energies)

                # Compute statistics
                time_stats = self._compute_stats(times_filtered)
                energy_stats = self._compute_stats(energies_filtered)

                # Build final results structure
                final_results = {
                    "time": time_stats,
                    "energy": energy_stats
                }

                # Write to file
                file.write(json.dumps(final_results, indent=2))
                file.write("\n")
                file.write(f"Outliers for time: {times_outliers}\n")
                file.write(f"Outliers for energy: {energies_outliers}\n\n")

                # Add valid records
                valid_records.extend([r for r in recs if r.time in times_filtered and r.energy in energies_filtered])

        return valid_records

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

        return stats_dict
    
    def __remove_outliers_zscore(self, values: List[float]) -> Tuple[List[float], int]:
        """
        Removes the outliers from the records.

        Paramaters:
        - values (List[float]): A list of numeric values.

        Returns:
        - Tuple[List[float], int]: A list of values with outliers removed and their count.
        """
        if len(values) < 3:
            return 0

        mean_val = statistics.mean(values)
        stdev_val = statistics.pstdev(values)
        filtered_values = [v for v in values if abs(v - mean_val) <= 3 * stdev_val]
        return filtered_values, len(values) - len(filtered_values)

    def _remove_outliers_iqr(self, values: List[float]) -> Tuple[List[float], int]:
        """
        Removes the outliers from the records.

        Paramaters:
        - values (List[float]): A list of numeric values.

        Returns:
        - Tuple[List[float], int]: A list of values with outliers removed and their count.
        """
        if len(values) < 4:
            return 0

        q1 = self._percentile(values, 25)
        q3 = self._percentile(values, 75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        filtered_values = [v for v in values if lower_bound <= v <= upper_bound]
        return filtered_values, len(values) - len(filtered_values)

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

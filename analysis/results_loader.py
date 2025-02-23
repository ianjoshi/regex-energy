import os
import pandas as pd
from analysis.energy_record import EnergyRecord
from typing import List

class ResultsLoader:
    """
    A class for loading and processing benchmark results from CSV files.
    This class extracts energy consumption results, computes execution time and energy
    based on the recorded energy measurements, and loads them into energy records.
    """
    def __init__(self, results_dir: str = "results"):
        """
        Initializes the ResultsLoader with a specified directory containing CSV results.

        Parameters:
        - results_dir (str): Path to the directory containing result CSV files.
        """
        self.results_dir = results_dir

    def parse_filename(self, filename: str):
        """
        Extracts metadata from the filename of a results CSV file.
        The filename is expected to follow the format:
        "engine_<engine_type>_<engine_size>_complexity_<complexity_level>_run_<run_number>.csv"
        
        Parameters:
        - filename (str): Name of the CSV file.

        Returns:
        - tuple: (engine (str), regex_complexity (str), run (int))
        """
        parts = filename.replace(".csv", "").split("_")
        engine = f"{parts[1]}"
        regex_complexity = f"{parts[4]}"
        run = int(parts[6]) 
        return engine, regex_complexity, run

    def load_results(self) -> List[EnergyRecord]:
        """
        Loads all benchmark results from CSV files in the results directory to Energy Records.
        
        Returns:
        - List[EnergyRecord]: A list of EnergyRecord instances containing the parsed results.
        """
        records = []
        for file in os.listdir(self.results_dir):
            if file.endswith(".csv"):
                engine, regex_complexity, run = self.parse_filename(file)
                file_path = os.path.join(self.results_dir, file)

                # Load CSV file into DataFrame
                df = pd.read_csv(file_path)

                # Compute execution time and energy consumption
                time_start, time_end = df.iloc[0]['Time'], df.iloc[-1]['Time']
                energy_start, energy_end = df.iloc[0]['PACKAGE_ENERGY (J)'], df.iloc[-1]['PACKAGE_ENERGY (J)']

                time_diff = (time_end - time_start) / 1000
                energy_diff = energy_end - energy_start

                record = EnergyRecord(engine, regex_complexity, run, time_diff, energy_diff)
                records.append(record)

        return records

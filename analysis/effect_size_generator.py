import os
import json
import numpy as np
from itertools import combinations
from typing import List, Dict, Tuple

class EffectSizeGenerator:
    """
    A class to compute effect sizes between regex engines for time and energy metrics,
    grouped by regex complexity.
    """
    
    def __init__(self, records: List):
        """
        Initializes the EffectSizeGenerator.
        
        Parameters:
        - records (List): A list of EnergyRecord objects containing time-energy measurements.
        """
        self.records = records
        self.grouped_data = self._group_by_engine_and_complexity()

    def _group_by_engine_and_complexity(self) -> Dict[Tuple[str, str], Dict[str, List[float]]]:
        """
        Groups input records by engine and regex complexity.
        
        Returns:
        - Dict[Tuple[str, str], Dict[str, List[float]]]: Grouped time and energy data.
        """
        grouped = {}
        for record in self.records:
            key = (record.regex_complexity, record.engine)
            if key not in grouped:
                grouped[key] = {'time': [], 'energy': []}
            grouped[key]['time'].append(record.time)
            grouped[key]['energy'].append(record.energy)
        return grouped

    def _compute_effect_sizes(self, data_by_engine: Dict[str, Dict[str, List[float]]]) -> Dict:
        """
        Computes effect sizes (mean difference, percent change, Cohen's d) between engines.
        
        Parameters:
        - data_by_engine (Dict[str, Dict[str, List[float]]]): Grouped data by engine.
        
        Returns:
        - Dict: Effect sizes between engine pairs for both time and energy.
        """
        effect_sizes = {}
        engines = list(data_by_engine.keys())
        for engine1, engine2 in combinations(engines, 2):
            for metric in ["time", "energy"]:
                values1 = np.array(data_by_engine[engine1][metric])
                values2 = np.array(data_by_engine[engine2][metric])
                mean_diff = np.mean(values1) - np.mean(values2)
                percent_change = ((np.mean(values1) - np.mean(values2)) / np.mean(values2)) * 100
                pooled_std = np.sqrt(((len(values1) - 1) * np.var(values1, ddof=1) + (len(values2) - 1) * np.var(values2, ddof=1)) / (len(values1) + len(values2) - 2))
                cohens_d = mean_diff / pooled_std if pooled_std > 0 else np.nan
                
                effect_sizes.setdefault((engine1, engine2), {})[metric] = {
                    "mean_diff": mean_diff,
                    "percent_change": percent_change,
                    "cohens_d": cohens_d
                }
        return effect_sizes

    def generate(self, output_dir="results/effect_size") -> None:
        """
        Generates effect sizes and saves results to text files.

        Parameters:
        - output_dir (str): Directory to save the resulting txt files.
        """
        # Create the output directory if it does not exist
        os.makedirs(output_dir, exist_ok=True)

        complexity_groups = {}
        for (regex_complexity, engine), data in self.grouped_data.items():
            if regex_complexity not in complexity_groups:
                complexity_groups[regex_complexity] = {}
            complexity_groups[regex_complexity][engine] = data
        
        for complexity, data_by_engine in complexity_groups.items():
            effect_sizes = self._compute_effect_sizes(data_by_engine)
            
            output = []
            for (engine1, engine2), metrics in effect_sizes.items():
                output.append(f"=== Effect Size: {engine1} vs {engine2} ===")
                output.append(json.dumps(metrics, indent=2))
                output.append("")
            
            with open(f"{output_dir}/{complexity}.txt", "w") as f:
                f.write("\n".join(output))

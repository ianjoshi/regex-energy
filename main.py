from energy_experiment import EnergyExperiment
from analysis.energy_analysis import EnergyAnalysis
import os
import sys


if __name__ == "__main__":

    # Verify that 'data/corpus.txt' exists
    if not os.path.exists("data/corpus.txt"):
        print("Error: 'data/corpus.txt' not found.")
        print("Please generate a corpus by running 'corpus_generator.py'. This will require a WIFI connection and should be done before running the experiment.")
        sys.exit(1)

    # Create an instance of the experiment
    experiment = EnergyExperiment()
    
    # Run the experiment with default parameters
    experiment.run_experiment()

    # Create an instance of the energy analysis
    analysis = EnergyAnalysis()

    # Run the energy analysis
    analysis.run()
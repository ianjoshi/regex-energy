from corpus_generator import CorpusGenerator
from energy_experiment import EnergyExperiment

if __name__ == "__main__":

    # # Create an instance of the corpus generator
    # corpus_generator = CorpusGenerator()

    # # Generate corpus files for the experiment
    # corpus_generator.generate_corpus_files()

    # Create an instance of the experiment
    experiment = EnergyExperiment()
    
    # Run the experiment with default parameters
    experiment.run_experiment()
import argparse
import pickle
from run_regex_engines import RegexEnginesExecutor

class RegexRunner:
    """
    A class to manage the execution of regex matching using different regex engines.
    """

    def __init__(self, corpus, engine, pattern, save_state_path="regex_engine_state.pkl"):
        """
        Initializes the RegexRunner with the specified corpus, engine, and pattern.
        
        Parameters:
        - corpus (str): Path to the text corpus file.
        - engine (str): Name of the regex engine to be used.
        - pattern (str): Regex pattern to be matched.
        - save_state_path (str, optional): Path to save the engine state.
        """
        self.corpus = corpus
        self.engine = engine
        self.pattern = pattern
        self.save_state_path = save_state_path
        self.regex_engine_executor = RegexEnginesExecutor(
            regex_engine=self.engine,
            corpus=self.corpus,
            pattern=self.pattern
        )

    def setup_engine(self):
        """
        Sets up the regex engine and saves its state for future use.
        """
        # Initialize the regex engine
        self.regex_engine_executor.setUp()

        # Save the state of the regex engine to a pickle file
        with open(self.save_state_path, "wb") as f:
            pickle.dump(self.regex_engine_executor, f)

        print(f"Regex engine setup completed and saved to {self.save_state_path}.")

    def run_matching(self):
        """
        Loads the saved regex engine state and runs pattern matching.
        """
        try:
            # Load the saved state of the regex engine
            with open(self.save_state_path, "rb") as f:
                self.regex_engine_executor = pickle.load(f)
        except FileNotFoundError:
            raise RuntimeError("Regex engine has not been set up. Run with --setup first.")
        
         # Get the method name for the regex engine execution
        method_name = RegexEnginesExecutor.engine_methods.get(self.engine)
        if method_name is None:
            raise ValueError(f"Unknown regex engine: {self.engine}")
        
        # Run the regex matching using the retrieved method name
        output = getattr(self.regex_engine_executor, method_name)()
        print("Found matches:", output)

if __name__ == "__main__":
    # Set up argument parser for command-line interaction
    parser = argparse.ArgumentParser(description="Run regex matching with a chosen regex engine.")
    parser.add_argument("--corpus", required=True, help="Path to the corpus file.")
    parser.add_argument("--engine", required=True, help="Name of the regex engine.")
    parser.add_argument("--pattern", required=True, help="Regex pattern to be used for matching.")
    parser.add_argument("--setup", action="store_true", help="Initialize the regex engine.")
    parser.add_argument("--match", action="store_true", help="Run regex matching.")

    args = parser.parse_args()

    # Instantiate the RegexRunner with provided arguments
    runner = RegexRunner(corpus=args.corpus, engine=args.engine, pattern=args.pattern)

    # Handle setup and matching operations based on command-line arguments
    if args.setup:
        runner.setup_engine()
    elif args.match:
        runner.run_matching()
    else:
        print("Please provide --setup or --match.")

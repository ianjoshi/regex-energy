import argparse
from run_regex_engines import RegexEnginesExecutor

def regex_matching(corpus, engine, pattern):
    # Create an instance of the RegexEnginesExecutor
    regex_engine_executor = RegexEnginesExecutor(
        regex_engine=engine,
        corpus=corpus,
        pattern=pattern
    )

    # Set up the regex engine
    regex_engine_executor.setUp()

    # Retrieve the method name from the dictionary and call it dynamically
    method_name = RegexEnginesExecutor.engine_methods.get(engine)
    if method_name is None:
        raise ValueError(f"Unknown regex engine: {engine}")

    # Call the method dynamically using `getattr`
    output = getattr(regex_engine_executor, method_name)()
    print("Found matches:", output)

    # regex_engine_executor.tearDown()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run regex matching with a chosen regex engine.")
    parser.add_argument("--corpus", required=True, help="Path to the corpus file.")
    parser.add_argument("--engine", required=True, help="Name of the regex engine.")
    parser.add_argument("--pattern", required=True, help="Regex pattern to be used for matching.")

    args = parser.parse_args()

    # Pass the arguments to the regex_matching function
    regex_matching(corpus=args.corpus, engine=args.engine, pattern=args.pattern)

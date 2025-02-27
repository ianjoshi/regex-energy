import os
import time
import random
from energibridge_executor import EnergibridgeExecutor

# Define the engines, file sizes, and regex patterns to be used in the experiment
engines = ["engine_dotnet", "engine_java", "engine_js", "engine_cpp"]
file_sizes = ["corpus"]
regex_complexities = {"complexity_low": r"def", "complexity_medium": r"\bclass\s+\w+", "complexity_high": r"(?<=def\s)\w+(?=\()"}

class EnergyExperiment:
    """
    A class for running controlled performance measurement experiments on a system.
    The experiment includes a warm-up phase, task execution, and rest periods between runs.
    """

    def __init__(self, num_runs=30, warmup_duration=300, rest_duration=60, engines=engines, file_sizes=file_sizes, regex_complexities=regex_complexities):
        """
        Initializes the experiment with the necessary parameters.

        Parameters:
        - num_runs (int): Number of times each task should be executed.
        - warmup_duration (int): Warm-up period (in seconds) before measurements.
        - rest_duration (int): Rest period (in seconds) between runs.
        """
        self.num_runs = num_runs
        self.warmup_duration = warmup_duration
        self.rest_duration = rest_duration
        self.engines = engines
        self.file_sizes = file_sizes
        self.regex_complexities = regex_complexities

        self.energibridge = EnergibridgeExecutor()

        # Dictionary of tasks for experiment
        self.tasks = {}

    def generate_tasks(self):
        """
        Generates a combination of all possible tasks for the experiment,
        and writes each as a separate .py file in the 'tasks' folder.
        """
        # Ensure we have a tasks/ folder
        if not os.path.exists("tasks"):
            os.makedirs("tasks")

        # Create tasks for each combination of engine, file size, and regex complexity
        for engine in self.engines:
            for file_size in self.file_sizes:
                for regex_complexity, pattern in self.regex_complexities.items():
                    task_name = f"{engine}_{file_size}_{regex_complexity}"

                    # Store task in list
                    self.tasks[task_name] = (f"data/{file_size}.txt", engine, rf"{pattern}")

    def run_experiment(self):
        """
        Orchestrates and runs the experiment sequence:
        1. Warns the user and prepares the environment.
        2. Warms up the CPU by running Fibonacci calculations.
        3. Runs each task multiple times in a shuffled order with rest intervals.
        """
        self.generate_tasks()

        if not self.tasks:
            raise ValueError("No tasks have been set.")

        self._warn_and_prepare()
        self._warmup_fibonacci()

        self.energibridge.start_service()

        # Create a list of (task_name, task, run_index) tuples for shuffling
        task_run_list = [(name, task, i + 1) for name, task in self.tasks.items() for i in range(self.num_runs)]
        random.shuffle(task_run_list)  # Shuffle task execution order

        for run_index, (task_name, (corpus, engine, pattern), run_id) in enumerate(task_run_list, 1):
            print(f"----- Run {run_index} (Task: {task_name}, Instance: {run_id}) -----")

            # If the results folder does not exist, create it
            if not os.path.exists("results"):
                os.makedirs("results")

            output_file = f"results/{task_name}_run_{run_id}.csv"

            # Prepare regex matching task
            self.energibridge.prepare_task(corpus=corpus, engine=engine, pattern=pattern)

            # Run energy measurement with task
            self.energibridge.run_measurement(corpus=corpus, engine=engine, pattern=pattern, output_file=output_file)

            # Rest between runs except for the last iteration
            if run_index < len(task_run_list):
                print(f"Resting for {self.rest_duration} seconds before the next run...")
                time.sleep(self.rest_duration)

        self.energibridge.stop_service()
        print("Experiment complete.")

    def _warn_and_prepare(self):
        """Provides instructions to the user to optimize system conditions before running the experiment."""
        print("WARNING: Before proceeding, please:")
        print("- Close all unnecessary applications.")
        print("- Kill unnecessary services.")
        print("- Turn off notifications.")
        print("- Disconnect any unnecessary hardware.")
        print("- Disconnect Wi-Fi.")
        print("- Switch off auto-brightness on your display.")
        print("- Set room temperature (if possible) to 25°C. Else stabilize room temperature if possible.")
        print("Press Enter to continue once the environment is ready.")
        input()

    def _warmup_fibonacci(self):
        """Runs Fibonacci calculations continuously for a specified duration to warm up the CPU."""
        print(f"Starting Fibonacci warm-up for {self.warmup_duration} seconds...")
        start_time = time.time()

        while time.time() - start_time < self.warmup_duration:
            # Compute Fibonacci of 30 repeatedly
            self._fib(30) 

        print("Warm-up complete.")

    def _fib(self, n):
        """Computes the nth Fibonacci number iteratively."""
        if n <= 1:
            return n
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
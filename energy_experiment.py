import time
import random
from energibridge_executor import EnergibridgeExecutor

# engines = ["engine_py", "engine_cpp", "engine_js", "engine_java"]
# file_sizes = ["size_small", "size_medium", "size_large"]
# regex_complexities = ["complexity_low", "complexity_medium", "complexity_high"]
engines = ["engine_py"]
file_sizes = ["size_small"]
regex_complexities = ["complexity_low", "complexity_medium"]

class EnergyExperiment:
    """
    A class for running controlled performance measurement experiments on a system.
    The experiment includes a warm-up phase, task execution, and rest periods between runs.
    """

    def __init__(self, num_runs=2, warmup_duration=10, rest_duration=5, measurement_duration=10, engines=engines, file_sizes=file_sizes, regex_complexities=regex_complexities):
        """
        Initializes the experiment with the necessary parameters.

        Parameters:
        - num_runs (int): Number of times each task should be executed.
        - warmup_duration (int): Warm-up period (in seconds) before measurements.
        - rest_duration (int): Rest period (in seconds) between runs.
        - measurement_duration (int): Maximum duration of each measurement in seconds.
        """
        self.num_runs = num_runs
        self.warmup_duration = warmup_duration
        self.rest_duration = rest_duration
        self.engines = engines
        self.file_sizes = file_sizes
        self.regex_complexities = regex_complexities

        self.energibridge = EnergibridgeExecutor(max_measurement_duration=measurement_duration)

        # Dictionary mapping task names to functions for experiment
        self.tasks = {}

    def generate_tasks(self):
        """
        Generates a combination of all possible tasks for the experiment.
        """
        for engine in self.engines:
            for file_size in self.file_sizes:
                for regex_complexity in self.regex_complexities:
                    task_name = f"{engine}_{file_size}_{regex_complexity}"
                    self.tasks[task_name] = lambda: regex_matching(engine, file_size, regex_complexity)

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

        # Create a list of (task_name, task_function, run_index) tuples for shuffling
        task_run_list = [(name, func, i + 1) for name, func in self.tasks.items() for i in range(self.num_runs)]
        random.shuffle(task_run_list)  # Shuffle task execution order

        for run_index, (task_name, task_func, run_id) in enumerate(task_run_list, 1):
            print(f"----- Run {run_index} (Task: {task_name}, Instance: {run_id}) -----")
            output_file = f"results/{task_name}_run_{run_id}.csv"

            task_func()  # Execute the task
            self.energibridge.run_measurement(output_file=output_file)

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
            self._fib(30)  # Compute Fibonacci of 30 repeatedly

        print("Warm-up complete.")

    def _fib(self, n):
        """Computes the nth Fibonacci number iteratively."""
        if n <= 1:
            return n
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
    
def regex_matching(engine, file_size, regex_complexity):
    print(f"Running task: {engine}, {file_size}, {regex_complexity}")
    time.sleep(2)

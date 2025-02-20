import time
import random
from energibridge_executor import EnergibridgeExecutor

class EnergyExperiment:
    """
    A class for running controlled performance measurement experiments on a system.
    The experiment includes a warm-up phase, task execution, and rest periods between runs.
    """

    def __init__(self, num_runs=30, warmup_duration=300, rest_duration=60, measurement_duration=10):
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
        self.energibridge = EnergibridgeExecutor(max_measurement_duration=measurement_duration)

        # Dictionary mapping task names to functions for experiment
        self.tasks = {
             "placeholder_task_a" : placeholder_task_a,
             "placeholder_task_b": placeholder_task_b
        }

    def run_experiment(self):
        """
        Orchestrates and runs the experiment sequence:
        1. Warns the user and prepares the environment.
        2. Warms up the CPU by running Fibonacci calculations.
        3. Runs each task multiple times in a shuffled order with rest intervals.
        """
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
    
# TODO: Remove once concrete tasks are implemented
def placeholder_task_a():
    print("Running placeholder task A...")
    time.sleep(2)

def placeholder_task_b():
    print("Running placeholder task B...")
    time.sleep(4)
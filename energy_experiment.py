from energibridge_executor import EnergibridgeExecutor
import time

class EnergyExperiment:
    """
    A class for running controlled performance measurement experiments on a system.
    The experiment includes a warm-up phase, task execution, and rest periods between runs.
    """
    def __init__(self, num_runs=30, warmup_duration=300, rest_duration=60, measurement_duration=10):
        """
        Initializes the experiment with the necessary parameters.

        Parameters:
        - num_runs (int): Number of times the task measurement should be executed.
        - warmup_duration (int): Warm up period (in seconds) before measurements.
        - rest_duration (int): Rest period (in seconds) between runs.
        - measurement_duration (int): Maximum duration of each measurement in seconds.
        """
        self.num_runs = num_runs
        self.warmup_duration = warmup_duration
        self.rest_duration = rest_duration
        self.energibridge = EnergibridgeExecutor(max_measurement_duration=measurement_duration)

    def run_experiment(self):
        """
        Orchestrates and runs the experiment sequence:
        1. Warns the user and prepares the environment.
        2. Warms up the CPU by running Fibonacci calculations.
        3. Runs the task measurement multiple times with rest intervals.
        """
        self._warn_and_prepare()
        self._warmup_fibonacci()
        self.energibridge.start_service()

        for i in range(self.num_runs):
            print(f"----- Run {i+1} of {self.num_runs} -----")

            self._run_task()
            self.energibridge.run_measurement()

            # Rest between runs except for the last iteration
            if i < self.num_runs - 1:
                print(f"Resting for {self.rest_duration} seconds before the next run...")
                time.sleep(self.rest_duration)

        self.energibridge.stop_service()
        print("Experiment complete.")

    def _warn_and_prepare(self):
        """
        Provides instructions to the user to optimize system conditions before running the experiment.
        Ensures that external factors (e.g., background tasks, notifications, hardware interference)
        do not affect the measurements.
        """
        print("WARNING: Before proceeding, please:")
        print("- Close all unnecessary applications.")
        print("- Kill unnecessary services.")
        print("- Turn off notifications.")
        print("- Disconnect any unnecessary hardware.")
        print("- Disconnect Wi-Fi.")
        print("- Switch off auto-brightness on your display.")
        print("- Set room temperature (if possible) to 25°C. Else stabalize room temperature it possible.")
        print("Press Enter to continue once the environment is ready.")
        input()

    def _warmup_fibonacci(self):
        """
        Runs Fibonacci calculations continuously for a specified duration to warm up the CPU.
        """
        print(f"Starting Fibonacci warm-up for {self.warmup_duration} seconds...")
        start_time = time.time()

        # Continuously calculate Fibonacci numbers until the warm-up duration is reached
        while time.time() - start_time < self.warmup_duration:
            self._fib(30)  # Compute Fibonacci of 30 repeatedly

        print("Warm-up complete.")

    def _fib(self, n):
        """
        Computes the nth Fibonacci number iteratively.
        
        Parameters:
        - n (int): The Fibonacci sequence index.
        
        Returns:
        - int: The nth Fibonacci number.
        """
        if n <= 1:
            return n
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

    def _run_task(self):
        """
        Placeholder method for running the actual task that needs performance measurement.
        """
        pass
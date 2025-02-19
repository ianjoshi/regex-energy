import time

class EnergiBridgeExperiment:
    """
    A class for running controlled performance measurement experiments on a system.
    The experiment includes a warm-up phase, task execution, and rest periods between runs.
    """

    def run_experiment(self, num_runs=30, rest_duration=60):
        """
        Orchestrates and runs the experiment sequence:
        1. Warns the user and prepares the environment.
        2. Warms up the CPU by running Fibonacci calculations.
        3. Runs the task measurement multiple times with rest intervals.
        
        Parameters:
        - num_runs (int): Number of times the task measurement should be executed.
        - rest_duration (int): Rest period (in seconds) between runs.
        """
        self._warn_and_prepare()
        self._warmup_fibonacci()

        for i in range(num_runs):
            print(f"----- Run {i+1} of {num_runs} -----")
            self._run_task_and_measurement()

            # Rest between runs except for the last iteration
            if i < num_runs - 1:
                print(f"Resting for {rest_duration} seconds before the next run...")
                time.sleep(rest_duration)

        print("Experiment complete.")

    def _warn_and_prepare(self):
        """
        Provides instructions to the user to optimize system conditions before running the experiment.
        Ensures that external factors (e.g., background tasks, notifications, hardware interference)
        do not affect the measurements.
        """
        print("WARNING: Before proceeding, please:")
        print("- Close all unnecessary applications.")
        print("- Turn off notifications.")
        print("- Disconnect any unnecessary hardware.")
        print("- Kill unnecessary services.")
        print("- Disconnect Wi-Fi (if your measurement does not require it).")
        print("- Switch off auto-brightness on your display.")
        print("- Set room temperature (if possible) to 20°C. Else stabalize room temperature.")
        print("Press Enter to continue once the environment is ready.")
        input()

    def _warmup_fibonacci(self, warmup_duration=300):
        """
        Runs Fibonacci calculations continuously for a specified duration to warm up the CPU.
        
        Parameters:
        - warmup_duration (int): Duration (in seconds) for which the CPU warm-up should run.
        """
        print(f"Starting Fibonacci warm-up for {warmup_duration} seconds...")
        start_time = time.time()

        # Continuously calculate Fibonacci numbers until the warm-up duration is reached
        while time.time() - start_time < warmup_duration:
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

    def _run_task_and_measurement(self):
        """
        Placeholder method for running the actual task that needs performance measurement.
        To be implemented with specific measurement logic based on the experiment requirements.
        """
        pass
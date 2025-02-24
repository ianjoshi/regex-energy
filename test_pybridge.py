import time
from pyEnergiBridge.api import EnergiBridgeRunner
from energibridge_executor import EnergibridgeExecutor

executor = EnergibridgeExecutor()
executor.start_service()

runner = EnergiBridgeRunner(max_duration=10)
runner.start(results_file="results.csv")

# Perform some task
time.sleep(10)

# Stop the data collection and retrieve results
energy, duration = runner.stop()
print(f"Energy consumption (J): {energy}; Execution time (s): {duration}")

executor.stop_service()
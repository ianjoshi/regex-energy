import subprocess
import time

class EnergiBridgeExecutor:
    """
    A class to handle the execution of EnergiBridge commands for energy measurements.
    """
    def __init__(self, output_file="results/results.csv", max_measurement_duration=10):
        """
        Initializes the EnergiBridgeExecutor with output file and duration.
        
        Parameters:
        - output_file (str): Path to store the measurement results.
        - max_measurement_duration (int): Maximum duration in seconds for measurement.
        """
        self.output_file = output_file
        self.max_measurement_duration = max_measurement_duration
        self.rapl_service = "rapl"
        self.driver_path = "energibridge/LibreHardwareMonitor.sys"
        self.energibridge_exe = "energibridge/energibridge"
    
    def _run_command(self, command):
        """
        Executes a command in the system shell.
        
        Parameters:
        - command (str): The command to execute.
        
        Returns:
        - str: Output of the command execution.
        """
        try:
            command = f"powershell -Command \"Start-Process cmd -ArgumentList '/c {command}' -Verb RunAs\""
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            print(result.stderr.strip())
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {command}\n{e.stderr}")
            return None

    def start_service(self):
        """
        Starts the EnergiBridge service by creating and starting the RAPL driver.
        """
        print("Starting EnergiBridge service...")
        self._run_command(f'sc.exe create {self.rapl_service} type=kernel binPath="{self.driver_path}"')
        self._run_command(f'sc.exe start {self.rapl_service}')
        time.sleep(5)  # Wait for service to start

    def stop_service(self):
        """
        Stops the EnergiBridge service.
        """
        print("Stopping EnergiBridge service...")
        self._run_command(f'sc.exe stop {self.rapl_service}')
        self._run_command(f'sc.exe delete {self.rapl_service}')

    def run_measurement(self):
        """
        Runs EnergiBridge measurement and stores the results in the specified file.
        """
        print(f"Running measurement...")
        self._run_command(f'{self.energibridge_exe} -o {self.output_file} --summary timeout {self.max_measurement_duration}')
        print("Measurement complete.")

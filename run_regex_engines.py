from regex_engine_factory import RegexEngineFactory
import subprocess
import re
import os
from dotenv import load_dotenv
from pyEnergiBridge.api import EnergiBridgeRunner

class RegexEnginesExecutor:
    """
    Class to execute the different regex engines.
    """

    # Dictionary to map the engine name to the method to execute
    engine_methods = {
        "engine_py": "run_python_engine",
        "engine_java": "run_java_engine",
        "engine_js": "run_javascript_engine",
        "engine_cpp": "run_boost_engine",
        "engine_dotnet": "run_dotnet_engine"
    }

    def __init__(self, regex_engine, corpus, pattern, energy_bridge_runner : EnergiBridgeRunner):
        """
        Initialize the class with the regex engine to use, the corpus file and the pattern to match.
        """
        self.regex_engine = regex_engine
        self.corpus = corpus
        self.pattern = pattern
        self.energy_bridge_runner = energy_bridge_runner

    def setUp(self):
        """
        Set up the regex engines.
        """
        self.factory = RegexEngineFactory(
            regular_expressions=[self.pattern],
            directory_to_store_engines="regex_engines",
            filepath_to_corpus=self.corpus
        )
        self.factory.create_engines()

    def tearDown(self):
        """
        Tear down the regex engines.
        """
        self.factory.destroy_engines()

    def run_python_engine(self):
        """
        Run the regex engine in Python.
        """
        with open(self.corpus, "r") as file:
            content = file.read()
            matches = re.findall(self.pattern, content)
            output = f'Pattern 0: {self.pattern} - Matches: {len(matches)}'
        return [output]

    def run_java_engine(self, output_file):
        """
        Run the regex engine in Java.
        """
        # Compile and start Java process
        subprocess.run(["javac", f"{self.factory.directory_to_store_engines}/RegexMatcher.java"])
        java_process = subprocess.Popen(
            ["java", "-cp", self.factory.directory_to_store_engines, "RegexMatcher"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for ready signal
        line = java_process.stdout.readline().strip()
        
        # Send start signal and get output
        self.energy_bridge_runner.start(results_file=output_file)
        stdout, stderr = java_process.communicate(input="start\n")
        self.energy_bridge_runner.stop()
        
        # Process output
        output_lines = []
        if stdout:
            lines = stdout.splitlines()
            for line in lines:
                if line.strip() and line.strip() != "done":
                    output_lines.append(line)
        
        if stderr:
            print(f"Java process stderr: {stderr}")
        
        return output_lines

    def run_javascript_engine(self, output_file):
        """
        Run the regex engine in JavaScript.
        """
        # Start Node.js process
        node_process = subprocess.Popen(
            ["node", f"{self.factory.directory_to_store_engines}/regex_matcher.js"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for ready signal
        line = node_process.stdout.readline().strip()
        
        # Send start signal and get output
        self.energy_bridge_runner.start(results_file=output_file)
        stdout, stderr = node_process.communicate(input="start\n")
        self.energy_bridge_runner.stop()
        
        # Process output
        output_lines = []
        if stdout:
            lines = stdout.splitlines()
            for line in lines:
                if line.strip() and line.strip() != "done":
                    output_lines.append(line)
        
        if stderr:
            print(f"JavaScript process stderr: {stderr}")
        
        return output_lines

    def run_boost_engine(self, output_file):
        """
        Run the regex engine in C++ using Boost.
        """
        # Load the Boost path from the environment
        load_dotenv()
        boost_path = os.getenv("BOOST_PATH")
        if not boost_path:
            raise RuntimeError("BOOST_PATH environment variable not set.")
        
        # Compile C++ code
        compile_result = subprocess.run([
            "g++",
            f"{self.factory.directory_to_store_engines}/regex_matcher.cpp",
            "-o", f"{self.factory.directory_to_store_engines}/regex_matcher.exe",
            f"-I{boost_path}/include",
            f"-L{boost_path}/lib",
            "-Wl,-rpath," + boost_path + "/bin",
            "-lboost_regex-vc143-mt-x64-1_86",  # Exact library name without 'lib' prefix and '.dll.a' suffix
            "--verbose"
        ], capture_output=True, text=True)
        
        # Check if compilation was successful
        if compile_result.returncode != 0:
            print("Library path contents:")
            subprocess.run(["dir", f"{boost_path}/lib"], shell=True)
            raise RuntimeError(f"C++ compilation failed:\n{compile_result.stderr}")
        
        # Start C++ process
        cpp_process = subprocess.Popen(
            f"{self.factory.directory_to_store_engines}/regex_matcher.exe",
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for ready signal
        line = cpp_process.stdout.readline().strip()
        
        # Send start signal and get output
        self.energy_bridge_runner.start(results_file=output_file)
        stdout, stderr = cpp_process.communicate(input="start\n")
        self.energy_bridge_runner.stop()
        
        # Process output
        output_lines = []
        if stdout:
            lines = stdout.splitlines()
            for line in lines:
                if line.strip() and line.strip() != "done":
                    output_lines.append(line)
        
        if stderr:
            print(f"C++ process stderr: {stderr}")
        
        return output_lines
    
    def run_dotnet_engine(self, output_file):
        """
        Run the regex engine in .NET using csc (C# compiler).
        """
        # Compile the C# code using csc
        compile_result = subprocess.run(
            ["csc",
             "-out:"
             + os.path.abspath(f"{self.factory.directory_to_store_engines}/RegexMatcher.exe"),
             os.path.abspath(f"{self.factory.directory_to_store_engines}/RegexMatcher.cs")],
            capture_output=True,
            text=True
        )
        
        # Check if compilation was successful
        if compile_result.returncode != 0:
            raise RuntimeError(f".NET compilation failed:\n{compile_result.stderr}")
        
        # Start the .NET process
        dotnet_process = subprocess.Popen(
            [os.path.abspath(f"{self.factory.directory_to_store_engines}/RegexMatcher.exe"),
                self.pattern,
                self.corpus],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for ready signal
        line = dotnet_process.stdout.readline().strip()
        
        # Send start signal and get output
        self.energy_bridge_runner.start(results_file=output_file)
        stdout, stderr = dotnet_process.communicate(input="start\n")
        self.energy_bridge_runner.stop()
        
        # Process output
        output_lines = []
        if stdout:
            lines = stdout.splitlines()
            for line in lines:
                if line.strip() and line.strip() != "done":
                    output_lines.append(line)
        
        if stderr:
            print(f".NET process stderr: {stderr}")
        
        return output_lines
    
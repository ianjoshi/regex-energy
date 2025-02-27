import os
import unittest
import time
from regex_engine_factory import RegexEngineFactory
import subprocess
from dotenv import load_dotenv

class TestRegexEngines(unittest.TestCase):
    def setUp(self):
        self.test_patterns = {"hello": 0, "Pickles": 1, ".*?ick.*?": 3}
        self.factory = RegexEngineFactory(
            regular_expressions=list(self.test_patterns.keys()),
            directory_to_store_engines="test_engines",
            filepath_to_corpus="data/test_corpus.txt"
        )
        self.factory.create_engines()

    def tearDown(self):
        self.factory.destroy_engines()

    # To run this test, you need to have Java installed.
    def test_java_engine_pipe_interaction(self):
        # Compile and start Java process
        subprocess.run(["javac", f"{self.factory.directory_to_store_engines}/RegexMatcher.java"])
        java_process = subprocess.Popen(
            ["java", "-cp", self.factory.directory_to_store_engines, "RegexMatcher"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True  # This makes communicate() use strings instead of bytes
        )
        
        # Wait for ready signal
        line = java_process.stdout.readline().strip()
        self.assertEqual(line, "ready")
        
        # Send start signal
        java_process.stdin.write("start\n")
        java_process.stdin.flush()
        
        # Read output until done
        output_lines = []
        while True:
            line = java_process.stdout.readline().strip()
            if line == "done":
                break
            if not line:
                # Check if there was an error
                error = java_process.stderr.read()
                if error:
                    break
            output_lines.append(line)
        
        # Verify output contains expected pattern matches
        for i, pattern in enumerate(self.test_patterns.keys()):
            expected_output = f"Pattern {i}: {pattern} - Matches: {self.test_patterns[pattern]}"
            self.assertTrue(any(expected_output in line for line in output_lines))

        self.assertEqual(java_process.wait(), 0)
    
    # To run this test, you need to have Node.js installed.
    def test_javascript_engine_pipe_interaction(self):
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
        self.assertEqual(line, "ready")
        
        # Send start signal
        node_process.stdin.write("start\n")
        node_process.stdin.flush()
        
        # Read output until done
        output_lines = []
        while True:
            line = node_process.stdout.readline().strip()
            if line == "done":
                break
            if not line:
                # Check if there was an error
                error = node_process.stderr.read()
                if error:
                    break
            output_lines.append(line)
        
        # Verify output contains expected pattern matches
        for i, pattern in enumerate(self.test_patterns.keys()):
            expected_output = f"Pattern {i}: {pattern} - Matches: {self.test_patterns[pattern]}"
            self.assertTrue(any(expected_output in line for line in output_lines))

        self.assertEqual(node_process.wait(), 0)

    # To run this test, you need to have the Boost-regex library installed. And a c++ compiler installed.
    # command: vcpkg install boost-regex:x64-windows
    def test_boost_engine_pipe_interaction(self):
        # Get Boost path from environment
        load_dotenv()
        boost_path = os.getenv("BOOST_PATH") # Depends on vcpkg installation path
        if not boost_path:
            raise ValueError("BOOST_PATH environment variable not set")
        
        # Print the directory contents to debug
        print("Checking library directory:")
        subprocess.run(["dir", f"{boost_path}/lib"], shell=True)
        
        compile_result = subprocess.run([
            "g++", # Depends on compiler
            f"{self.factory.directory_to_store_engines}/regex_matcher.cpp",
            "-o", f"{self.factory.directory_to_store_engines}/regex_matcher.exe",
            f"-I{boost_path}/include",
            f"-L{boost_path}/lib",
            "-Wl,-rpath," + boost_path + "/bin",
            "-lboost_regex-vc143-mt-x64-1_86",  # Depends on compiler
            "--verbose"
        ], capture_output=True, text=True)
        
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
        self.assertEqual(line, "ready")
        
        # Send start signal
        cpp_process.stdin.write("start\n")
        cpp_process.stdin.flush()
        
        # Read output until done
        output_lines = []
        while True:
            line = cpp_process.stdout.readline().strip()
            if line == "done":
                break
            if not line:
                # Check if there was an error
                error = cpp_process.stderr.read()
                if error:
                    break
            output_lines.append(line)
        
        # Verify output contains expected pattern matches
        for i, pattern in enumerate(self.test_patterns.keys()):
            expected_output = f"Pattern {i}: {pattern} - Matches: {self.test_patterns[pattern]}"
            self.assertTrue(any(expected_output in line for line in output_lines))

        self.assertEqual(cpp_process.wait(), 0)


    def test_dotnet_engine_pipe_interaction(self):
        # Compile the C# code using csc
        compile_result_dotnet = subprocess.run(
            ["csc",
             "-out:"
             + os.path.abspath(f"{self.factory.directory_to_store_engines}/RegexMatcher.exe"),
             os.path.abspath(f"{self.factory.directory_to_store_engines}/RegexMatcher.cs")],
            capture_output=True,
            text=True
        )
        
        # Check if compilation was successful
        if compile_result_dotnet.returncode != 0:
            raise RuntimeError(f".NET compilation failed:\n{compile_result_dotnet.stderr}")
        
        # Ensure the .NET executable exists
        dotnet_exe_path = os.path.abspath(f"{self.factory.directory_to_store_engines}/RegexMatcher.exe")
        self.assertTrue(os.path.exists(dotnet_exe_path), "RegexMatcher.exe not found.")

        # Start the .NET process
        dotnet_process = subprocess.Popen(
            [dotnet_exe_path, self.factory.filepath_to_corpus],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for ready signal
        line = dotnet_process.stdout.readline().strip()
        self.assertEqual(line, "ready")
        
        # Send start signal
        dotnet_process.stdin.write("start\n")
        dotnet_process.stdin.flush()
        
        # Read output until done
        output_lines = []
        while True:
            line = dotnet_process.stdout.readline().strip()
            if line == "done":
                break
            if not line:
                # Check if there was an error
                error = dotnet_process.stderr.read()
                if error:
                    break
            output_lines.append(line)
        
        # Verify output contains expected pattern matches
        for i, pattern in enumerate(self.test_patterns.keys()):
            expected_output = f"Pattern {i}: {pattern} - Matches: {self.test_patterns[pattern]}"
            self.assertTrue(any(expected_output in line for line in output_lines))

        self.assertEqual(dotnet_process.wait(), 0)

if __name__ == '__main__':
    unittest.main()

from regex_engine_factory import RegexEngineFactory
import subprocess
import re

class RegexEnginesExecutor:

    engine_methods = {
        "engine_py": "run_python_engine",
        "engine_java": "run_java_engine",
        "engine_js": "run_javascript_engine",
        "engine_cpp": "run_boost_engine",
    }

    def __init__(self, regex_engine, corpus, pattern):
        self.regex_engine = regex_engine
        self.corpus = corpus
        self.pattern = pattern

    def setUp(self):
        self.factory = RegexEngineFactory(
            regular_expressions=[self.pattern],
            filepath_to_corpus=self.corpus
        )
        self.factory.create_engines()

    def tearDown(self):
        self.factory.destroy_engines()

    def run_python_engine(self):
        with open(self.corpus, "r") as file:
            content = file.read()
            matches = re.findall(self.pattern, content)
        return matches

    def run_java_engine(self):
        subprocess.run(["javac", f"{self.factory.directory_to_store_engines}/RegexMatcher.java"])
        java_process = subprocess.Popen(
            ["java", "-cp", self.factory.directory_to_store_engines, "RegexMatcher"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        java_process.stdin.write(f"{self.pattern}\n")
        java_process.stdin.flush()
        output = java_process.stdout.read().strip()
        java_process.wait()
        return output

    def run_javascript_engine(self):
        node_process = subprocess.Popen(
            ["node", f"{self.factory.directory_to_store_engines}/regex_matcher.js"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        node_process.stdin.write(f"{self.pattern}\n")
        node_process.stdin.flush()
        output = node_process.stdout.read().strip()
        node_process.wait()
        return output

    def run_boost_engine(self):
        boost_exe = f"{self.factory.directory_to_store_engines}/regex_matcher.exe"
        boost_process = subprocess.Popen(
            [boost_exe],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        boost_process.stdin.write(f"{self.pattern}\n")
        boost_process.stdin.flush()
        output = boost_process.stdout.read().strip()
        boost_process.wait()
        return output
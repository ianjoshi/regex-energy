import os
import shutil

class RegexEngineFactory:
    def __init__(self, regular_expressions: list[str], directory_to_store_engines: str = 'regex_engines', filepath_to_corpus: str = 'data/corpus.txt'):
        self.regular_expressions = regular_expressions
        self.directory_to_store_engines = directory_to_store_engines
        self.filepath_to_corpus = filepath_to_corpus
        
        # Create named pipes for synchronization
        self.ready_pipe = os.path.join(self.directory_to_store_engines, 'ready_pipe')
        self.start_pipe = os.path.join(self.directory_to_store_engines, 'start_pipe')
        self.done_pipe = os.path.join(self.directory_to_store_engines, 'done_pipe')

    def create_engines(self):
        """
        Create all the engines that will be used to evaluate the matches,
        the engines will be stored as files in the 'self.directory_to_store_engines' directory.
        The different engines will run the 'regular_expressions' list of matches against the 
        'filepath_to_corpus' file.
        """
        if not os.path.exists(self.directory_to_store_engines):
            os.makedirs(self.directory_to_store_engines)
            
        if not os.path.exists(self.filepath_to_corpus):
            print(f"The corpus file '{self.filepath_to_corpus}' does not exist.")
            return
            
        self._create_java_engine()
        self._create_javascript_engine()
        self._create_boost_engine()
    
    def _create_java_engine(self):
        java_code = f"""
import java.io.*;
import java.util.regex.*;
import java.util.List;
import java.util.Arrays;

public class RegexMatcher {{
    public static void main(String[] args) throws IOException {{
        // Load corpus first
        String corpus = readFile("{self.filepath_to_corpus}");
        List<String> patterns = Arrays.asList({", ".join(f'"{pattern}"' for pattern in self.regular_expressions)});
        
        // Signal ready and wait for start
        BufferedWriter readyWriter = new BufferedWriter(new FileWriter("{self.ready_pipe}"));
        readyWriter.write("ready\\n");
        readyWriter.flush();
        readyWriter.close();
        
        BufferedReader startReader = new BufferedReader(new FileReader("{self.start_pipe}"));
        startReader.readLine();  // Wait for start signal
        startReader.close();
        
        // Perform regex matching
        for (int i = 0; i < patterns.size(); i++) {{
            String pattern = patterns.get(i);
            System.out.println("Pattern " + i + ": " + pattern);
            Pattern compiledPattern = Pattern.compile(pattern);
            Matcher matcher = compiledPattern.matcher(corpus);
            while (matcher.find()) {{
                System.out.println("Match: " + matcher.group());
            }}
            System.out.println();
        }}
        
        // Signal completion
        BufferedWriter doneWriter = new BufferedWriter(new FileWriter("{self.done_pipe}"));
        doneWriter.write("done\\n");
        doneWriter.flush();
        doneWriter.close();
    }}

    private static String readFile(String filepath) {{
        StringBuilder content = new StringBuilder();
        try (BufferedReader reader = new BufferedReader(new FileReader(filepath))) {{
            String line;
            while ((line = reader.readLine()) != null) {{
                content.append(line).append("\\n");
            }}
        }} catch (IOException e) {{
            e.printStackTrace();
        }}
        return content.toString();
    }}
}}"""
        
        with open(f"{self.directory_to_store_engines}/RegexMatcher.java", "w") as f:
            f.write(java_code)
    
    def _create_javascript_engine(self):
        """
        Create the javascript engine, it will use the javascript RegExp object.
        The engine will be stored as a javascript file.
        """
        js_code = f"""
const fs = require('fs');

// Load corpus first
const corpus = fs.readFileSync('{self.filepath_to_corpus}', 'utf8');
const patterns = [{", ".join(f'"{pattern}"' for pattern in self.regular_expressions)}];

// Signal ready and wait for start
fs.writeFileSync('{self.ready_pipe}', 'ready\\n');
fs.readFileSync('{self.start_pipe}'); // Wait for start signal

// Perform regex matching
patterns.forEach((pattern, i) => {{
    console.log(`Pattern ${{i}}: ${{pattern}}`);
    const regex = new RegExp(pattern, 'g');
    let match;
    while ((match = regex.exec(corpus)) !== null) {{
        console.log(`Match: ${{match[0]}}`);
    }}
    console.log();
}});

// Signal completion
fs.writeFileSync('{self.done_pipe}', 'done\\n');
"""
        
        with open(f"{self.directory_to_store_engines}/regex_matcher.js", "w") as f:
            f.write(js_code)

    def _create_boost_engine(self):
        """
        Create the boost engine, it will use the Boost.Regex package.
        The engine will be stored as a c++ file.
        """
        cpp_code = f"""
#include <boost/regex.hpp>
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>

std::string read_file(const std::string& filepath) {{
    std::ifstream file(filepath);
    std::stringstream buffer;
    buffer << file.rdbuf();
    return buffer.str();
}}

int main() {{
    // Load corpus first
    std::string corpus = read_file("{self.filepath_to_corpus}");
    std::vector<std::string> patterns = {{{", ".join(f'"{pattern}"' for pattern in self.regular_expressions)}}};
    
    // Signal ready and wait for start
    {{
        std::ofstream ready_file("{self.ready_pipe}");
        ready_file << "ready\\n";
    }}
    {{
        std::ifstream start_file("{self.start_pipe}");
        std::string _;
        std::getline(start_file, _);  // Wait for start signal
    }}
    
    // Perform regex matching
    for (size_t i = 0; i < patterns.size(); ++i) {{
        std::cout << "Pattern " << i << ": " << patterns[i] << std::endl;
        boost::regex pattern(patterns[i]);
        boost::sregex_iterator it(corpus.begin(), corpus.end(), pattern);
        boost::sregex_iterator end;
        while(it != end) {{
            std::cout << "Match: " << it->str() << std::endl;
            ++it;
        }}
        std::cout << std::endl;
    }}
    
    // Signal completion
    {{
        std::ofstream done_file("{self.done_pipe}");
        done_file << "done\\n";
    }}
    
    return 0;
}}"""
        
        with open(f"{self.directory_to_store_engines}/regex_matcher.cpp", "w") as f:
            f.write(cpp_code)
    
    def destroy_engines(self):
        """
        Destroy all the engines that were created by deleting the files in the
        'self.directory_to_store_engines' directory.
        """
        if os.path.exists(self.directory_to_store_engines):
            shutil.rmtree(self.directory_to_store_engines)

if __name__ == "__main__":
    factory = RegexEngineFactory(regular_expressions=["hello", "Pikles"], directory_to_store_engines="regex_engines", filepath_to_corpus="data/corpus.txt")
    # factory.create_engines()
    # input("Press Enter to destroy the engines...")
    factory.destroy_engines()

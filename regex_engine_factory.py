import os
import shutil

class RegexEngineFactory:
    def __init__(self, regular_expressions: list[str], directory_to_store_engines: str = 'regex_engines', filepath_to_corpus: str = 'data/test_corpus.txt'):
        self.regular_expressions = regular_expressions
        self.directory_to_store_engines = directory_to_store_engines
        self.filepath_to_corpus = filepath_to_corpus

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
        self._create_dotnet_engine()
    
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
        List<String> patterns = Arrays.asList({", ".join(f'"{pattern.replace("\\", "\\\\")}"' for pattern in self.regular_expressions)});
        
        // Signal ready
        System.out.println("ready");
        
        // Wait for start signal
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        reader.readLine();  // Wait for any input
        
        // Perform regex matching
        for (int i = 0; i < patterns.size(); i++) {{
            String pattern = patterns.get(i);
            Pattern compiledPattern = Pattern.compile(pattern);
            Matcher matcher = compiledPattern.matcher(corpus);
            int count = 0;
            while (matcher.find()) {{
                count++;
            }}
            System.out.println("Pattern " + i + ": " + pattern + " - Matches: " + count);
        }}
        
        // Signal completion
        System.out.println("done");
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
const patterns = [{", ".join(f'"{pattern.replace("\\", "\\\\")}"' for pattern in self.regular_expressions)}];

// Signal ready
console.log('ready');

// Wait for start signal
process.stdin.resume();
process.stdin.once('data', () => {{
    // Perform regex matching
    patterns.forEach((pattern, i) => {{
        const regex = new RegExp(pattern, 'g');
        const matches = corpus.match(regex) || [];
        console.log(`Pattern ${{i}}: ${{pattern}} - Matches: ${{matches.length}}`);
    }});

    // Signal completion
    console.log('done');
    process.exit(0);
}});
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
    std::vector<std::string> patterns = {{{", ".join(f'"{pattern.replace("\\", "\\\\")}"' for pattern in self.regular_expressions)}}};
    
    // Signal ready
    std::cout << "ready" << std::endl;
    
    // Wait for start signal
    std::string _;
    std::getline(std::cin, _);
    
    // Perform regex matching
    for (size_t i = 0; i < patterns.size(); ++i) {{
        boost::regex pattern(patterns[i]);
        boost::sregex_iterator it(corpus.begin(), corpus.end(), pattern);
        boost::sregex_iterator end;
        int count = 0;
        while(it != end) {{
            count++;
            ++it;
        }}
        std::cout << "Pattern " << i << ": " << patterns[i] << " - Matches: " << count << std::endl;
    }}
    
    // Signal completion
    std::cout << "done" << std::endl;
    
    return 0;
}}"""
        
        with open(f"{self.directory_to_store_engines}/regex_matcher.cpp", "w") as f:
            f.write(cpp_code)
    
    def _create_dotnet_engine(self):
        """
        Create the .NET engine as a C# console application, which uses
        System.Text.RegularExpressions.Regex to find matches.
        """
        cs_code = f"""
using System;
using System.IO;
using System.Text.RegularExpressions;

public class RegexMatcher
{{
    public static void Main(string[] args)
    {{
        // Load corpus first
        string corpus = File.ReadAllText("{self.filepath_to_corpus}");
        string[] patterns = new string[] {{ {", ".join(f'"{pattern.replace("\\", "\\\\")}"' for pattern in self.regular_expressions)} }};

        // Signal ready
        Console.WriteLine("ready");

        // Wait for start signal
        Console.ReadLine();

        // Perform regex matching
        for (int i = 0; i < patterns.Length; i++)
        {{
            string pattern = patterns[i];
            var matches = Regex.Matches(corpus, pattern);
            Console.WriteLine("Pattern " + i + ": " + pattern + " - Matches: " + matches.Count);
        }}

        // Signal completion
        Console.WriteLine("done");
    }}
}}
"""
        with open(f"{self.directory_to_store_engines}/RegexMatcher.cs", "w") as f:
            f.write(cs_code)
    
    def destroy_engines(self):
        """
        Destroy all the engines that were created by deleting the files in the
        'self.directory_to_store_engines' directory.
        """
        if os.path.exists(self.directory_to_store_engines):
            shutil.rmtree(self.directory_to_store_engines)

if __name__ == "__main__":
    factory = RegexEngineFactory(regular_expressions=["hello", "Pikles"], directory_to_store_engines="regex_engines", filepath_to_corpus="data/test_corpus.txt")
    factory.create_engines()
    # input("Press Enter to destroy the engines...")
    # factory.destroy_engines()

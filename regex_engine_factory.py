import os
import shutil

class RegexEngineFactory:
    def __init__(self, matches_to_evaluate: list[str], directory_to_store_engines: str = 'regex_engines', filepath_to_corpus: str = 'data/corpus.txt'):
        self.matches_to_evaluate = matches_to_evaluate
        self.directory_to_store_engines = directory_to_store_engines
        self.filepath_to_corpus = filepath_to_corpus

    def create_engines(self):
        """
        Create all the engines that will be used to evaluate the matches,
        the engines will be stored as files in the 'self.directory_to_store_engines' directory.
        The different engines will run the 'matches_to_evaluate' list of matches against the 
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
        """
        Create the java engine, it will use the java.util.regex package.
        The engine will be stored as a java file.
        """
        java_code = f"""
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.regex.Pattern;
import java.util.regex.Matcher;

public class RegexMatcher {{
    public static void main(String[] args) {{
        String corpus = readFile("{self.filepath_to_corpus}");
        
        {self._generate_java_matches()}
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

    def _generate_java_matches(self):
        java_matches = []
        for i, pattern in enumerate(self.matches_to_evaluate):
            java_matches.append(f"""
        Pattern pattern{i} = Pattern.compile("{pattern}");
        Matcher matcher{i} = pattern{i}.matcher(corpus);
        while (matcher{i}.find()) {{
            System.out.println("Match {i}: " + matcher{i}.group());
        }}""")
        return "\n".join(java_matches)
    
    def _create_javascript_engine(self):
        """
        Create the javascript engine, it will use the javascript RegExp object.
        The engine will be stored as a javascript file.
        """
        js_code = f"""
const fs = require('fs');

const corpus = fs.readFileSync('{self.filepath_to_corpus}', 'utf8');

{self._generate_js_matches()}
"""
        
        with open(f"{self.directory_to_store_engines}/regex_matcher.js", "w") as f:
            f.write(js_code)

    def _generate_js_matches(self):
        js_matches = []
        for i, pattern in enumerate(self.matches_to_evaluate):
            js_matches.append(f"""
const regex{i} = new RegExp('{pattern}', 'g');
let match{i};
while ((match{i} = regex{i}.exec(corpus)) !== null) {{
    console.log(`Match {i}: ${{match{i}[0]}}`);
}}""")
        return "\n".join(js_matches)
    
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

std::string read_file(const std::string& filepath) {{
    std::ifstream file(filepath);
    std::stringstream buffer;
    buffer << file.rdbuf();
    return buffer.str();
}}

int main() {{
    std::string corpus = read_file("{self.filepath_to_corpus}");
    
    {self._generate_cpp_matches()}
    
    return 0;
}}"""
        
        with open(f"{self.directory_to_store_engines}/regex_matcher.cpp", "w") as f:
            f.write(cpp_code)

    def _generate_cpp_matches(self):
        cpp_matches = []
        for i, pattern in enumerate(self.matches_to_evaluate):
            cpp_matches.append(f"""
    boost::regex pattern{i}("{pattern}");
    boost::sregex_iterator it{i}(corpus.begin(), corpus.end(), pattern{i});
    boost::sregex_iterator end;
    while(it{i} != end) {{
        std::cout << "Match {i}: " << it{i}->str() << std::endl;
        ++it{i};
    }}""")
        return "\n".join(cpp_matches)
    
    def destroy_engines(self):
        """
        Destroy all the engines that were created by deleting the files in the
        'self.directory_to_store_engines' directory.
        """
        if os.path.exists(self.directory_to_store_engines):
            shutil.rmtree(self.directory_to_store_engines)

if __name__ == "__main__":
    factory = RegexEngineFactory(matches_to_evaluate=["hello", "Pikles"], directory_to_store_engines="regex_engines", filepath_to_corpus="data/corpus.txt")
    factory.create_engines()


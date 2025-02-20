
#include <boost/regex.hpp>
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>

std::string read_file(const std::string& filepath) {
    std::ifstream file(filepath);
    std::stringstream buffer;
    buffer << file.rdbuf();
    return buffer.str();
}

int main() {
    // Load corpus first
    std::string corpus = read_file("data/test_corpus.txt");
    std::vector<std::string> patterns = {"hello", "Pikles"};
    
    // Signal ready and wait for start
    {
        std::ofstream ready_file("regex_engines/ready_pipe");
        ready_file << "ready\n";
    }
    {
        std::ifstream start_file("regex_engines/start_pipe");
        std::string _;
        std::getline(start_file, _);  // Wait for start signal
    }
    
    // Perform regex matching
    for (size_t i = 0; i < patterns.size(); ++i) {
        std::cout << "Pattern " << i << ": " << patterns[i] << std::endl;
        boost::regex pattern(patterns[i]);
        boost::sregex_iterator it(corpus.begin(), corpus.end(), pattern);
        boost::sregex_iterator end;
        while(it != end) {
            std::cout << "Match: " << it->str() << std::endl;
            ++it;
        }
        std::cout << std::endl;
    }
    
    // Signal completion
    {
        std::ofstream done_file("regex_engines/done_pipe");
        done_file << "done\n";
    }
    
    return 0;
}
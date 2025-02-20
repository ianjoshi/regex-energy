
#include <boost/regex.hpp>
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>

std::string read_file(const std::string& filepath) {
    std::ifstream file(filepath);
    std::stringstream buffer;
    buffer << file.rdbuf();
    return buffer.str();
}

int main() {
    std::string corpus = read_file("data/corpus.txt");
    
    
    boost::regex pattern0("hello");
    boost::sregex_iterator it0(corpus.begin(), corpus.end(), pattern0);
    boost::sregex_iterator end;
    while(it0 != end) {
        std::cout << "Match 0: " << it0->str() << std::endl;
        ++it0;
    }

    boost::regex pattern1("Pikles");
    boost::sregex_iterator it1(corpus.begin(), corpus.end(), pattern1);
    boost::sregex_iterator end;
    while(it1 != end) {
        std::cout << "Match 1: " << it1->str() << std::endl;
        ++it1;
    }
    
    return 0;
}
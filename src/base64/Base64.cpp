#include <iostream>
#include <string>
#include <sstream>
#include <map>

using namespace std;
class Base64 {
public:
    string encode(string data);
    string decode(string data);
private:
    string base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
};

string Base64::encode(string data) {
    std::stringstream binary_str;
    std::stringstream encoded_data;
    for (const auto& s : data) {
        // binary <<
    }

    // pad binary data
    while (binary_str.str().length() % 6 != 0) {
        binary_str << '0';
    }

    // encode byte
    for (int i = 0; i < binary_str.str().length(); i += 6) {
        string chunk = binary_str.str().substr(i, 6);
        int decimal_val = std::stoi(chunk);
        encoded_data << base64_chars.at(decimal_val);
    }

    // add padding '=' if needed
    int padding = (4 - encoded_data.str().length() % 4) % 4;
    for (int i = 0; i < padding; i++) {
        encoded_data << '=';
    }

    return encoded_data.str();
}

// ------------------------------------------------

class ArgParser {
public:
    ArgParser(int argc, char* args[]);
    void add(char* arg_name, bool get_value);
    bool has_arg(char* arg_name);
private:
    char** m_args;
    map<string, string> arg_map;
};

ArgParser::ArgParser(int argc, char* args[]) {
    this->m_args = args;
}

void ArgParser::add(char* arg_name, bool get_value) {
    arg_map[string(arg_name)] = string("");
}

// ------------------------------------------------

int main(int argc, char* args[]) {
    ArgParser aparser(argc, args);
    aparser.add("-e", false);
    aparser.add("-d", false);
    if (aparser.has_arg("-e")) {
        // encode
    }
    else if (aparser.has_arg("-d")) {
        // decode
    }
}

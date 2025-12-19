#include "cashflow_calculator.h"
#include <iostream>
#include <fstream>
#include <sstream>

InstrumentType parse_type(const std::string& type) {
    if (type == "bond") return InstrumentType::BOND;
    if (type == "deposit") return InstrumentType::DEPOSIT;
    return InstrumentType::LOAN;
}

PaymentFrequency parse_freq(const std::string& freq) {
    if (freq == "quarterly") return PaymentFrequency::QUARTERLY;
    return PaymentFrequency::MONTHLY;
}

CustomerSegment parse_seg(const std::string& seg) {
    if (seg == "corporate") return CustomerSegment::CORPORATE;
    return CustomerSegment::RETAIL;
}

int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cerr << "Usage: " << argv[0] << " <input_csv> <output_csv>\n";
        return 1;
    }

    std::string input_file = argv[1];
    std::string output_file = argv[2];

    std::vector<Instrument> instruments;
    std::ifstream in(input_file);
    if (!in.is_open()) {
        std::cerr << "Failed to open input file.\n";
        return 1;
    }

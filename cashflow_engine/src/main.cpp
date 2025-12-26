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

    std::string line;
    std::getline(in, line); // header loop
    while (std::getline(in, line)) {
        if (line.empty()) continue;
        std::stringstream ss(line);
        std::string id, type, notional, rate, start, maturity, freq, seg;
        
        std::getline(ss, id, ',');
        std::getline(ss, type, ',');
        std::getline(ss, notional, ',');
        std::getline(ss, rate, ',');
        std::getline(ss, start, ',');
        std::getline(ss, maturity, ',');
        std::getline(ss, freq, ',');
        std::getline(ss, seg, ',');

        instruments.push_back({
            id, parse_type(type), std::stod(notional), std::stod(rate),
            start, maturity, parse_freq(freq), parse_seg(seg)
        });
    }
    
    std::cout << "Engine processing " << instruments.size() << " instruments...\n";
    auto flows = CashflowCalculator::calculate_all(instruments);
    std::cout << "Generated " << flows.size() << " cashflows.\n";

    std::ofstream out(output_file);
    out << "instrument_id,date,principal_amount,interest_amount,total_amount\n";
    for (const auto& f : flows) {
        out << f.instrument_id << "," << f.date << "," << f.principal_amount 
            << "," << f.interest_amount << "," << f.total_amount << "\n";
    }

    return 0;
}

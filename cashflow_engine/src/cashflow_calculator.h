#pragma once

#include "instrument.h"
#include <vector>
#include <string>

struct Cashflow {
    std::string instrument_id;
    std::string date;
    double principal_amount;
    double interest_amount;
    double total_amount;
};

class CashflowCalculator {
public:
    static std::vector<Cashflow> calculate_loan_cashflows(const Instrument& inst);
    static std::vector<Cashflow> calculate_bond_cashflows(const Instrument& inst);
    static std::vector<Cashflow> calculate_deposit_cashflows(const Instrument& inst);
    
    static std::vector<Cashflow> calculate_all(const std::vector<Instrument>& instruments);
};

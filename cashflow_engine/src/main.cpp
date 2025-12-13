#include "cashflow_calculator.h"
#include <iostream>
#include <fstream>
#include <sstream>

InstrumentType parse_type(const std::string& type) {
    if (type == "bond") return InstrumentType::BOND;

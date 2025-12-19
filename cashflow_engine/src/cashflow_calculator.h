#pragma once

#include "instrument.h"
#include <vector>
#include <string>

struct Cashflow {
    std::string instrument_id;
    std::string date;
    double principal_amount;
    double interest_amount;

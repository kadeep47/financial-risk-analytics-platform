#pragma once

#include <string>

enum class InstrumentType {
    LOAN,
    BOND,
    DEPOSIT
};

enum class PaymentFrequency {
    MONTHLY,
    QUARTERLY
};

enum class CustomerSegment {
    RETAIL,
    CORPORATE
};

struct Instrument {
    std::string instrument_id;
    InstrumentType instrument_type;
    double notional;
    double interest_rate;
    std::string start_date;
    std::string maturity_date;
    PaymentFrequency payment_frequency;
    CustomerSegment customer_segment;
};

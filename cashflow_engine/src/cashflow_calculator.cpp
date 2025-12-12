#include "cashflow_calculator.h"
#include <cmath>
#include <thread>
#include <future>
#include <iostream>
#include <algorithm>

// Very simplified date math for MVP: assuming 30 days every month, or simplified periodic addition.
// In a real system we'd use <chrono> with Howard Hinnant's date library.

std::vector<Cashflow> CashflowCalculator::calculate_loan_cashflows(const Instrument& inst) {
    std::vector<Cashflow> flows;

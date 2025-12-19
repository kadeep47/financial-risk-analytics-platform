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
    
    // Simplification: assume 1 year tenure and monthly payments for demonstration
    // if exact maturity date diff is needed, it would be calculated.
    // Let's use standard EMI formula: E = P * r * (1+r)^n / ((1+r)^n - 1)
    
    int periods_per_year = (inst.payment_frequency == PaymentFrequency::MONTHLY) ? 12 : 4;
    double r = inst.interest_rate / periods_per_year;
    // Approximating tenure to 5 years (60 months) if not provided strictly by date diff in MVP
    int n = 5 * periods_per_year; 
    
    double emi = inst.notional * r * std::pow(1+r, n) / (std::pow(1+r, n) - 1);
    
    double remaining_principal = inst.notional;
    for(int i = 1; i <= n; ++i) {
        double interest = remaining_principal * r;
        double principal = emi - interest;
        
        // Final period adjustment
        if (i == n) {
            principal = remaining_principal;
            emi = principal + interest;
        }
        
        remaining_principal -= principal;
        
        flows.push_back({
            inst.instrument_id,
            "period_" + std::to_string(i), // simplifying dates for MVP
            principal,
            interest,
            emi
        });
    }
    
    return flows;
}

std::vector<Cashflow> CashflowCalculator::calculate_bond_cashflows(const Instrument& inst) {
    std::vector<Cashflow> flows;
    int periods_per_year = (inst.payment_frequency == PaymentFrequency::MONTHLY) ? 12 : 4;
    double current_coupon = inst.notional * (inst.interest_rate / periods_per_year);
    int n = 5 * periods_per_year; // Approx 5 yrs
    
    for(int i = 1; i <= n; ++i) {
        double principal = (i == n) ? inst.notional : 0.0;
        flows.push_back({
            inst.instrument_id,
            "period_" + std::to_string(i),
            principal,
            current_coupon,
            principal + current_coupon

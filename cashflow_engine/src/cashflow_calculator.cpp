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
        });
    }
    
    return flows;
}

std::vector<Cashflow> CashflowCalculator::calculate_deposit_cashflows(const Instrument& inst) {
    std::vector<Cashflow> flows;
    // Simple maturity deposit
    int periods_per_year = (inst.payment_frequency == PaymentFrequency::MONTHLY) ? 12 : 4;
    int n = 1 * periods_per_year; // Approx 1 yr
    
    double interest = inst.notional * inst.interest_rate; // simple interest
    flows.push_back({
        inst.instrument_id,
        "period_" + std::to_string(n),
        inst.notional,
        interest,
        inst.notional + interest
    });
    
    return flows;
}

std::vector<Cashflow> CashflowCalculator::calculate_all(const std::vector<Instrument>& instruments) {
    std::vector<Cashflow> all_flows;
    
    // Very basic multithreading
    const size_t num_threads = std::thread::hardware_concurrency();
    std::vector<std::future<std::vector<Cashflow>>> futures;
    
    auto process_batch = [](std::vector<Instrument> batch) {
        std::vector<Cashflow> local_flows;
        for (const auto& inst : batch) {
            std::vector<Cashflow> flows;
            if (inst.instrument_type == InstrumentType::LOAN) {
                flows = calculate_loan_cashflows(inst);
            } else if (inst.instrument_type == InstrumentType::BOND) {
                flows = calculate_bond_cashflows(inst);
            } else {
                flows = calculate_deposit_cashflows(inst);
            }
            local_flows.insert(local_flows.end(), flows.begin(), flows.end());
        }
        return local_flows;
    };

    size_t batch_size = instruments.size() / num_threads;
    if (batch_size == 0) batch_size = instruments.size();

    for (size_t i = 0; i < instruments.size(); i += batch_size) {
        auto end = std::min(i + batch_size, instruments.size());
        std::vector<Instrument> batch(instruments.begin() + i, instruments.begin() + end);
        futures.push_back(std::async(std::launch::async, process_batch, batch));
    }

    for (auto& f : futures) {
        auto res = f.get();
        all_flows.insert(all_flows.end(), res.begin(), res.end());
    }

    return all_flows;
}

"""
FinSakhi - Financial Calculation Engine
Subject Mapping: Python Programming & Procedural Logic (Functions, Conditionals, Error Handling)

Implements formulas and validation rules for:
1. Business Finance Calculator (Profit, Margin %, Savings %)
2. Loan Assessment Guidance (Debt-to-Income ratio, educational estimate)
3. Monthly Budget Breakdown
"""

def calculate_business_finance(monthly_income, monthly_expenses, monthly_savings=0.0):
    """
    Computes business profitability and savings metrics.
    Prevents division by zero and validates numeric types.
    
    Formulas:
    - Profit = Income - Expenses
    - Remaining Amount = Income - Expenses - Savings
    - Profit Margin (%) = (Profit / Income) * 100  [if Income > 0]
    - Savings Rate (%) = (Savings / Income) * 100   [if Income > 0]
    """
    try:
        income = float(monthly_income)
        expenses = float(monthly_expenses)
        savings = float(monthly_savings)
    except (ValueError, TypeError):
        return {
            'success': False,
            'error': 'Please enter valid numerical amounts for income, expenses, and savings.'
        }

    if income < 0 or expenses < 0 or savings < 0:
        return {
            'success': False,
            'error': 'Amounts cannot be negative numbers.'
        }

    # Core Calculations
    profit = income - expenses
    remaining_after_savings = profit - savings
    
    # Division by Zero Safe Computation
    if income > 0:
        profit_percentage = round((profit / income) * 100, 2)
        savings_percentage = round((savings / income) * 100, 2)
    else:
        profit_percentage = 0.0
        savings_percentage = 0.0

    # Business Health Classification
    if profit > 0 and profit_percentage >= 20.0:
        health_status = 'Healthy & Sustainable'
        health_color = 'success'
        health_message = 'Your enterprise generates a sound surplus. Continue building an emergency buffer.'
    elif profit > 0:
        health_status = 'Moderate Margin'
        health_color = 'warning'
        health_message = 'Your business is profitable, but keep a close eye on reducing raw material and overhead costs.'
    elif profit == 0:
        health_status = 'Break-even'
        health_color = 'warning'
        health_message = 'Revenue exactly covers expenses. You need higher sales volume or lower costs to earn a living wage.'
    else:
        health_status = 'Operating at a Loss'
        health_color = 'danger'
        health_message = 'Monthly expenses exceed total sales. Urgent cost cutting or price adjustments are recommended.'

    return {
        'success': True,
        'income': round(income, 2),
        'expenses': round(expenses, 2),
        'savings': round(savings, 2),
        'profit': round(profit, 2),
        'remaining_after_savings': round(remaining_after_savings, 2),
        'profit_percentage': profit_percentage,
        'savings_percentage': savings_percentage,
        'health_status': health_status,
        'health_color': health_color,
        'health_message': health_message
    }


def analyze_loan_guidance(annual_income, business_age_years, existing_loan_amount, required_loan_amount):
    """
    Analyzes user inputs to provide educational loan guidance and possible loan categories.
    Note: Explicitly framed as educational assessment, NOT credit guarantee.
    
    Key Metrics:
    - Debt-to-Income (DTI) estimate
    - Loan-to-Annual-Income ratio
    - Eligibility tier recommendations
    """
    try:
        income = float(annual_income)
        years = float(business_age_years)
        existing_loan = float(existing_loan_amount)
        req_loan = float(required_loan_amount)
    except (ValueError, TypeError):
        return {
            'success': False,
            'error': 'Please provide valid positive numbers for all loan assessment fields.'
        }

    if income <= 0 or years < 0 or existing_loan < 0 or req_loan <= 0:
        return {
            'success': False,
            'error': 'Annual income and required loan must be greater than zero. Business age and existing loans cannot be negative.'
        }

    monthly_income = income / 12.0
    # Rule of thumb: Estimated existing monthly debt service ~ 3% of existing loan
    estimated_existing_emi = existing_loan * 0.03
    dti_percentage = round((estimated_existing_emi / monthly_income) * 100, 2) if monthly_income > 0 else 100.0

    # Loan ratio
    loan_to_income_ratio = round(req_loan / income, 2)

    # Educational categories determination
    categories = []
    if req_loan <= 50000:
        categories.append({
            'name': 'Micro Working Capital (PMMY Shishu / PM SVANidhi)',
            'range': 'Up to ₹50,000',
            'features': 'Collateral-free, fast processing, minimal documentation suitable for small village shops and vendors.'
        })
    elif req_loan <= 500000:
        categories.append({
            'name': 'Small Enterprise Term Loan (PMMY Kishor)',
            'range': '₹50,000 to ₹5,00,000',
            'features': 'Designed for purchasing shop equipment, milk chillers, sewing machinery, or commercial stock.'
        })
    else:
        categories.append({
            'name': 'Commercial Expansion / PMEGP / Stand-Up India',
            'range': 'Above ₹5,00,000',
            'features': 'Requires a detailed Project Report, quotation from suppliers, Udyam registration, and bank viability appraisal.'
        })

    # Educational Readiness Level
    if dti_percentage < 35.0 and years >= 1.0 and loan_to_income_ratio <= 3.0:
        readiness = 'Strong Educational Profile'
        readiness_badge = 'success'
        readiness_advice = 'Your business demonstrates healthy borrowing capacity. Banks look favorably on low existing debt and active operational history.'
    elif dti_percentage < 50.0 and loan_to_income_ratio <= 5.0:
        readiness = 'Moderate Educational Profile'
        readiness_badge = 'warning'
        readiness_advice = 'You may qualify for micro-loans (such as MUDRA Shishu). Keep bank statements updated and consider starting with smaller credit lines.'
    else:
        readiness = 'Caution - High Debt Ratio'
        readiness_badge = 'danger'
        readiness_advice = 'Your existing obligations or required loan amount is high relative to current annual turnover. Focus on debt reduction before taking new liabilities.'

    return {
        'success': True,
        'annual_income': round(income, 2),
        'monthly_income': round(monthly_income, 2),
        'business_age_years': years,
        'existing_loan': round(existing_loan, 2),
        'required_loan': round(req_loan, 2),
        'dti_percentage': min(dti_percentage, 100.0),
        'loan_to_income_ratio': loan_to_income_ratio,
        'readiness': readiness,
        'readiness_badge': readiness_badge,
        'readiness_advice': readiness_advice,
        'categories': categories,
        'required_documents': [
            'Aadhaar Card and PAN Card (Identity and Address Proof)',
            'Last 6-12 months Bank Account Statement',
            'Udyam Registration Certificate (Free MSME registration)',
            'Proof of Business Location (Electricity bill or Gram Panchayat NOC)',
            'Vendor Quotations for machinery or raw materials to be bought'
        ]
    }


def calculate_monthly_budget(monthly_income, expenses_dict, target_savings=0.0):
    """
    Computes categorized monthly budget breakdown.
    expenses_dict contains keys like:
    - raw_materials, rent, utilities, transport, household, misc
    """
    try:
        income = float(monthly_income)
        target_savings = float(target_savings)
        clean_expenses = {k: float(v) for k, v in expenses_dict.items() if float(v) >= 0}
    except (ValueError, TypeError):
        return {
            'success': False,
            'error': 'All budget inputs must be valid positive numbers.'
        }

    total_expenses = sum(clean_expenses.values())
    net_balance = income - total_expenses
    balance_after_savings = net_balance - target_savings

    percentages = {}
    if income > 0:
        for k, v in clean_expenses.items():
            percentages[k] = round((v / income) * 100, 1)
        savings_ratio = round((target_savings / income) * 100, 1)
    else:
        savings_ratio = 0.0

    return {
        'success': True,
        'income': round(income, 2),
        'expenses_breakdown': clean_expenses,
        'percentages': percentages,
        'total_expenses': round(total_expenses, 2),
        'target_savings': round(target_savings, 2),
        'savings_ratio': savings_ratio,
        'net_balance': round(net_balance, 2),
        'balance_after_savings': round(balance_after_savings, 2)
    }

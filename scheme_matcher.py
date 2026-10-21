"""
FinSakhi - Government Scheme Finder & Matching Logic
Subject Mapping: Python Data Structures, Searching & Conditional Branching (Sem 1-3)

Evaluates user business profile against stored MySQL scheme records using 
transparent, deterministic if-else rules and relational SQL filters.
"""

from db import query_db

def find_matching_schemes(business_type, state, annual_income, required_loan_amount, lang='en'):
    """
    Retrieves candidate schemes from the database and evaluates them against 
    deterministic eligibility rules:
    
    1. Business Type Match: Scheme accepts 'All' OR user's selected business type.
    2. State Applicability: Scheme applies to 'All India' OR matches user's state.
    3. Income Ceiling: User's income is <= max_annual_income (or ceiling is 0.0, i.e., no limit).
    4. Loan Range: Required loan is within [min_loan_amount, max_loan_amount].
    """
    try:
        income = float(annual_income)
        loan_amt = float(required_loan_amount)
    except (ValueError, TypeError):
        return {
            'success': False,
            'error': 'Please provide valid numeric values for income and required loan amount.',
            'matched_schemes': [],
            'count': 0
        }

    # Fetch all active schemes from database
    schemes = query_db("SELECT * FROM schemes ORDER BY id ASC")
    if not schemes:
        return {
            'success': True,
            'matched_schemes': [],
            'count': 0,
            'message': 'No schemes are currently registered in the database.'
        }

    matched_schemes = []
    
    for s in schemes:
        # Condition 1: State Match
        scheme_state = s.get('state_applicability', 'All India').strip()
        state_match = (
            scheme_state.lower() == 'all india' or 
            state.lower() in scheme_state.lower() or 
            state.lower() == 'all'
        )

        # Condition 2: Business Type Match
        # eligible_business_types in DB is a comma-separated string like "Dairy,Kirana,Handicraft"
        # Form business_type is like "Agriculture & Dairy" or "Small Grocery / Kirana"
        # We check both directions: if any DB keyword appears in user's selection, or vice versa
        eligible_types = [t.strip().lower() for t in s.get('eligible_business_types', 'All').split(',')]
        user_btype = business_type.lower().strip()
        business_match = (
            'all' in eligible_types or
            'all rural business' in eligible_types or
            user_btype in eligible_types or
            any(t in user_btype for t in eligible_types) or
            any(user_btype in t for t in eligible_types)
        )

        # Condition 3: Income Ceiling Match
        max_income = float(s.get('max_annual_income', 0.0))
        income_match = (max_income == 0.0) or (income <= max_income)

        # Condition 4: Loan Amount Match
        min_loan = float(s.get('min_loan_amount', 0.0))
        max_loan = float(s.get('max_loan_amount', 10000000.0))
        loan_match = (loan_amt <= max_loan) and (loan_amt >= (min_loan * 0.5)) # Allow reasonable leeway

        # Evaluate Composite Condition
        if state_match and business_match and income_match and loan_match:
            # Select appropriate multilingual description
            desc_key = f"description_{lang}"
            description = s.get(desc_key) or s.get('description_en') or ''
            
            scheme_item = {
                'id': s.get('id'),
                'scheme_name': s.get('scheme_name'),
                'scheme_code': s.get('scheme_code'),
                'category': s.get('category'),
                'description': description,
                'state_applicability': s.get('state_applicability'),
                'max_loan_amount': float(s.get('max_loan_amount', 0)),
                'min_loan_amount': float(s.get('min_loan_amount', 0)),
                'max_annual_income': float(s.get('max_annual_income', 0)),
                'subsidy_percentage': float(s.get('subsidy_percentage', 0)),
                'required_documents': s.get('required_documents', ''),
                'how_to_apply': s.get('how_to_apply', ''),
                'official_portal': s.get('official_portal', '')
            }
            matched_schemes.append(scheme_item)

    # Sort matched schemes: prioritizing schemes with subsidy percentage (descending)
    matched_schemes.sort(key=lambda x: x['subsidy_percentage'], reverse=True)

    return {
        'success': True,
        'matched_schemes': matched_schemes,
        'count': len(matched_schemes),
        'searched_criteria': {
            'business_type': business_type,
            'state': state,
            'annual_income': income,
            'required_loan_amount': loan_amt
        }
    }

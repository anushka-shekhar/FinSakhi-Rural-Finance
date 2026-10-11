"""
FinSakhi - Comprehensive Automated Test Suite
Subject Mapping: Software Testing, Quality Assurance, and System Validation
Tests all modules: Auth, Schemes, Calculations, Language, Feedback, and Admin CRUD.
"""

import unittest
from werkzeug.security import check_password_hash
from app import app
from db import query_db, execute_db
from finance_calc import calculate_business_finance, analyze_loan_guidance, calculate_monthly_budget
from scheme_matcher import find_matching_schemes

class FinSakhiSystemTestCase(unittest.TestCase):

    def setUp(self):
        """Set up test client with testing mode enabled."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()

    # -------------------------------------------------------------
    # 1. DATABASE CONNECTIVITY & INTEGRITY
    # -------------------------------------------------------------
    def test_01_database_tables_exist(self):
        """Verify that all core relational tables exist and are populated."""
        users = query_db("SELECT COUNT(*) as count FROM users", one=True)
        schemes = query_db("SELECT COUNT(*) as count FROM schemes", one=True)
        awareness = query_db("SELECT COUNT(*) as count FROM financial_content", one=True)
        admins = query_db("SELECT COUNT(*) as count FROM admin_users", one=True)

        self.assertIsNotNone(users)
        self.assertIsNotNone(schemes)
        self.assertIsNotNone(awareness)
        self.assertIsNotNone(admins)
        self.assertGreaterEqual(schemes['count'], 5, "Database must have at least 5 default schemes")
        self.assertGreaterEqual(awareness['count'], 6, "Database must have 6 financial awareness topics")

    # -------------------------------------------------------------
    # 2. USER REGISTRATION & PASSWORD HASHING
    # -------------------------------------------------------------
    def test_02_registration_and_hashing(self):
        """Verify user registration, input validation, and password hashing security."""
        # Clean up test user if previously exists
        execute_db("DELETE FROM users WHERE mobile_number = %s", ('9999988888',))

        # Test valid registration
        res = self.client.post('/register', data={
            'full_name': 'Test Entrepreneur Ramesh',
            'mobile_number': '9999988888',
            'password': 'secretpassword123',
            'village': 'Shirur, Maharashtra',
            'business_type': 'Agriculture & Dairy'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)

        # Verify in database that password is NOT plaintext
        db_user = query_db("SELECT * FROM users WHERE mobile_number = %s", ('9999988888',), one=True)
        self.assertIsNotNone(db_user)
        self.assertNotEqual(db_user['password_hash'], 'secretpassword123')
        self.assertTrue(check_password_hash(db_user['password_hash'], 'secretpassword123'))

        # Test invalid mobile number validation (must fail)
        invalid_res = self.client.post('/register', data={
            'full_name': 'Bad Mobile User',
            'mobile_number': '12345', # Less than 10 digits
            'password': 'password123',
            'village': 'Village',
            'business_type': 'Food Stall'
        }, follow_redirects=True)
        self.assertIn(b'valid 10-digit', invalid_res.data)

    # -------------------------------------------------------------
    # 3. USER AUTHENTICATION & LOGIN
    # -------------------------------------------------------------
    def test_03_user_login(self):
        """Verify login credentials check and session creation."""
        # Login with demo user
        res = self.client.post('/login', data={
            'mobile_number': '9876543210',
            'password': 'user123'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Welcome back', res.data)

        # Login with bad password
        bad_res = self.client.post('/login', data={
            'mobile_number': '9876543210',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        self.assertIn(b'Invalid mobile number or password', bad_res.data)

    # -------------------------------------------------------------
    # 4. MULTILINGUAL LANGUAGE SWITCHING
    # -------------------------------------------------------------
    def test_04_language_switching(self):
        """Verify switching session language between en, hi, mr."""
        # Switch to Marathi
        res_mr = self.client.get('/set-language/mr', follow_redirects=True)
        self.assertEqual(res_mr.status_code, 200)
        self.assertIn('मराठी'.encode('utf-8'), res_mr.data)

        # Switch to Hindi
        res_hi = self.client.get('/set-language/hi', follow_redirects=True)
        self.assertEqual(res_hi.status_code, 200)
        self.assertIn('हिन्दी'.encode('utf-8'), res_hi.data)

        # Switch back to English
        res_en = self.client.get('/set-language/en', follow_redirects=True)
        self.assertEqual(res_en.status_code, 200)

    # -------------------------------------------------------------
    # 5. BUSINESS FINANCE CALCULATOR UNIT TESTS
    # -------------------------------------------------------------
    def test_05_business_finance_calculations(self):
        """Verify business finance math, profit margin, savings rate and division by zero protection."""
        # Normal case
        calc = calculate_business_finance(monthly_income=50000, monthly_expenses=30000, monthly_savings=5000)
        self.assertTrue(calc['success'])
        self.assertEqual(calc['profit'], 20000.0)
        self.assertEqual(calc['remaining_after_savings'], 15000.0)
        self.assertEqual(calc['profit_percentage'], 40.0) # (20000/50000)*100
        self.assertEqual(calc['savings_percentage'], 10.0) # (5000/50000)*100
        self.assertEqual(calc['health_status'], 'Healthy & Sustainable')

        # Division by zero test: Income = 0
        zero_calc = calculate_business_finance(monthly_income=0, monthly_expenses=500, monthly_savings=0)
        self.assertTrue(zero_calc['success'])
        self.assertEqual(zero_calc['profit_percentage'], 0.0)
        self.assertEqual(zero_calc['savings_percentage'], 0.0)
        self.assertEqual(zero_calc['health_status'], 'Operating at a Loss')

        # Negative values input validation
        neg_calc = calculate_business_finance(monthly_income=-1000, monthly_expenses=500)
        self.assertFalse(neg_calc['success'])

    # -------------------------------------------------------------
    # 6. GOVERNMENT SCHEME MATCHING ENGINE
    # -------------------------------------------------------------
    def test_06_scheme_matching_engine(self):
        """Verify scheme matching rules for matching and non-matching parameters."""
        # 1. Matching case: Kirana shop with ₹30,000 loan need
        match = find_matching_schemes(
            business_type='Small Grocery / Kirana',
            state='All India',
            annual_income=150000,
            required_loan_amount=30000,
            lang='en'
        )
        self.assertTrue(match['success'])
        self.assertGreater(match['count'], 0)
        # Should include MUDRA Shishu
        names = [s['scheme_name'] for s in match['matched_schemes']]
        self.assertTrue(any('MUDRA' in name for name in names))

        # 2. High loan case: ₹50,00,000 for Small Grocery
        high_loan_match = find_matching_schemes(
            business_type='Small Grocery / Kirana',
            state='Maharashtra',
            annual_income=300000,
            required_loan_amount=50000000, # 5 Crore - beyond standard schemes
            lang='en'
        )
        self.assertTrue(high_loan_match['success'])
        self.assertEqual(high_loan_match['count'], 0, "Extreme loan amount should match zero micro-schemes")

    # -------------------------------------------------------------
    # 7. BASIC LOAN GUIDANCE & BUDGET PLANNER
    # -------------------------------------------------------------
    def test_07_loan_guidance_and_budget(self):
        """Verify DTI ratio calculation and budget planner categorizations."""
        guidance = analyze_loan_guidance(
            annual_income=300000,
            business_age_years=2,
            existing_loan_amount=20000,
            required_loan_amount=50000
        )
        self.assertTrue(guidance['success'])
        self.assertIn('dti_percentage', guidance)
        self.assertGreater(len(guidance['categories']), 0)

        # Budget planner
        expenses = {
            'Raw Materials / Stock': 15000,
            'Shop Rent / Stall Fee': 3000,
            'Electricity & Water': 1000,
            'Transport & Freight': 2000,
            'Household Expenses': 8000,
            'Miscellaneous': 1000
        }
        budget = calculate_monthly_budget(monthly_income=35000, expenses_dict=expenses, target_savings=3000)
        self.assertTrue(budget['success'])
        self.assertEqual(budget['total_expenses'], 30000.0)
        self.assertEqual(budget['net_balance'], 5000.0)
        self.assertEqual(budget['balance_after_savings'], 2000.0)

    # -------------------------------------------------------------
    # 8. FEEDBACK SUBMISSION
    # -------------------------------------------------------------
    def test_08_feedback_submission(self):
        """Verify feedback insertion with authenticated user session."""
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['user_name'] = 'Sunita Ramesh Patil'
            sess['mobile'] = '9876543210'

        res = self.client.post('/feedback', data={
            'category': 'Suggestion',
            'rating': '5',
            'message': 'Automated unit test feedback verifying database record persistence.'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)

        # Verify feedback in database
        latest_fb = query_db(
            "SELECT * FROM feedback WHERE message LIKE %s", 
            ('%Automated unit test feedback%',), 
            one=True
        )
        self.assertIsNotNone(latest_fb)
        self.assertEqual(latest_fb['rating'], 5)

    # -------------------------------------------------------------
    # 9. ADMINISTRATOR AUTHORIZATION & CRUD
    # -------------------------------------------------------------
    def test_09_admin_security_and_crud(self):
        """Verify administrator security wall and complete CRUD cycle for schemes."""
        # Non-admin trying to access admin dashboard should be redirected
        anon_res = self.client.get('/admin/dashboard')
        self.assertEqual(anon_res.status_code, 302)
        self.assertIn('/admin/login', anon_res.location)

        # Admin Login
        login_res = self.client.post('/admin/login', data={
            'username': 'admin',
            'password': 'admin123'
        }, follow_redirects=True)
        self.assertEqual(login_res.status_code, 200)
        self.assertIn(b'System Administration', login_res.data)

        # Admin CRUD: Create new scheme
        add_res = self.client.post('/admin/schemes/add', data={
            'scheme_name': 'Test Rural Dairy Grant 2026',
            'scheme_code': 'TEST-DAIRY-2026',
            'category': 'Dairy Subsidy',
            'description_en': 'Sample test grant for dairy entrepreneurs.',
            'description_hi': 'डेयरी उद्यमियों के लिए परीक्षण अनुदान।',
            'description_mr': 'दुग्ध व्यावसायिकांसाठी चाचणी अनुदान.',
            'eligible_business_types': 'Agriculture & Dairy',
            'state_applicability': 'All India',
            'min_loan_amount': '15000',
            'max_loan_amount': '100000',
            'max_annual_income': '250000',
            'subsidy_percentage': '20',
            'required_documents': 'Aadhaar, Animal count letter',
            'how_to_apply': 'Apply through Gram Panchayat',
            'official_portal': 'https://example.gov.in'
        }, follow_redirects=True)
        self.assertEqual(add_res.status_code, 200)

        # Verify Scheme Exists
        added = query_db("SELECT * FROM schemes WHERE scheme_code = %s", ('TEST-DAIRY-2026',), one=True)
        self.assertIsNotNone(added)
        self.assertEqual(added['scheme_name'], 'Test Rural Dairy Grant 2026')

        # Admin CRUD: Edit the scheme
        edit_res = self.client.post(f'/admin/schemes/edit/{added["id"]}', data={
            'scheme_name': 'Updated Rural Dairy Grant 2026',
            'scheme_code': 'TEST-DAIRY-2026',
            'category': 'Dairy Subsidy',
            'description_en': 'Updated description.',
            'description_hi': 'अपडेट विवरण।',
            'description_mr': 'अद्ययावत माहिती.',
            'eligible_business_types': 'Agriculture & Dairy',
            'state_applicability': 'Maharashtra',
            'min_loan_amount': '20000',
            'max_loan_amount': '150000',
            'max_annual_income': '300000',
            'subsidy_percentage': '25',
            'required_documents': 'Aadhaar Card',
            'how_to_apply': 'Direct bank visit',
            'official_portal': 'https://example.gov.in'
        }, follow_redirects=True)
        self.assertEqual(edit_res.status_code, 200)

        updated = query_db("SELECT * FROM schemes WHERE id = %s", (added['id'],), one=True)
        self.assertEqual(updated['scheme_name'], 'Updated Rural Dairy Grant 2026')
        self.assertEqual(updated['subsidy_percentage'], 25.0)

        # Admin CRUD: Delete the scheme
        del_res = self.client.post(f'/admin/schemes/delete/{added["id"]}', follow_redirects=True)
        self.assertEqual(del_res.status_code, 200)
        deleted = query_db("SELECT * FROM schemes WHERE id = %s", (added['id'],), one=True)
        self.assertIsNone(deleted)

if __name__ == '__main__':
    unittest.main()

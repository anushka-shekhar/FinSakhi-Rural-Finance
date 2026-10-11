"""
FinSakhi - Main Web Application Controller (Flask)
Project: FinSakhi - Smart Financial Awareness and Guidance System for Rural Entrepreneurs
Target Audience: Rural Micro-Entrepreneurs (Farmers, Artisans, Small Vendors, SHGs)
Academic Subject Mapping: 
  - Python & Flask (Backend Web Architecture, Routing, Sessions, Security)
  - DBMS & SQL (Relational Database Operations, Parameterized Queries)
  - Object-Oriented & Procedural Programming (Modular Components)
"""

import functools
from flask import (
    Flask, render_template, request, redirect, 
    url_for, session, flash, jsonify
)
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config
from db import init_db, query_db, execute_db
from finance_calc import (
    calculate_business_finance, 
    analyze_loan_guidance, 
    calculate_monthly_budget
)
from scheme_matcher import find_matching_schemes
from translations import TRANSLATIONS, get_text

# Initialize Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Initialize Database connection (MySQL primary, SQLite local fallback)
init_db()

# ====================================================================
# TEMPLATE HELPERS & CONTEXT PROCESSORS
# ====================================================================

@app.context_processor
def inject_global_template_vars():
    """
    Injects the active language code, translation lookup function `t()`,
    and active user session details into all Jinja2 HTML templates.
    """
    current_lang = session.get('lang', Config.DEFAULT_LANGUAGE)
    return {
        'current_lang': current_lang,
        't': lambda key: get_text(key, current_lang),
        'user_name': session.get('user_name'),
        'user_id': session.get('user_id'),
        'is_admin': session.get('is_admin', False)
    }

# ====================================================================
# AUTHENTICATION DECORATORS
# ====================================================================

def login_required(view):
    """Decorator ensuring a user is authenticated before accessing a route."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            flash('Please log in with your mobile number to access this page.', 'warning')
            return redirect(url_for('login', next=request.url))
        return view(**kwargs)
    return wrapped_view

def admin_required(view):
    """Decorator ensuring an administrator is authenticated before accessing admin routes."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not session.get('is_admin'):
            flash('Administrative authorization required. Please log in as administrator.', 'danger')
            return redirect(url_for('admin_login'))
        return view(**kwargs)
    return wrapped_view

# ====================================================================
# LANGUAGE SWITCHER ROUTE
# ====================================================================

@app.route('/set-language/<lang>')
def set_language(lang):
    """
    Switches active session language to English (en), Hindi (hi), or Marathi (mr).
    Redirects back to previous page.
    """
    if lang in Config.LANGUAGES:
        session['lang'] = lang
    return redirect(request.referrer or url_for('index'))

# ====================================================================
# PUBLIC PAGES & HOME
# ====================================================================

@app.route('/')
def index():
    """FinSakhi Home Page."""
    lang = session.get('lang', 'en')
    # Fetch top 3 featured schemes for homepage preview
    schemes = query_db("SELECT id, scheme_name, category, max_loan_amount, subsidy_percentage FROM schemes LIMIT 3")
    # Fetch awareness categories
    awareness_list = query_db("SELECT category_slug, title_en, title_hi, title_mr FROM financial_content ORDER BY display_order ASC")
    
    return render_template(
        'index.html', 
        featured_schemes=schemes, 
        awareness_list=awareness_list,
        lang=lang
    )

# ====================================================================
# USER REGISTRATION, LOGIN & LOGOUT
# ====================================================================

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User Registration: Validates mobile number and securely hashes password."""
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        mobile_number = request.form.get('mobile_number', '').strip()
        password = request.form.get('password', '')
        village = request.form.get('village', '').strip()
        business_type = request.form.get('business_type', '').strip()

        # Input Validation (Sem 1-3 C/Python Logic)
        if not full_name or not mobile_number or not password or not village or not business_type:
            flash('All registration fields are required. Please fill them out.', 'danger')
            return render_template('register.html')

        if len(mobile_number) != 10 or not mobile_number.isdigit():
            flash('Please enter a valid 10-digit Indian mobile number.', 'danger')
            return render_template('register.html')

        if len(password) < 6:
            flash('Password should be at least 6 characters long for security.', 'danger')
            return render_template('register.html')

        # Check for existing mobile number (Unique Constraint Check)
        existing_user = query_db(
            "SELECT id FROM users WHERE mobile_number = %s", 
            (mobile_number,), 
            one=True
        )
        if existing_user:
            flash('This mobile number is already registered. Please log in.', 'warning')
            return redirect(url_for('login'))

        # Secure password hashing (Werkzeug scrypt)
        password_hash = generate_password_hash(password)

        try:
            execute_db(
                """
                INSERT INTO users (full_name, mobile_number, password_hash, village, business_type)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (full_name, mobile_number, password_hash, village, business_type)
            )
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'An error occurred during registration: {e}', 'danger')
            return render_template('register.html')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User Login: Authenticates user against stored password hash."""
    if request.method == 'POST':
        mobile_number = request.form.get('mobile_number', '').strip()
        password = request.form.get('password', '')

        if not mobile_number or not password:
            flash('Please enter both mobile number and password.', 'danger')
            return render_template('login.html')

        user = query_db(
            "SELECT * FROM users WHERE mobile_number = %s", 
            (mobile_number,), 
            one=True
        )

        if user and check_password_hash(user['password_hash'], password):
            # Establish session variables
            session.clear()
            session['user_id'] = user['id']
            session['user_name'] = user['full_name']
            session['mobile'] = user['mobile_number']
            session['village'] = user['village']
            session['business_type'] = user['business_type']
            session['is_admin'] = False

            flash(f'Welcome back, {user["full_name"]}!', 'success')
            next_url = request.args.get('next')
            return redirect(next_url or url_for('dashboard'))
        else:
            flash('Invalid mobile number or password. Please try again.', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    """Terminates active user or administrator session."""
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))


@app.route('/dashboard')
@login_required
def dashboard():
    """User Dashboard: Displays entrepreneur details, quick tools, and user activity."""
    user_id = session.get('user_id')
    user = query_db("SELECT * FROM users WHERE id = %s", (user_id,), one=True)
    user_feedback = query_db("SELECT * FROM feedback WHERE user_id = %s ORDER BY id DESC LIMIT 5", (user_id,))
    
    return render_template('dashboard.html', user=user, feedback_list=user_feedback)

# ====================================================================
# GOVERNMENT SCHEME FINDER
# ====================================================================

@app.route('/schemes', methods=['GET', 'POST'])
def schemes():
    """
    Government Scheme Finder:
    Evaluates applicant criteria against schemes database using deterministic rules.
    """
    lang = session.get('lang', 'en')
    matched_data = None
    has_searched = False

    business_types = [
        'Agriculture & Dairy',
        'Small Grocery / Kirana',
        'Handicrafts & Tailoring',
        'Food Stall',
        'Poultry & Livestock',
        'Service & Repairs',
        'Other Micro Enterprise'
    ]
    
    states = [
        'All India',
        'Maharashtra',
        'Uttar Pradesh',
        'Madhya Pradesh',
        'Rajasthan',
        'Bihar',
        'Gujarat',
        'Karnataka',
        'Punjab',
        'Tamil Nadu',
        'West Bengal'
    ]

    if request.method == 'POST':
        has_searched = True
        business_type = request.form.get('business_type', 'Small Grocery / Kirana')
        state = request.form.get('state', 'All India')
        annual_income = request.form.get('annual_income', '150000')
        required_loan = request.form.get('required_loan', '50000')

        matched_data = find_matching_schemes(
            business_type=business_type,
            state=state,
            annual_income=annual_income,
            required_loan_amount=required_loan,
            lang=lang
        )

    # If GET, fetch all schemes for general browsing
    all_schemes = query_db("SELECT * FROM schemes ORDER BY id ASC")

    return render_template(
        'schemes.html',
        business_types=business_types,
        states=states,
        matched_data=matched_data,
        has_searched=has_searched,
        all_schemes=all_schemes,
        lang=lang
    )

# ====================================================================
# FINANCIAL AWARENESS MODULE
# ====================================================================

@app.route('/awareness')
def awareness():
    """Lists all financial literacy categories."""
    lang = session.get('lang', 'en')
    articles = query_db("SELECT * FROM financial_content ORDER BY display_order ASC")
    return render_template('awareness.html', articles=articles, lang=lang)


@app.route('/awareness/<category_slug>')
def awareness_detail(category_slug):
    """Detailed view for a specific financial awareness topic."""
    lang = session.get('lang', 'en')
    article = query_db("SELECT * FROM financial_content WHERE category_slug = %s", (category_slug,), one=True)
    if not article:
        flash('Financial topic not found.', 'warning')
        return redirect(url_for('awareness'))

    # Extract active language content
    content_view = {
        'title': article.get(f'title_{lang}') or article.get('title_en'),
        'explanation': article.get(f'explanation_{lang}') or article.get('explanation_en'),
        'example': article.get(f'example_{lang}') or article.get('example_en'),
        'safety_tips': article.get(f'safety_tips_{lang}') or article.get('safety_tips_en'),
        'category_slug': article.get('category_slug')
    }

    # Fetch next/other topics for quick navigation
    other_topics = query_db("SELECT category_slug, title_en, title_hi, title_mr FROM financial_content WHERE category_slug != %s LIMIT 5", (category_slug,))

    return render_template('awareness_detail.html', article=content_view, other_topics=other_topics, lang=lang)

# ====================================================================
# BASIC LOAN GUIDANCE MODULE
# ====================================================================

@app.route('/loan-guidance', methods=['GET', 'POST'])
def loan_guidance():
    """Educational assessment of borrowing capacity and preparation tips."""
    guidance_result = None
    if request.method == 'POST':
        annual_income = request.form.get('annual_income', '0')
        business_age = request.form.get('business_age', '0')
        existing_loan = request.form.get('existing_loan', '0')
        required_loan = request.form.get('required_loan', '0')

        guidance_result = analyze_loan_guidance(
            annual_income=annual_income,
            business_age_years=business_age,
            existing_loan_amount=existing_loan,
            required_loan_amount=required_loan
        )

    return render_template('loan_guidance.html', guidance=guidance_result)

# ====================================================================
# BUSINESS FINANCE CALCULATOR MODULE
# ====================================================================

@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    """
    Business Finance Calculator:
    Computes Net Profit, Remaining Balance, Profit Margin %, and Savings Rate %.
    """
    calc_result = None
    if request.method == 'POST':
        income = request.form.get('monthly_income', '0')
        expenses = request.form.get('monthly_expenses', '0')
        savings = request.form.get('monthly_savings', '0')

        calc_result = calculate_business_finance(
            monthly_income=income,
            monthly_expenses=expenses,
            monthly_savings=savings
        )

    return render_template('calculator.html', result=calc_result)

# ====================================================================
# BUDGET PLANNER MODULE
# ====================================================================

@app.route('/budget-planner', methods=['GET', 'POST'])
def budget_planner():
    """Categorized monthly budget planner for rural enterprises."""
    budget_result = None
    if request.method == 'POST':
        monthly_income = request.form.get('monthly_income', '0')
        target_savings = request.form.get('target_savings', '0')
        
        expenses_dict = {
            'Raw Materials / Stock': request.form.get('exp_raw_materials', '0'),
            'Shop Rent / Stall Fee': request.form.get('exp_rent', '0'),
            'Electricity & Water': request.form.get('exp_utilities', '0'),
            'Transport & Freight': request.form.get('exp_transport', '0'),
            'Household Expenses': request.form.get('exp_household', '0'),
            'Miscellaneous': request.form.get('exp_misc', '0')
        }

        budget_result = calculate_monthly_budget(
            monthly_income=monthly_income,
            expenses_dict=expenses_dict,
            target_savings=target_savings
        )

    return render_template('budget_planner.html', budget=budget_result)

# ====================================================================
# DIGITAL FRAUD AWARENESS MODULE
# ====================================================================

@app.route('/fraud-awareness')
def fraud_awareness():
    """Detailed awareness on UPI scams, OTP fraud, fake loan websites, and safety rules."""
    return render_template('fraud_awareness.html')

# ====================================================================
# FEEDBACK MODULE
# ====================================================================

@app.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback():
    """Allows logged-in users to submit suggestions and reviews."""
    if request.method == 'POST':
        user_id = session.get('user_id')
        user_name = session.get('user_name')
        mobile = session.get('mobile')
        category = request.form.get('category', 'Suggestion')
        rating = int(request.form.get('rating', '5'))
        message = request.form.get('message', '').strip()

        if not message:
            flash('Please enter your feedback message.', 'danger')
            return render_template('feedback.html')

        try:
            execute_db(
                """
                INSERT INTO feedback (user_id, user_name, mobile_number, category, rating, message, status)
                VALUES (%s, %s, %s, %s, %s, %s, 'Reviewed')
                """,
                (user_id, user_name, mobile, category, rating, message)
            )
            flash('Thank you! Your feedback has been submitted successfully.', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f'Error recording feedback: {e}', 'danger')

    return render_template('feedback.html')

# ====================================================================
# ADMINISTRATOR DASHBOARD & CMS
# ====================================================================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Administrator Login: Authenticates administrators against admin_users table."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        admin = query_db("SELECT * FROM admin_users WHERE username = %s", (username,), one=True)
        if admin and check_password_hash(admin['password_hash'], password):
            session.clear()
            session['admin_id'] = admin['id']
            session['user_name'] = admin['full_name']
            session['admin_username'] = admin['username']
            session['is_admin'] = True

            flash('Welcome Administrator. System access granted.', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid administrator credentials.', 'danger')

    return render_template('admin/admin_login.html')


@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    """Administrator Overview: Stats, user feedback, and management links."""
    # Summary Statistics
    total_users = query_db("SELECT COUNT(*) as count FROM users", one=True)['count']
    total_schemes = query_db("SELECT COUNT(*) as count FROM schemes", one=True)['count']
    total_feedback = query_db("SELECT COUNT(*) as count FROM feedback", one=True)['count']
    total_articles = query_db("SELECT COUNT(*) as count FROM financial_content", one=True)['count']
    
    # Recent Feedback
    recent_feedback = query_db("SELECT * FROM feedback ORDER BY id DESC LIMIT 10")
    
    return render_template(
        'admin/admin_dashboard.html',
        stats={
            'users': total_users,
            'schemes': total_schemes,
            'feedback': total_feedback,
            'articles': total_articles
        },
        feedback_list=recent_feedback
    )


@app.route('/admin/schemes')
@admin_required
def admin_schemes():
    """Admin CRUD: Lists all government schemes with options to Add, Edit, or Delete."""
    schemes = query_db("SELECT * FROM schemes ORDER BY id DESC")
    return render_template('admin/manage_schemes.html', schemes=schemes)


@app.route('/admin/schemes/add', methods=['GET', 'POST'])
@admin_required
def admin_add_scheme():
    """Admin CRUD: Inserts a new government scheme."""
    if request.method == 'POST':
        scheme_name = request.form.get('scheme_name')
        scheme_code = request.form.get('scheme_code')
        category = request.form.get('category')
        description_en = request.form.get('description_en')
        description_hi = request.form.get('description_hi')
        description_mr = request.form.get('description_mr')
        eligible_business_types = request.form.get('eligible_business_types')
        state_applicability = request.form.get('state_applicability')
        max_annual_income = float(request.form.get('max_annual_income', 0))
        min_loan_amount = float(request.form.get('min_loan_amount', 10000))
        max_loan_amount = float(request.form.get('max_loan_amount', 1000000))
        subsidy_percentage = float(request.form.get('subsidy_percentage', 0))
        required_documents = request.form.get('required_documents')
        how_to_apply = request.form.get('how_to_apply')
        official_portal = request.form.get('official_portal')

        try:
            execute_db(
                """
                INSERT INTO schemes (
                    scheme_name, scheme_code, category,
                    description_en, description_hi, description_mr,
                    eligible_business_types, state_applicability,
                    max_annual_income, min_loan_amount, max_loan_amount,
                    subsidy_percentage, required_documents, how_to_apply, official_portal
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    scheme_name, scheme_code, category,
                    description_en, description_hi, description_mr,
                    eligible_business_types, state_applicability,
                    max_annual_income, min_loan_amount, max_loan_amount,
                    subsidy_percentage, required_documents, how_to_apply, official_portal
                )
            )
            flash('New scheme added successfully!', 'success')
            return redirect(url_for('admin_schemes'))
        except Exception as e:
            flash(f'Error adding scheme: {e}', 'danger')

    return render_template('admin/scheme_form.html', action='Add', scheme=None)


@app.route('/admin/schemes/edit/<int:scheme_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_scheme(scheme_id):
    """Admin CRUD: Updates an existing government scheme."""
    scheme = query_db("SELECT * FROM schemes WHERE id = %s", (scheme_id,), one=True)
    if not scheme:
        flash('Scheme record not found.', 'danger')
        return redirect(url_for('admin_schemes'))

    if request.method == 'POST':
        scheme_name = request.form.get('scheme_name')
        scheme_code = request.form.get('scheme_code')
        category = request.form.get('category')
        description_en = request.form.get('description_en')
        description_hi = request.form.get('description_hi')
        description_mr = request.form.get('description_mr')
        eligible_business_types = request.form.get('eligible_business_types')
        state_applicability = request.form.get('state_applicability')
        max_annual_income = float(request.form.get('max_annual_income', 0))
        min_loan_amount = float(request.form.get('min_loan_amount', 10000))
        max_loan_amount = float(request.form.get('max_loan_amount', 1000000))
        subsidy_percentage = float(request.form.get('subsidy_percentage', 0))
        required_documents = request.form.get('required_documents')
        how_to_apply = request.form.get('how_to_apply')
        official_portal = request.form.get('official_portal')

        try:
            execute_db(
                """
                UPDATE schemes SET
                    scheme_name = %s, scheme_code = %s, category = %s,
                    description_en = %s, description_hi = %s, description_mr = %s,
                    eligible_business_types = %s, state_applicability = %s,
                    max_annual_income = %s, min_loan_amount = %s, max_loan_amount = %s,
                    subsidy_percentage = %s, required_documents = %s, how_to_apply = %s, official_portal = %s
                WHERE id = %s
                """,
                (
                    scheme_name, scheme_code, category,
                    description_en, description_hi, description_mr,
                    eligible_business_types, state_applicability,
                    max_annual_income, min_loan_amount, max_loan_amount,
                    subsidy_percentage, required_documents, how_to_apply, official_portal,
                    scheme_id
                )
            )
            flash('Scheme updated successfully!', 'success')
            return redirect(url_for('admin_schemes'))
        except Exception as e:
            flash(f'Error updating scheme: {e}', 'danger')

    return render_template('admin/scheme_form.html', action='Edit', scheme=scheme)


@app.route('/admin/schemes/delete/<int:scheme_id>', methods=['POST'])
@admin_required
def admin_delete_scheme(scheme_id):
    """Admin CRUD: Deletes a scheme from the database."""
    try:
        execute_db("DELETE FROM schemes WHERE id = %s", (scheme_id,))
        flash('Scheme deleted successfully.', 'info')
    except Exception as e:
        flash(f'Error deleting scheme: {e}', 'danger')
    return redirect(url_for('admin_schemes'))


# ====================================================================
# APPLICATION ENTRYPOINT
# ====================================================================

if __name__ == '__main__':
    # Run server accessible across the local network (host='0.0.0.0') on port 5000
    app.run(debug=True, host='0.0.0.0', port=5000)


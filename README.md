# FinSakhi – Smart Financial Awareness & Guidance System for Rural Entrepreneurs

**A Complete Academic Computer Engineering Project (Semester 1–3 Focus)**  
*Developed for College Project Submission, Viva-Voce Demonstration, and Rural Financial Literacy.*

---

## 1. Project Overview & Problem Statement
Rural micro-entrepreneurs in India—such as village grocery (*kirana*) shopkeepers, dairy farmers, vegetable vendors, tailor artisans, and women in Self-Help Groups (SHGs)—face significant challenges in accessing formal credit and navigating digital banking:
1. **Language & Jargon Barriers:** Most banking applications use complex financial terminology.
2. **Awareness Deficit:** Entrepreneurs miss out on government subsidies (such as MUDRA, PM SVANidhi, PMEGP, KCC) because criteria are difficult to understand.
3. **Calculation Difficulties:** Estimating true business profit margin vs. daily cash flow often leads to unplanned losses.
4. **Cyber Fraud Vulnerability:** Rural citizens are heavily targeted by fake UPI "money request" scams, lottery SMS, and illegal high-interest loan apps.

**FinSakhi** solves these challenges by providing a clean, accessible, multilingual (English, Hindi, Marathi) web application built using fundamental computer engineering concepts.

---

## 2. Academic Subject Mapping (Semester 1–3 Computer Engineering)

| Semester Subject | Theoretical Concept | Concrete Implementation in FinSakhi |
| :--- | :--- | :--- |
| **DBMS (Database Management Systems)** | Relational Schema Design, Normalization, Primary Keys, Foreign Keys, Referential Integrity, Constraints | Tables: `users`, `schemes`, `financial_content`, `feedback`, `admin_users`. `feedback.user_id` has a foreign key referencing `users(id)`. |
| **SQL (Structured Query Language)** | Parameterized Prepared Statements, CRUD Operations, ACID Transactions, Indexing | Parameterized queries (`%s` placeholders in `db.py`) prevent SQL Injection. Complete CRUD implementation for schemes in the Admin portal. |
| **Python Programming** | Functions, Dictionaries, Decorators, Session Management, Modular Architecture | Flask routing controllers in `app.py`, custom auth decorators (`@login_required`, `@admin_required`), Jinja2 templating context processors. |
| **Object-Oriented & Procedural Logic (C / C++ / Python)** | Procedural Abstraction, Conditional Branching, Boundary Value Testing, Division-by-Zero Handling | `finance_calc.py` strictly checks `income > 0` before computing percentages. `scheme_matcher.py` uses deterministic `if-else` trees. |
| **Web Technologies (HTML5 & CSS3)** | Semantic Markup, CSS Grid, Flexbox, Mobile-Responsive Design | HTML5 semantic elements (`<header>`, `<nav>`, `<main>`, `<section>`). Clean CSS with green, cream, and white palette without heavy external frameworks. |
| **Data Security & Cryptography** | Password Hashing, Salted Hashes, Session Isolation | Werkzeug Scrypt password hashing (`generate_password_hash`, `check_password_hash`). No plaintext passwords stored. |

---

## 3. Technology Stack

* **Frontend:** Semantic HTML5, CSS3 (Mobile-first responsive design), Vanilla JavaScript (no external bloated frameworks).
* **Backend:** Python 3 with Flask framework.
* **Database:** MySQL 8.0 (`finsakhi_db`), relational SQL queries with parameterized statements.
* **Localization:** Predefined, human-reviewed dictionary and database content in **English**, **Hindi (हिन्दी)**, and **Marathi (मराठी)**.
* **Development Environment:** VS Code compatible structure.

---

## 4. Project Directory Structure

```text
finsakhi/
├── app.py                     # Main Flask Application & Route Controller
├── config.py                  # Database & Security Configuration
├── db.py                      # DBMS Connector & Parameterized Query Execution
├── finance_calc.py            # Business Finance & Loan Math Engine
├── scheme_matcher.py          # Deterministic Scheme Eligibility Matcher
├── translations.py            # Human-Reviewed Dictionary (EN, HI, MR)
├── requirements.txt           # Python Package Dependencies
├── test_app.py                # Automated Test Suite (9 Tests)
├── .env.example               # Database Credentials Configuration Template
├── .venv/                     # Dedicated Virtual Environment
├── database/
│   ├── finsakhi_db.sql        # MySQL Database Schema & Sample Data Script
│   └── seed_data.py           # Fallback Seeder Script
├── static/
│   ├── css/
│   │   ├── style.css          # Green/Cream/White Palette & Responsive Layout
│   │   └── dashboard.css      # Dashboard & Admin Data Table Styles
│   ├── js/
│   │   ├── main.js            # Menu Toggle & Input Validation
│   │   ├── calculator.js      # Real-Time Business Finance Calculator Preview
│   │   └── budget.js          # Interactive Budget Planner Calculator
│   └── images/
│       └── logo.svg           # Professional FinSakhi Vector Brand Logo
└── templates/
    ├── base.html              # Master Layout Template with Nav & Language Switcher
    ├── index.html             # Home Page: Welcome, Modules, How It Helps
    ├── register.html          # Rural Entrepreneur Registration
    ├── login.html             # User Login
    ├── dashboard.html         # User Dashboard
    ├── schemes.html           # Government Scheme Finder & Results
    ├── awareness.html         # Financial Awareness Lessons Catalog
    ├── awareness_detail.html   # Detailed Lesson View (Example & Safety Tip)
    ├── loan_guidance.html     # Loan Readiness & DTI Assessment
    ├── calculator.html        # Business Finance Calculator
    ├── budget_planner.html    # Monthly Budget Planner
    ├── fraud_awareness.html   # Digital Fraud Shield & Scam Guidance
    ├── feedback.html          # Citizen Feedback Submission
    └── admin/
        ├── admin_login.html   # Administrator Login
        ├── admin_dashboard.html # Admin Dashboard with Statistics & Feedback
        ├── manage_schemes.html  # Scheme Management CRUD Table
        └── scheme_form.html   # Add & Edit Scheme Form
```

---

## 5. Step-by-Step Local Setup & Execution

### Step 1: Open in VS Code
Open the `finsakhi` directory inside Visual Studio Code:
```powershell
cd "C:\Users\Anushka Shekhar\.gemini\antigravity\scratch\finsakhi"
code .
```

### Step 2: Configure MySQL Database
1. Open your MySQL CLI or **MySQL Workbench**.
2. Run the provided SQL script to create `finsakhi_db` and insert sample data:
   ```bash
   mysql -u root -p < database/finsakhi_db.sql
   ```
   *(Or in MySQL Workbench: Open `database/finsakhi_db.sql` and click Execute).*
3. Copy `.env.example` to `.env` and fill in your MySQL root password:
   ```ini
   MYSQL_HOST=localhost
   MYSQL_PORT=3306
   MYSQL_USER=root
   MYSQL_PASSWORD=your_actual_mysql_password
   MYSQL_DB=finsakhi_db
   ```
> **Note on Zero-Downtime Fallback:** If you run the application before entering your MySQL password, `db.py` automatically runs using a local fallback database (`finsakhi_local.db`) so the project will never crash during a demonstration!

### Step 3: Run the Flask Web Application
Using the pre-configured virtual environment:
```powershell
.\.venv\Scripts\python app.py
```
Open your web browser at: **`http://127.0.0.1:5000`**

---

## 6. Default Demo Credentials (For Presentation / Viva)

| Role | Username / Mobile | Password | Access Level |
| :--- | :--- | :--- | :--- |
| **System Administrator** | `admin` | `admin123` | Full CMS, Feedback Viewer, Scheme Add/Edit/Delete |
| **Rural Entrepreneur 1** | `9876543210` | `user123` | Dairy Business Owner Profile & Dashboard |
| **Rural Entrepreneur 2** | `9811223344` | `user123` | Kirana / Grocery Store Owner Profile |

---

## 7. Running the Automated Test Suite

To verify all system features, security validations, and mathematical calculations:
```powershell
.\.venv\Scripts\python test_app.py
```
**Test Results:**
* `test_01`: Database relational tables verified.
* `test_02`: User registration & password hashing verified.
* `test_03`: Authentication & sessions verified.
* `test_04`: Multilingual switching (EN, HI, MR) verified.
* `test_05`: Business Finance math & zero-division protection verified.
* `test_06`: Government Scheme matching algorithm verified.
* `test_07`: Debt-to-Income (DTI) & Budget calculations verified.
* `test_08`: Feedback insertion verified.
* `test_09`: Administrator security wall & Scheme CRUD lifecycle verified.

---

## 8. College Viva-Voce (Oral Exam) Preparation Guide

### Q1: Why did you use Flask instead of Django or React?
**Answer:** Flask is a lightweight WSGI web framework that allows us to demonstrate core Computer Engineering fundamentals taught in Semesters 1–3 (standard HTTP methods, session cookies, manual SQL integration, and modular functions) without hiding the architectural mechanics behind complex third-party abstractions.

### Q2: How is SQL Injection prevented in your code?
**Answer:** In `db.py`, all queries use **parameterized statements** (e.g. `cursor.execute("SELECT * FROM users WHERE mobile_number = %s", (mobile_number,))`). The database driver sends the SQL command and user inputs separately, treating parameters purely as data rather than executable SQL syntax.

### Q3: How does the Government Scheme Finder work?
**Answer:** In `scheme_matcher.py`, candidate records are retrieved from the MySQL `schemes` table and evaluated against deterministic boolean criteria:
1. `State Match`: Scheme state is 'All India' or matches the applicant's state.
2. `Business Match`: Scheme accepts 'All' or matches the selected enterprise category.
3. `Income Ceiling`: Applicant's income is $\le$ `max_annual_income` (or ceiling is 0, denoting no restriction).
4. `Loan Range`: Requested loan is within the scheme's minimum and maximum thresholds.

### Q4: How is password security handled?
**Answer:** Passwords are never stored in plaintext. We utilize Werkzeug's `generate_password_hash` algorithm which uses salted key derivation (`scrypt`), protecting against rainbow table attacks and credential leaks.

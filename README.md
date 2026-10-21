# FinSakhi — Smart Financial Awareness & Guidance System for Rural Entrepreneurs

**Academic Computer Engineering Project — SE CMPN C | SLRTCE Mumbai**  
*A multilingual web application empowering rural micro-entrepreneurs with financial literacy and government scheme discovery.*

---

## 1. Project Overview & Problem Statement

Rural micro-entrepreneurs in India — village grocery (*kirana*) shopkeepers, dairy farmers, vegetable vendors, tailor artisans, and women in Self-Help Groups (SHGs) — face significant challenges:

1. **Language & Jargon Barriers:** Most banking applications use complex financial terminology.
2. **Awareness Deficit:** Entrepreneurs miss government subsidies (MUDRA, PM SVANidhi, PMFME, NRLM) because eligibility criteria are hard to understand.
3. **Cyber Fraud Vulnerability:** Rural citizens are targeted by fake UPI scams, lottery SMS, and illegal high-interest loan apps.

**FinSakhi** (Financial Friend) solves these by providing a clean, multilingual (English, Hindi, Marathi) web application using core Computer Engineering concepts.

---

## 2. Academic Subject Mapping (SE Computer Engineering)

| Subject | Concept | Implementation in FinSakhi |
|:---|:---|:---|
| **DBMS** | Relational Schema, Normalization, Primary/Foreign Keys, ACID | Tables: `users`, `schemes`, `financial_content`, `feedback`, `admin_users` |
| **SQL** | Parameterized Queries, CRUD, Transactions | `%s` placeholders in `db.py` prevent SQL Injection; full CRUD in Admin panel |
| **Python Programming** | Functions, Decorators, Sessions, Modular Architecture | Flask routing in `app.py`, `@login_required`, `@admin_required` decorators |
| **Web Technologies** | HTML5, CSS3, Responsive Design | Semantic HTML5 elements, CSS Grid/Flexbox, mobile-first responsive layout |
| **Data Security** | Password Hashing, Session Isolation | Werkzeug `generate_password_hash` (scrypt), no plaintext passwords stored |
| **Cloud Deployment** | PostgreSQL, Environment Variables, CI/CD | Render cloud hosting, GitHub auto-deploy, persistent PostgreSQL database |

---

## 3. Technology Stack

| Layer | Technology | Purpose |
|:---|:---|:---|
| **Frontend** | HTML5, CSS3, Vanilla JavaScript | User interface, responsive design, form validation |
| **Template Engine** | Jinja2 | Dynamic HTML rendering with database data |
| **Backend** | Python 3, Flask | Route handling, sessions, business logic |
| **Security** | Werkzeug | Password hashing (scrypt), input validation |
| **Database (Cloud)** | PostgreSQL 16 (Render) | Persistent cloud storage — all user data stored permanently |
| **Database (Local)** | SQLite | Offline development fallback |
| **Web Server** | Gunicorn | Production WSGI server on Render |
| **Hosting** | Render (Free Tier) | 24/7 cloud deployment |
| **Version Control** | Git + GitHub | Source code management, auto-deploy trigger |

---

## 4. Features

### User-Facing Features
| Feature | Route | Description |
|:---|:---|:---|
| Home Page | `/` | Welcome page with featured schemes and awareness topics |
| User Registration | `/register` | Create account with mobile number, village, business type |
| User Login | `/login` | Secure login using mobile number + password |
| User Dashboard | `/dashboard` | Personalized profile view |
| **Government Scheme Finder** | `/schemes` | Enter business profile → get matching government schemes |
| **Financial Awareness** | `/awareness` | 6 categories of financial education in EN/HI/MR |
| Awareness Detail | `/awareness/<slug>` | Explanation, real example, safety tips per topic |
| Fraud Awareness | `/fraud-awareness` | Digital fraud prevention, scam types, helpline 1930 |
| Feedback | `/feedback` | Submit rating and message |

### Admin Features
| Feature | Route | Description |
|:---|:---|:---|
| Admin Login | `/admin/login` | Separate admin authentication |
| Admin Dashboard | `/admin/dashboard` | Stats: total users, schemes, feedback |
| Manage Schemes | `/admin/schemes` | View all government schemes |
| Add Scheme | `/admin/schemes/add` | Add new government scheme |
| Edit Scheme | `/admin/schemes/edit/<id>` | Update scheme details |
| Delete Scheme | `/admin/schemes/delete/<id>` | Remove a scheme |

### Multilingual Support
- **English** (EN), **Hindi** (HI), **Marathi** (MR)
- Language switcher in navigation bar — all content switches dynamically
- Implemented via `translations.py` dictionary + multilingual DB columns

---

## 5. Government Schemes in Database (8 Schemes)

| Scheme | Loan Range | For |
|:---|:---|:---|
| PM SVANidhi | Up to ₹50,000 | Street vendors, kirana, food stalls |
| Mudra Yojana - Shishu | ₹10,000–₹50,000 | All micro businesses |
| Mudra Yojana - Kishor | ₹50,001–₹5 lakh | Growing micro businesses |
| Mudra Yojana - Tarun | ₹5 lakh–₹10 lakh | Established micro enterprises |
| NRLM - SHG Loan | ₹25,000–₹3 lakh | Women Self-Help Groups (3% subsidy) |
| PMFME Scheme | ₹1 lakh–₹10 lakh | Food processing, dairy, agro (35% subsidy) |
| Stand Up India | ₹10 lakh–₹1 crore | SC/ST & women entrepreneurs |
| CGTMSE Scheme | ₹1 lakh–₹2 crore | Collateral-free MSME loans |

---

## 6. Database Architecture

**Priority Order:** PostgreSQL (Render Cloud) → MySQL → SQLite (local fallback)

### Tables (5 Tables)

```
users              — Registered rural entrepreneurs
admin_users        — Administrator accounts
schemes            — Government scheme data (multilingual)
financial_content  — Awareness education content (multilingual)
feedback           — User feedback submissions
```

### Database Connection (`db.py`)
- `DATABASE_URL` env variable → connects to **PostgreSQL** on Render (persistent, permanent)
- Falls back to MySQL if available locally
- Falls back to SQLite file (`database/finsakhi_local.db`) for offline development

---

## 7. Project Directory Structure

```
finsakhi/
├── app.py                    # Main Flask Application & Route Controller
├── config.py                 # Database & Security Configuration
├── db.py                     # DB Connector (PostgreSQL / MySQL / SQLite)
├── scheme_matcher.py         # Deterministic Scheme Eligibility Matcher
├── translations.py           # Multilingual Dictionary (EN, HI, MR)
├── requirements.txt          # Python Package Dependencies
├── database/
│   ├── finsakhi_db.sql       # MySQL Schema Script
│   ├── finsakhi_local.db     # Local SQLite Fallback
│   └── seed_data.py          # Initial Data Seeder
├── static/
│   ├── css/style.css         # Green/Cream/White Responsive Stylesheet
│   ├── js/main.js            # Frontend JavaScript
│   └── images/               # Logo & Icons
└── templates/
    ├── base.html             # Base Layout (header, footer, nav)
    ├── index.html            # Home Page
    ├── register.html         # Registration Form
    ├── login.html            # Login Form
    ├── dashboard.html        # User Dashboard
    ├── schemes.html          # Government Scheme Finder
    ├── awareness.html        # Awareness Categories List
    ├── awareness_detail.html # Individual Awareness Topic
    ├── fraud_awareness.html  # Fraud Shield & Scam Guidance
    ├── feedback.html         # Feedback Submission
    └── admin/
        ├── admin_login.html       # Admin Login
        ├── admin_dashboard.html   # Admin Dashboard with Stats
        ├── manage_schemes.html    # Scheme CRUD Table
        └── scheme_form.html       # Add/Edit Scheme Form
```

---

## 8. Local Setup & Execution

### Step 1: Open Project
```powershell
cd "C:\Users\Anushka Shekhar\.gemini\antigravity\scratch\finsakhi"
```

### Step 2: Run Locally (SQLite fallback — no DB setup needed)
```powershell
.\.venv\Scripts\python app.py
```
Open browser at: **`http://127.0.0.1:5000`**

> The app automatically uses SQLite if MySQL/PostgreSQL is not configured — no crash during demo!

### Step 3: Live Website
The app is deployed at: **[https://finsakhi-rural-finance.onrender.com](https://finsakhi-rural-finance.onrender.com)**

---

## 9. Default Demo Credentials

| Role | Username / Mobile | Password | Access |
|:---|:---|:---|:---|
| **System Administrator** | `admin` | `admin123` | Full CMS, Feedback Viewer, Scheme CRUD |
| **Demo User 1** | `9876543210` | `user123` | Dairy Business Owner Dashboard |
| **Demo User 2** | `9811223344` | `user123` | Kirana Store Owner Dashboard |

---

## 10. Security Implementation

| Security Feature | How It Works |
|:---|:---|
| **Password Hashing** | `generate_password_hash()` uses scrypt — no plaintext passwords in DB |
| **SQL Injection Prevention** | All queries use `%s` parameterized placeholders |
| **Session Security** | Flask session cookies with SECRET_KEY signing |
| **Login Required** | `@login_required` decorator blocks unauthenticated access to protected routes |
| **Admin Required** | `@admin_required` decorator protects all `/admin/*` routes separately |

---

## 11. Viva-Voce Preparation

### Q1: Why Flask instead of Django?
**Answer:** Flask is lightweight and lets us demonstrate core CE fundamentals (HTTP methods, sessions, manual SQL, modular functions) without hiding the mechanics behind heavy abstractions.

### Q2: How is SQL Injection prevented?
**Answer:** In `db.py`, all queries use parameterized statements — `cursor.execute("SELECT * FROM users WHERE mobile_number = %s", (mobile_number,))`. The driver sends SQL and user input separately, so input is never treated as executable SQL.

### Q3: How does the Scheme Finder work?
**Answer:** In `scheme_matcher.py`, all schemes are fetched from the database and evaluated using 4 deterministic rules:
1. **State Match** — scheme is 'All India' or matches selected state
2. **Business Type Match** — scheme eligible types contain user's business type
3. **Income Ceiling** — user's income ≤ max_annual_income (or no ceiling)
4. **Loan Range** — required loan is within scheme's min–max range

### Q4: How is password security handled?
**Answer:** Werkzeug's `generate_password_hash` uses salted scrypt derivation. Even if the database is breached, passwords cannot be read — `check_password_hash` verifies without ever storing plaintext.

### Q5: Where is user data stored?
**Answer:** On the live website, data is stored in **PostgreSQL** on Render's cloud servers. The `DATABASE_URL` environment variable connects the app to this persistent database. Data survives server restarts, sleeps, and redeployments.

### Q6: How does multilingual support work?
**Answer:** `translations.py` is a Python dictionary mapping text keys to 3 language values. When a user switches language, their preference is saved in Flask session. All templates call `t('key')` — a helper that returns the string in the active language.

### Q7: How is the app deployed?
**Answer:** Code is pushed to GitHub → Render detects the push via webhook → automatically builds (installs requirements.txt) → runs `gunicorn app:app` → site goes live.

---

## 12. Live Links

| Resource | URL |
|:---|:---|
| 🌐 Live Website | [https://finsakhi-rural-finance.onrender.com](https://finsakhi-rural-finance.onrender.com) |
| 💻 GitHub Repository | [https://github.com/anushka-shekhar/FinSakhi-Rural-Finance](https://github.com/anushka-shekhar/FinSakhi-Rural-Finance) |

---

*FinSakhi — An Educational Initiative for Rural Entrepreneurship & Financial Literacy.*  
*Academic College Project. All scheme information is for educational awareness only.*

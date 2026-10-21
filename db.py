"""
FinSakhi - Database Connection & Abstraction Layer
Subject Mapping: DBMS & SQL (Relational Databases, Parameterized Queries, ACID Transactions)

This module handles:
1. Connection to PostgreSQL (Render Cloud) via DATABASE_URL environment variable.
2. Connection to MySQL Server (Target: MySQL 8.0 `finsakhi_db`) as second option.
3. Parameterized SQL queries to prevent SQL Injection (DBMS Security).
4. Safe execution of CRUD operations (Create, Read, Update, Delete).
5. Automatic fallback to local SQLite database if no cloud/MySQL DB is configured,
   ensuring the application is immediately testable while preserving full compatibility.

Database Priority:
  1. PostgreSQL (DATABASE_URL set) — Render Cloud persistent storage
  2. MySQL (MYSQL_HOST configured)  — Local or remote MySQL server
  3. SQLite                          — Local offline development fallback
"""

import os
import sqlite3
from config import Config

# Global variable to track active database backend
ACTIVE_DB_BACKEND = "sqlite"  # Will be set during init_db()


# ══════════════════════════════════════════════════════════════
#  POSTGRESQL HELPERS
# ══════════════════════════════════════════════════════════════

def get_postgres_connection():
    """
    Returns a psycopg2 connection using DATABASE_URL.
    psycopg2 uses %s placeholders (same as our query_db/execute_db helpers).
    """
    import psycopg2
    import psycopg2.extras
    conn = psycopg2.connect(Config.DATABASE_URL)
    return conn


def init_postgres():
    """
    Initializes PostgreSQL tables on Render (CREATE TABLE IF NOT EXISTS).
    Returns True if successful, False otherwise.
    """
    try:
        import psycopg2
        conn = get_postgres_connection()
        cur = conn.cursor()

        # 1. users table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            full_name VARCHAR(100) NOT NULL,
            mobile_number VARCHAR(15) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            village VARCHAR(100) NOT NULL,
            business_type VARCHAR(100) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # 2. admin_users table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS admin_users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            full_name VARCHAR(100) NOT NULL,
            email VARCHAR(100),
            role VARCHAR(30) DEFAULT 'admin',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # 3. schemes table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS schemes (
            id SERIAL PRIMARY KEY,
            scheme_name VARCHAR(200) NOT NULL,
            scheme_code VARCHAR(50) UNIQUE,
            category VARCHAR(100) NOT NULL,
            description_en TEXT NOT NULL,
            description_hi TEXT,
            description_mr TEXT,
            eligible_business_types TEXT NOT NULL,
            state_applicability VARCHAR(100) NOT NULL DEFAULT 'All India',
            max_annual_income REAL NOT NULL DEFAULT 0.0,
            min_loan_amount REAL NOT NULL DEFAULT 10000.0,
            max_loan_amount REAL NOT NULL DEFAULT 1000000.0,
            subsidy_percentage REAL DEFAULT 0.0,
            required_documents TEXT NOT NULL,
            how_to_apply TEXT NOT NULL,
            official_portal TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # 4. financial_content table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS financial_content (
            id SERIAL PRIMARY KEY,
            category_slug VARCHAR(100) NOT NULL UNIQUE,
            title_en TEXT NOT NULL,
            title_hi TEXT NOT NULL,
            title_mr TEXT NOT NULL,
            explanation_en TEXT NOT NULL,
            explanation_hi TEXT NOT NULL,
            explanation_mr TEXT NOT NULL,
            example_en TEXT NOT NULL,
            example_hi TEXT NOT NULL,
            example_mr TEXT NOT NULL,
            safety_tips_en TEXT NOT NULL,
            safety_tips_hi TEXT NOT NULL,
            safety_tips_mr TEXT NOT NULL,
            display_order INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # 5. feedback table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id SERIAL PRIMARY KEY,
            user_id INTEGER,
            user_name VARCHAR(100) NOT NULL,
            mobile_number VARCHAR(15) NOT NULL,
            category VARCHAR(100) NOT NULL,
            rating INTEGER NOT NULL,
            message TEXT NOT NULL,
            status VARCHAR(50) DEFAULT 'Reviewed',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
        );
        """)

        # Seed default admin if not exists
        cur.execute("SELECT COUNT(*) FROM admin_users;")
        if cur.fetchone()[0] == 0:
            from werkzeug.security import generate_password_hash
            admin_hash = generate_password_hash('admin123')
            cur.execute("""
                INSERT INTO admin_users (username, password_hash, full_name, email, role)
                VALUES (%s, %s, %s, %s, %s)
            """, ('admin', admin_hash, 'FinSakhi Lead Administrator', 'admin@finsakhi.gov.in', 'admin'))

        # Seed schemes if not exists
        cur.execute("SELECT COUNT(*) FROM schemes;")
        if cur.fetchone()[0] == 0:
            _seed_postgres_schemes(cur)

        # Seed financial_content if not exists
        cur.execute("SELECT COUNT(*) FROM financial_content;")
        if cur.fetchone()[0] == 0:
            _seed_postgres_financial_content(cur)

        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"[FinSakhi DB Warning] PostgreSQL init note: {e}")
        return False


def _seed_postgres_schemes(cur):
    """Seeds government schemes into PostgreSQL."""
    schemes = [
        ("PM SVANidhi", "PMSVN001", "Street Vendor Loan",
         "Provides collateral-free working capital loans up to Rs.50,000 for street vendors.",
         "स्ट्रीट वेंडर्स को 50,000 रुपये तक का कार्यशील पूंजी ऋण।",
         "रस्त्यावरील विक्रेत्यांना 50,000 रुपयांपर्यंत कर्ज.",
         "Street Vendor,Small Trade", "All India", 500000, 10000, 50000, 0.0,
         "Aadhar Card, Vendor Certificate, Bank Account",
         "Apply via PM SVANidhi portal or nearest bank.",
         "https://pmsvanidhi.mohua.gov.in"),
        ("Mudra Yojana - Shishu", "MUDRA001", "Micro Business Loan",
         "PMMY Shishu category offers loans up to Rs.50,000 for new micro businesses.",
         "नए सूक्ष्म उद्यमों के लिए 50,000 रु. तक का ऋण।",
         "नवीन सूक्ष्म उद्योगांसाठी 50,000 रुपयांपर्यंत कर्ज.",
         "Dairy,Kirana,Handicraft,Tailoring", "All India", 300000, 10000, 50000, 0.0,
         "Aadhar, PAN, Business Proof, Bank Statement",
         "Visit nearest PSU Bank or MFI and fill Mudra loan form.",
         "https://www.mudra.org.in"),
        ("Mudra Yojana - Kishor", "MUDRA002", "Small Business Loan",
         "PMMY Kishor offers loans from Rs.50,001 to Rs.5 lakh for expanding businesses.",
         "विस्तार के लिए 5 लाख तक का ऋण।",
         "व्यवसाय विस्तारासाठी 5 लाखांपर्यंत कर्ज.",
         "Dairy,Kirana,Handicraft,Tailoring,Poultry,Vegetable", "All India", 1500000, 50001, 500000, 0.0,
         "Aadhar, PAN, 2 Year ITR, Business Proof",
         "Visit bank with 2 year business proof and apply.",
         "https://www.mudra.org.in"),
        ("NRLM - SHG Loan", "NRLM001", "Women Self Help Group",
         "National Rural Livelihood Mission provides credit linkage to SHGs at subsidized rates.",
         "महिला स्वयं सहायता समूहों को रियायती दर पर ऋण.",
         "महिला बचत गटांना अनुदानित दराने कर्ज.",
         "All Rural Business", "All India", 0, 25000, 300000, 3.0,
         "SHG Registration, Bank Passbook, Aadhar",
         "Join a SHG registered under NRLM and apply through bank.",
         "https://aajeevika.gov.in"),
        ("PMFME Scheme", "PMFME001", "Food Processing",
         "PM Formalisation of Micro Food Processing Enterprises - 35% credit linked subsidy.",
         "खाद्य प्रसंस्करण उद्यमों के लिए 35% सब्सिडी.",
         "अन्न प्रक्रिया उद्योगांसाठी 35% अनुदान.",
         "Food Processing,Dairy,Agro", "All India", 0, 100000, 1000000, 35.0,
         "Udyam Registration, Aadhar, PAN, Bank Statement",
         "Apply via MoFPI portal or state nodal agency.",
         "https://pmfme.mofpi.gov.in"),
        ("Stand Up India", "STANDUP01", "SC/ST Women Entrepreneur Loan",
         "Bank loans between Rs.10 lakh and Rs.1 crore for SC/ST and women entrepreneurs.",
         "अनुसूचित जाति/जनजाति व महिला उद्यमियों के लिए 10 लाख से 1 करोड़ तक ऋण.",
         "SC/ST आणि महिला उद्योजकांसाठी 10 लाख ते 1 कोटी कर्ज.",
         "Manufacturing,Service,Trade", "All India", 0, 1000000, 10000000, 0.0,
         "Aadhar, PAN, Business Plan, SC/ST Certificate if applicable",
         "Apply via Stand Up India portal or nearest Scheduled Commercial Bank.",
         "https://www.standupmitra.in"),
        ("CGTMSE Scheme", "CGTMSE01", "Collateral-Free Loan",
         "Credit Guarantee Scheme for MSMEs - collateral-free loans up to Rs.2 crore.",
         "एमएसएमई के लिए 2 करोड़ तक बिना गारंटी ऋण.",
         "MSMEs साठी 2 कोटींपर्यंत विनातारण कर्ज.",
         "Manufacturing,Service,Small Business", "All India", 0, 100000, 20000000, 0.0,
         "Udyam Registration, Bank Statement, Business Plan",
         "Apply via CGTMSE portal or partner bank.",
         "https://www.cgtmse.in"),
    ]
    for s in schemes:
        cur.execute("""
            INSERT INTO schemes (scheme_name, scheme_code, category,
                description_en, description_hi, description_mr,
                eligible_business_types, state_applicability,
                max_annual_income, min_loan_amount, max_loan_amount, subsidy_percentage,
                required_documents, how_to_apply, official_portal)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (scheme_code) DO NOTHING;
        """, s)


def _seed_postgres_financial_content(cur):
    """Seeds financial literacy content into PostgreSQL."""
    content = [
        ("savings", "Savings & Deposit Accounts", "बचत और जमा खाते", "बचत आणि ठेव खाते",
         "A savings account is a basic bank account that keeps your money safe and earns interest.",
         "बचत खाता आपका पैसा सुरक्षित रखता है और ब्याज देता है।",
         "बचत खाते आपले पैसे सुरक्षित ठेवते आणि व्याज देते.",
         "If you save Rs.500/month at 4% annual interest, in 5 years you'll have approx Rs.33,000.",
         "यदि आप 4% ब्याज पर 500 रु/माह बचाते हैं, 5 साल में ₹33,000 होंगे।",
         "जर तुम्ही 500 रु./महिना 4% व्याजाने बचत केली, 5 वर्षात ₹33,000 होतील.",
         "Use Jan Dhan account. Keep emergency fund. Don't keep cash at home.",
         "जन धन खाता उपयोग करें। आपातकालीन निधि रखें।",
         "जन धन खाते वापरा. आपत्कालीन निधी ठेवा.", 1),
        ("loans", "Loans & Credit", "ऋण और क्रेडिट", "कर्ज आणि क्रेडिट",
         "A loan is borrowed money that must be repaid with interest over a fixed period.",
         "ऋण वह पैसा है जो निश्चित अवधि में ब्याज सहित वापस करना होता है।",
         "कर्ज म्हणजे ठराविक कालावधीत व्याजासह परत करावयाचे उधार पैसे.",
         "If you borrow Rs.1 lakh at 10% per year for 3 years, you pay about Rs.3,226/month.",
         "1 लाख 10% ब्याज 3 साल के लिए = ~₹3,226/माह EMI.",
         "1 लाख 10% व्याजाने 3 वर्षांसाठी = ~₹3,226/महिना EMI.",
         "Borrow only what you need. Always compare interest rates. Never skip EMI.",
         "केवल जरूरत का पैसा उधार लें। ब्याज दरें compare करें।",
         "फक्त गरजेपुरतेच कर्ज घ्या. व्याज दर तुलना करा.", 2),
        ("insurance", "Insurance & Risk Cover", "बीमा और जोखिम", "विमा आणि जोखीम",
         "Insurance protects you from sudden financial losses due to accidents, illness, or natural disasters.",
         "बीमा आपको दुर्घटना, बीमारी या आपदा से आर्थिक नुकसान से बचाता है।",
         "विमा अपघात, आजारपण किंवा नैसर्गिक आपत्तीतील आर्थिक नुकसानापासून संरक्षण करतो.",
         "PM Jeevan Jyoti Bima Yojana: Rs.2 lakh life cover at just Rs.436/year.",
         "PMJJBY: मात्र ₹436/वर्ष में ₹2 लाख का जीवन बीमा.",
         "PMJJBY: फक्त ₹436/वर्षात ₹2 लाखांचे आयुर्विमा संरक्षण.",
         "Always buy PM Suraksha Bima (₹20/year). Keep policy documents safe.",
         "PM सुरक्षा बीमा (₹20/वर्ष) जरूर लें। पॉलिसी दस्तावेज सुरक्षित रखें।",
         "PM सुरक्षा विमा (₹20/वर्ष) नक्की घ्या. पॉलिसी कागदपत्रे सुरक्षित ठेवा.", 3),
        ("upi-banking", "Digital Payments & UPI", "डिजिटल भुगतान और UPI", "डिजिटल पेमेंट आणि UPI",
         "UPI (Unified Payments Interface) lets you send and receive money instantly using your mobile phone.",
         "UPI से आप मोबाइल से तुरंत पैसे भेज और प्राप्त कर सकते हैं।",
         "UPI द्वारे तुम्ही मोबाइलवरून तत्काळ पैसे पाठवू आणि प्राप्त करू शकता.",
         "Open PhonePe/GPay → Link bank account → Enter UPI PIN → Send Rs.500 to vendor instantly.",
         "PhonePe/GPay खोलें → बैंक खाता लिंक करें → UPI PIN डालें → तुरंत पैसे भेजें।",
         "PhonePe/GPay उघडा → बँक खाते लिंक करा → UPI PIN टाका → लगेच पैसे पाठवा.",
         "Never share OTP or UPI PIN. Use only official apps. Verify QR code before paying.",
         "कभी OTP या UPI PIN share न करें। केवल आधिकारिक ऐप्स उपयोग करें।",
         "OTP किंवा UPI PIN कधीही शेअर करू नका. अधिकृत ऍप्स वापरा.", 4),
        ("fraud-awareness", "Financial Fraud Awareness", "वित्तीय धोखाधड़ी", "आर्थिक फसवणूक जागरूकता",
         "Financial frauds target rural users through fake calls, fake schemes, and phishing links.",
         "वित्तीय धोखाधड़ी नकली कॉल, नकली योजनाओं और फ़िशिंग लिंक द्वारा होती है।",
         "आर्थिक फसवणूक खोट्या कॉल, खोट्या योजना आणि फिशिंग लिंकद्वारे होते.",
         "Red Flag: 'You won Rs.10 lakh! Share your OTP to claim.' — This is FRAUD. Hang up.",
         "लाल झंडा: 'आपने 10 लाख जीते! OTP share करें' — यह धोखाधड़ी है। फोन काटें।",
         "धोक्याची घंटा: '10 लाख जिंकलेत! OTP द्या' — हे फसवणूक आहे. फोन ठेवा.",
         "Never share OTP/PIN. Never click unknown links. Report fraud: 1930 (Cyber Helpline).",
         "OTP/PIN कभी share न करें। अनजान लिंक click न करें। साइबर हेल्पलाइन: 1930।",
         "OTP/PIN कधीही शेअर करू नका. सायबर हेल्पलाइन: 1930.", 5),
        ("govt-schemes", "Government Financial Schemes", "सरकारी वित्तीय योजनाएं", "सरकारी आर्थिक योजना",
         "Government schemes provide financial support, subsidies, and loans to rural entrepreneurs at low interest rates.",
         "सरकारी योजनाएं ग्रामीण उद्यमियों को कम ब्याज पर ऋण और सब्सिडी देती हैं।",
         "सरकारी योजना ग्रामीण उद्योजकांना कमी व्याजाने कर्ज आणि अनुदान देतात.",
         "A dairy farmer in Maharashtra applied for PMFME with 35% subsidy → got Rs.3.5 lakh on Rs.10 lakh project.",
         "महाराष्ट्र के एक डेयरी किसान ने PMFME से 35% सब्सिडी पर 3.5 लाख पाए।",
         "महाराष्ट्रातील एका दुग्धपालक शेतकऱ्याने PMFME मधून 35% अनुदानावर ₹3.5 लाख मिळवले.",
         "Check eligibility before applying. Use official portals only. Beware of agents charging fees.",
         "आवेदन से पहले पात्रता जांचें। केवल आधिकारिक पोर्टल उपयोग करें।",
         "अर्ज करण्यापूर्वी पात्रता तपासा. अधिकृत पोर्टल वापरा.", 6),
    ]
    for c in content:
        cur.execute("""
            INSERT INTO financial_content (
                category_slug, title_en, title_hi, title_mr,
                explanation_en, explanation_hi, explanation_mr,
                example_en, example_hi, example_mr,
                safety_tips_en, safety_tips_hi, safety_tips_mr, display_order)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (category_slug) DO NOTHING;
        """, c)


# ══════════════════════════════════════════════════════════════
#  MYSQL HELPERS
# ══════════════════════════════════════════════════════════════

def get_mysql_connection():
    """
    Attempts to establish a connection to the MySQL Server.
    Uses credentials defined in Config.
    """
    import pymysql
    import pymysql.cursors
    return pymysql.connect(
        host=Config.MYSQL_HOST,
        port=Config.MYSQL_PORT,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False
    )


def init_mysql_if_possible():
    """
    Tries to connect to MySQL and execute the finsakhi_db.sql schema.
    Returns True if successful, False otherwise.
    """
    try:
        import pymysql
        conn = pymysql.connect(
            host=Config.MYSQL_HOST,
            port=Config.MYSQL_PORT,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            charset='utf8mb4'
        )
        with conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.MYSQL_DB} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        conn.close()

        db_conn = get_mysql_connection()
        sql_path = os.path.join(os.path.dirname(__file__), 'database', 'finsakhi_db.sql')
        if os.path.exists(sql_path):
            with open(sql_path, 'r', encoding='utf-8') as f:
                sql_script = f.read()
            commands = [cmd.strip() for cmd in sql_script.split(';') if cmd.strip()]
            with db_conn.cursor() as cursor:
                for cmd in commands:
                    if cmd.upper().startswith('CREATE DATABASE') or cmd.upper().startswith('USE'):
                        continue
                    cursor.execute(cmd)
            db_conn.commit()
        db_conn.close()
        return True
    except Exception as e:
        print(f"[FinSakhi DB Warning] MySQL Connection/Init Note: {e}")
        return False


# ══════════════════════════════════════════════════════════════
#  SQLITE FALLBACK HELPERS
# ══════════════════════════════════════════════════════════════

def init_sqlite_fallback():
    """
    Initializes a local SQLite database matching the schema.
    Allows zero-dependency offline running during local development.
    """
    conn = sqlite3.connect(Config.SQLITE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        mobile_number TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        village TEXT NOT NULL,
        business_type TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        full_name TEXT NOT NULL,
        email TEXT,
        role TEXT DEFAULT 'admin',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS schemes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        scheme_name TEXT NOT NULL,
        scheme_code TEXT UNIQUE,
        category TEXT NOT NULL,
        description_en TEXT NOT NULL,
        description_hi TEXT,
        description_mr TEXT,
        eligible_business_types TEXT NOT NULL,
        state_applicability TEXT NOT NULL DEFAULT 'All India',
        max_annual_income REAL NOT NULL DEFAULT 0.0,
        min_loan_amount REAL NOT NULL DEFAULT 10000.0,
        max_loan_amount REAL NOT NULL DEFAULT 1000000.0,
        subsidy_percentage REAL DEFAULT 0.0,
        required_documents TEXT NOT NULL,
        how_to_apply TEXT NOT NULL,
        official_portal TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS financial_content (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_slug TEXT NOT NULL UNIQUE,
        title_en TEXT NOT NULL,
        title_hi TEXT NOT NULL,
        title_mr TEXT NOT NULL,
        explanation_en TEXT NOT NULL,
        explanation_hi TEXT NOT NULL,
        explanation_mr TEXT NOT NULL,
        example_en TEXT NOT NULL,
        example_hi TEXT NOT NULL,
        example_mr TEXT NOT NULL,
        safety_tips_en TEXT NOT NULL,
        safety_tips_hi TEXT NOT NULL,
        safety_tips_mr TEXT NOT NULL,
        display_order INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        user_name TEXT NOT NULL,
        mobile_number TEXT NOT NULL,
        category TEXT NOT NULL,
        rating INTEGER NOT NULL,
        message TEXT NOT NULL,
        status TEXT DEFAULT 'Reviewed',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
    );
    """)

    cursor.execute("SELECT COUNT(*) FROM schemes")
    if cursor.fetchone()[0] == 0:
        from database.seed_data import seed_fallback_data
        seed_fallback_data(conn)

    conn.commit()
    conn.close()


# ══════════════════════════════════════════════════════════════
#  MAIN INIT — Chooses the best available backend
# ══════════════════════════════════════════════════════════════

def init_db():
    """
    Determines and initializes the active database backend.
    Priority: PostgreSQL (DATABASE_URL) > MySQL > SQLite
    """
    global ACTIVE_DB_BACKEND

    # 1. Try PostgreSQL first (Render cloud deployment)
    if Config.DATABASE_URL:
        pg_ok = init_postgres()
        if pg_ok:
            ACTIVE_DB_BACKEND = "postgres"
            print("[FinSakhi DB] ✅ Connected to PostgreSQL database (Render Cloud).")
            return

    # 2. Try MySQL
    mysql_ok = init_mysql_if_possible()
    if mysql_ok:
        ACTIVE_DB_BACKEND = "mysql"
        print("[FinSakhi DB] ✅ Connected successfully to MySQL database 'finsakhi_db'.")
        return

    # 3. Fall back to SQLite (local development)
    ACTIVE_DB_BACKEND = "sqlite"
    init_sqlite_fallback()
    print("[FinSakhi DB] ⚠️  Running with local fallback database (SQLite).")
    print("[FinSakhi DB Tip] Set DATABASE_URL on Render for persistent cloud storage.")


# ══════════════════════════════════════════════════════════════
#  CONNECTION FACTORY
# ══════════════════════════════════════════════════════════════

def get_connection():
    """Returns an active database connection based on the active backend."""
    global ACTIVE_DB_BACKEND

    if ACTIVE_DB_BACKEND == "postgres":
        return get_postgres_connection()

    elif ACTIVE_DB_BACKEND == "mysql":
        try:
            return get_mysql_connection()
        except Exception:
            # If MySQL drops mid-run, fallback to sqlite
            conn = sqlite3.connect(Config.SQLITE_PATH)
            conn.row_factory = sqlite3.Row
            return conn

    else:
        conn = sqlite3.connect(Config.SQLITE_PATH)
        conn.row_factory = sqlite3.Row
        return conn


# ══════════════════════════════════════════════════════════════
#  QUERY HELPERS
# ══════════════════════════════════════════════════════════════

def query_db(query, args=(), one=False):
    """
    Executes a SELECT SQL query with parameterized values (prevents SQL Injection).
    Returns list of dicts or single dict.
    Uses %s placeholders for MySQL/PostgreSQL and auto-converts to ? for SQLite.
    """
    global ACTIVE_DB_BACKEND
    conn = get_connection()
    try:
        if isinstance(conn, sqlite3.Connection):
            sqlite_query = query.replace('%s', '?')
            cursor = conn.cursor()
            cursor.execute(sqlite_query, args)
            rows = cursor.fetchall()
            result = [dict(row) for row in rows]
            cursor.close()
        else:
            import psycopg2.extras
            if ACTIVE_DB_BACKEND == "postgres":
                cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                cur.execute(query, args)
                rows = cur.fetchall()
                result = [dict(row) for row in rows]
                cur.close()
            else:
                # MySQL (pymysql DictCursor already configured)
                with conn.cursor() as cursor:
                    cursor.execute(query, args)
                    result = cursor.fetchall()
        return (result[0] if result else None) if one else result
    finally:
        conn.close()


def execute_db(query, args=(), get_last_id=False):
    """
    Executes an INSERT, UPDATE, or DELETE query with parameterized values.
    Returns last inserted ID if requested, otherwise affected rows count.
    """
    global ACTIVE_DB_BACKEND
    conn = get_connection()
    try:
        last_id = None
        row_count = 0

        if isinstance(conn, sqlite3.Connection):
            sqlite_query = query.replace('%s', '?')
            cursor = conn.cursor()
            cursor.execute(sqlite_query, args)
            conn.commit()
            last_id = cursor.lastrowid
            row_count = cursor.rowcount
            cursor.close()

        elif ACTIVE_DB_BACKEND == "postgres":
            # For PostgreSQL, use RETURNING id to get last inserted id
            if get_last_id and 'INSERT' in query.upper() and 'RETURNING' not in query.upper():
                query = query.rstrip().rstrip(';') + ' RETURNING id;'
            cur = conn.cursor()
            cur.execute(query, args)
            conn.commit()
            if get_last_id and 'RETURNING' in query.upper():
                row = cur.fetchone()
                last_id = row[0] if row else None
            else:
                row_count = cur.rowcount
            cur.close()

        else:
            # MySQL
            with conn.cursor() as cursor:
                cursor.execute(query, args)
                conn.commit()
                last_id = cursor.lastrowid
                row_count = cursor.rowcount

        return last_id if get_last_id else row_count

    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

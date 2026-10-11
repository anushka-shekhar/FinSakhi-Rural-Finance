"""
FinSakhi - Database Connection & Abstraction Layer
Subject Mapping: DBMS & SQL (Relational Databases, Parameterized Queries, ACID Transactions)

This module handles:
1. Connection to MySQL Server (Target: MySQL 8.0 `finsakhi_db`).
2. Parameterized SQL queries to prevent SQL Injection (DBMS Security).
3. Safe execution of CRUD operations (Create, Read, Update, Delete).
4. Automatic fallback to local SQLite database if MySQL credentials are not yet entered,
   ensuring the application is immediately testable while preserving full MySQL compatibility.
"""

import os
import pymysql
import pymysql.cursors
import sqlite3
from config import Config

# Global variable to track active database backend
ACTIVE_DB_BACKEND = "mysql"

def get_mysql_connection():
    """
    Attempts to establish a connection to the MySQL Server.
    Uses credentials defined in Config.
    """
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
        # First connect without database to ensure database exists
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

        # Now connect to finsakhi_db
        db_conn = get_mysql_connection()
        sql_path = os.path.join(os.path.dirname(__file__), 'database', 'finsakhi_db.sql')
        if os.path.exists(sql_path):
            with open(sql_path, 'r', encoding='utf-8') as f:
                sql_script = f.read()
            # Split commands by semicolon for execution
            commands = [cmd.strip() for cmd in sql_script.split(';') if cmd.strip()]
            with db_conn.cursor() as cursor:
                for cmd in commands:
                    # Ignore USE and CREATE DATABASE in individual splits
                    if cmd.upper().startswith('CREATE DATABASE') or cmd.upper().startswith('USE'):
                        continue
                    cursor.execute(cmd)
            db_conn.commit()
        db_conn.close()
        return True
    except Exception as e:
        print(f"[FinSakhi DB Warning] MySQL Connection/Init Note: {e}")
        return False

def init_sqlite_fallback():
    """
    Initializes a local SQLite database matching the MySQL schema.
    Allows zero-dependency offline running while students setup MySQL.
    """
    conn = sqlite3.connect(Config.SQLITE_PATH)
    cursor = conn.cursor()
    
    # 1. users table
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

    # 2. admin_users table
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

    # 3. schemes table
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

    # 4. financial_content table
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

    # 5. feedback table
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

    # Seed data if schemes table is empty
    cursor.execute("SELECT COUNT(*) FROM schemes")
    if cursor.fetchone()[0] == 0:
        from database.seed_data import seed_fallback_data
        seed_fallback_data(conn)

    conn.commit()
    conn.close()

def init_db():
    """
    Determines and initializes the active database (MySQL preferred, SQLite fallback).
    """
    global ACTIVE_DB_BACKEND
    mysql_ok = init_mysql_if_possible()
    if mysql_ok:
        ACTIVE_DB_BACKEND = "mysql"
        print("[FinSakhi DB] Connected successfully to MySQL database 'finsakhi_db'.")
    else:
        ACTIVE_DB_BACKEND = "sqlite"
        init_sqlite_fallback()
        print("[FinSakhi DB] Running with local fallback database (SQLite).")
        print("[FinSakhi DB Tip] To connect to MySQL, configure your credentials in '.env' file.")

def get_connection():
    """Returns an active database connection."""
    global ACTIVE_DB_BACKEND
    if ACTIVE_DB_BACKEND == "mysql":
        try:
            return get_mysql_connection()
        except Exception:
            # If MySQL connection fails mid-run, fallback to sqlite
            return sqlite3.connect(Config.SQLITE_PATH)
    else:
        conn = sqlite3.connect(Config.SQLITE_PATH)
        conn.row_factory = sqlite3.Row  # Returns rows as dictionaries
        return conn

def query_db(query, args=(), one=False):
    """
    Executes a SELECT SQL query with parameterized values (prevents SQL Injection).
    Returns list of dicts or single dict.
    """
    global ACTIVE_DB_BACKEND
    conn = get_connection()
    try:
        if isinstance(conn, sqlite3.Connection):
            # Translate %s placeholder to ? for sqlite
            sqlite_query = query.replace('%s', '?')
            cursor = conn.cursor()
            cursor.execute(sqlite_query, args)
            rows = cursor.fetchall()
            result = [dict(row) for row in rows]
            cursor.close()
        else:
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
        else:
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

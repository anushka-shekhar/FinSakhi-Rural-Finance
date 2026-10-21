"""
FinSakhi - Application Configuration
Subject Mapping: Software Engineering & Web Programming
Handles environment configurations, security keys, and database credentials.

Database Priority Order:
  1. PostgreSQL  — if DATABASE_URL env variable is set (Render Cloud / Production)
  2. MySQL       — if MYSQL_HOST is a live server (local MySQL or remote MySQL)
  3. SQLite      — offline fallback for local development without any DB server
"""

import os
from dotenv import load_dotenv

# Load variables from .env file if present
load_dotenv()

class Config:
    # Flask Session Secret Key
    SECRET_KEY = os.environ.get('SECRET_KEY', 'finsakhi-secret-key-rural-fin-2026')

    # ── PostgreSQL (Render Free Postgres / Production) ────────────────────────
    # Set this env variable on Render dashboard for persistent cloud database.
    DATABASE_URL = os.environ.get('DATABASE_URL', None)

    # ── MySQL Database Settings ───────────────────────────────────────────────
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'root')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'finsakhi_db')

    # ── Fallback SQLite path ──────────────────────────────────────────────────
    # Used automatically if neither PostgreSQL nor MySQL is available.
    SQLITE_PATH = os.path.join(os.path.dirname(__file__), 'database', 'finsakhi_local.db')

    # Supported Languages
    LANGUAGES = ['en', 'hi', 'mr']
    DEFAULT_LANGUAGE = 'en'

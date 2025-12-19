import sqlite3
import os

# Resolve the project base directory dynamically to avoid
# hardcoded paths and ensure portability across environments.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DB_PATH = os.path.join(BASE_DIR, "wallets.db")


def get_connection():
    """
    Creates and returns a new SQLite database connection.

    A fresh connection is intentionally created per operation to
    keep database access simple, thread-safe, and predictable for
    a lightweight, single-process application.
    """
    return sqlite3.connect(DB_PATH)


def init_db():
    """
    Initializes the database schema if it does not already exist.

    This function is designed to be idempotent and safe to call
    during application startup without impacting existing data.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Stores tracked wallet addresses.
    # The address is used as the primary key to enforce uniqueness
    # and prevent duplicate registrations at the database level.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wallets (
            address TEXT PRIMARY KEY
        )
    """)

    conn.commit()
    conn.close()


def add_wallet(address: str):
    """
    Persists a wallet address for tracking.

    Duplicate inserts are intentionally ignored to keep the
    operation idempotent and to simplify API behavior when
    clients retry requests.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # INSERT OR IGNORE ensures database-level de-duplication
    # without requiring additional application-side checks.
    cursor.execute(
        "INSERT OR IGNORE INTO wallets (address) VALUES (?)",
        (address,)
    )

    conn.commit()
    conn.close()


def wallet_exists(address: str) -> bool:
    """
    Checks whether a wallet address is already registered.

    This utility method provides a lightweight existence check
    without fetching unnecessary data, enabling efficient
    validation flows in the service layer.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT address FROM wallets WHERE address = ?",
        (address,)
    )

    exists = cursor.fetchone() is not None
    conn.close()
    return exists


def get_all_wallets():
    """
    Retrieves all tracked wallet addresses.

    Returns a flat list of wallet identifiers, intentionally
    omitting additional metadata to keep the read path fast
    and suitable for downstream aggregation or synchronization.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT address FROM wallets")
    rows = cursor.fetchall()

    conn.close()
    return [row[0] for row in rows]

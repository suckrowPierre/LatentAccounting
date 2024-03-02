from pathlib import Path
import sqlite3
import contextlib

# Define the path to the database
DB_PATH = Path("./db/accounts.db")

def ensure_db_directory():
    """Ensure the database directory exists."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)


@contextlib.contextmanager
def get_db_connection():
    """Context manager for SQLite database connections."""
    connection = None
    try:
        connection = sqlite3.connect(str(DB_PATH))
        connection.row_factory = sqlite3.Row  # Enable column access by name
        yield connection
    finally:
        if connection:
            connection.close()

def create_db():
    """Create the database and the necessary tables if they don't exist."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bank_accounts (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                account_number TEXT,
                last_data_update TEXT
            )
        """)
        conn.commit()
        print(f"Database directory created: {DB_PATH}")

def add_account(name, account_number=None):
    """Add a new account to the database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO bank_accounts (name, account_number) VALUES (?, ?)
        """, (name, account_number))
        # Get the ID of the newly inserted row
        account_id = cursor.lastrowid
        conn.commit()
        return account_id

def update_account(account_id, name=None, account_number=None):
    """Update an existing account."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE bank_accounts
            SET name = COALESCE(?, name),
                account_number = COALESCE(?, account_number)
            WHERE id = ?
        """, (name, account_number, account_id))
        conn.commit()
        return True

def delete_account(account_id):
    """Delete an account from the database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM bank_accounts WHERE id = ?", (account_id,))
        conn.commit()
        return True

def get_accounts():
    """Retrieve all accounts from the database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bank_accounts")
        return cursor.fetchall()

# Run the startup event to ensure DB and table creation
def startup_event():
    ensure_db_directory()
    create_db()
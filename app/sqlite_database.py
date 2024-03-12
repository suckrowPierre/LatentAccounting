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
                last_data_update TEXT,
                csv_seperator TEXT,
                csv_columns TEXT,
                csv_file_path TEXT,
                flowchart_diagram TEXT
            )
        """)
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS settings (
                        id INTEGER PRIMARY KEY CHECK (id = 1),
                        currency TEXT,
                        api_key TEXT,
                        gpt_api_model TEXT
                    )
                """)
        conn.commit()
        print(f"Database directory created: {DB_PATH}")

def add_account(name, account_number=None, last_data_update=None, csv_seperator=None, csv_columns=None, csv_file_path=None, flowchart_diagram=None):
    """Add a new account to the database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(""" 
        INSERT INTO bank_accounts (name, account_number, last_data_update, csv_seperator, csv_columns, csv_file_path, flowchart_diagram) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                       (name, account_number, last_data_update, csv_seperator, csv_columns, csv_file_path, flowchart_diagram))
        # Get the ID of the newly inserted row
        account_id = cursor.lastrowid
        conn.commit()
        return account_id

def update_account(account_id, name=None, account_number=None, csv_seperator=None, csv_columns=None, csv_file_path=None, flowchart_diagram=None):
    """Update an existing account."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE bank_accounts
            SET name = COALESCE(?, name),
                account_number = COALESCE(?, account_number),
                csv_seperator = COALESCE(?, csv_seperator),
                csv_columns = COALESCE(?, csv_columns),
                csv_file_path = COALESCE(?, csv_file_path),
                flowchart_diagram = COALESCE(?, flowchart_diagram)
            WHERE id = ?
        """, (name, account_number, csv_seperator, csv_columns, csv_file_path, flowchart_diagram, account_id))
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

def get_account(account_id):
    """Retrieve a single account from the database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bank_accounts WHERE id = ?", (account_id,))
        return cursor.fetchone()

def update_or_insert_settings(currency, api_key, gpt_api_model):
    """Update or insert the single settings entry."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO settings (id, currency, api_key, gpt_api_model)
            VALUES (1, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                currency = excluded.currency,
                api_key = excluded.api_key,
                gpt_api_model = excluded.gpt_api_model
        """, (currency, api_key, gpt_api_model))
        conn.commit()

def get_settings():
    """Retrieve the settings from the database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM settings WHERE id = 1")
        return cursor.fetchone()

# Run the startup event to ensure DB and table creation
def startup_event():
    ensure_db_directory()
    create_db()
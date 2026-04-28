# setup_db.py
# Run this one time to create the database and all three tables.
# Usage: python setup_db.py
 
import mysql.connector
from config import DB_CONFIG, DB_NAME
 
 
def get_raw_connection():
    # Connect without picking a database so we can create one
    return mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
    )
 
 
def create_database():
    conn   = get_raw_connection()
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    print(f"Database '{DB_NAME}' is ready.")
    cursor.close()
    conn.close()
 
 
def create_tables():
    conn   = get_raw_connection()
    cursor = conn.cursor()
    cursor.execute(f"USE {DB_NAME}")
 
    # users table stores login info for each person
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id       INT          AUTO_INCREMENT PRIMARY KEY,
            username      VARCHAR(60)  NOT NULL UNIQUE,
            password_hash VARCHAR(64)  NOT NULL,
            salt          VARCHAR(32)  NOT NULL,
            full_name     VARCHAR(100) NOT NULL,
            created_at    DATETIME     DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("Table 'users' is ready.")
 
    # accounts table stores each bank account
    # user_id links the account back to whoever created it
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            account_id  INT           AUTO_INCREMENT PRIMARY KEY,
            user_id     INT           NOT NULL,
            owner_name  VARCHAR(100)  NOT NULL,
            balance     DECIMAL(15,2) NOT NULL DEFAULT 0.00,
            created_at  DATETIME      DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT chk_balance CHECK (balance >= 0),
            CONSTRAINT fk_user
                FOREIGN KEY (user_id) REFERENCES users (user_id)
                ON DELETE CASCADE
        )
    """)
    print("Table 'accounts' is ready.")
 
    # transactions table logs every deposit, withdrawal, and transfer
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INT           AUTO_INCREMENT PRIMARY KEY,
            account_id     INT           NOT NULL,
            type           VARCHAR(20)   NOT NULL,
            amount         DECIMAL(15,2) NOT NULL,
            note           VARCHAR(255)  DEFAULT NULL,
            created_at     DATETIME      DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_account
                FOREIGN KEY (account_id) REFERENCES accounts (account_id)
                ON DELETE CASCADE
        )
    """)
    print("Table 'transactions' is ready.")
 
    conn.commit()
    cursor.close()
    conn.close()
 
 
if __name__ == "__main__":
    print("\nSetting up the database...\n")
    create_database()
    create_tables()
    print("\nDone! Now run: python app.py\n")
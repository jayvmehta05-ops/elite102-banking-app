# banking.py
# All the banking operations live here.
# The UI just calls these functions and shows whatever they return.
 
from db import get_connection
 
 
def _log_transaction(cursor, account_id, tx_type, amount, note=None):
    # Save one transaction record to the database
    cursor.execute(
        "INSERT INTO transactions (account_id, type, amount, note) VALUES (%s, %s, %s, %s)",
        (account_id, tx_type, amount, note)
    )
 
 
def create_account(owner_name, initial_deposit, user_id):
    # Make sure the inputs are valid
    owner_name = owner_name.strip()
    if not owner_name:
        raise ValueError("Account name cannot be blank.")
    if initial_deposit < 0:
        raise ValueError("Initial deposit cannot be negative.")
 
    conn   = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO accounts (owner_name, balance, user_id) VALUES (%s, %s, %s)",
            (owner_name, initial_deposit, user_id)
        )
        new_id = cursor.lastrowid
 
        # Log the opening deposit if there was one
        if initial_deposit > 0:
            _log_transaction(cursor, new_id, "deposit", initial_deposit, "Opening deposit")
 
        conn.commit()
        return new_id
    finally:
        cursor.close()
        conn.close()
 
 
def get_account(account_id):
    # Get one account by its ID, returns None if it doesn't exist
    conn   = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM accounts WHERE account_id = %s", (account_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()
 
 
def list_accounts(user_id=None):
    # Get all accounts, or just the ones belonging to one user
    conn   = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        if user_id is not None:
            cursor.execute(
                "SELECT * FROM accounts WHERE user_id = %s ORDER BY account_id",
                (user_id,)
            )
        else:
            cursor.execute("SELECT * FROM accounts ORDER BY account_id")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
 
 
def delete_account(account_id):
    # You can only close an account if the balance is zero
    account = get_account(account_id)
    if account is None:
        return False
    if float(account["balance"]) != 0:
        raise ValueError(
            f"Cannot close account #{account_id}. "
            f"Balance is ${account['balance']:.2f}. Withdraw all funds first."
        )
 
    conn   = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM accounts WHERE account_id = %s", (account_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        cursor.close()
        conn.close()
 
 
def check_balance(account_id):
    # Get just the balance number for an account
    account = get_account(account_id)
    if account is None:
        raise ValueError(f"Account #{account_id} not found.")
    return float(account["balance"])
 
 
def deposit(account_id, amount):
    if amount <= 0:
        raise ValueError("Deposit amount must be greater than zero.")
 
    if get_account(account_id) is None:
        raise ValueError(f"Account #{account_id} not found.")
 
    conn   = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE accounts SET balance = balance + %s WHERE account_id = %s",
            (amount, account_id)
        )
        _log_transaction(cursor, account_id, "deposit", amount)
        conn.commit()
        return check_balance(account_id)
    finally:
        cursor.close()
        conn.close()
 
 
def withdraw(account_id, amount):
    if amount <= 0:
        raise ValueError("Withdrawal amount must be greater than zero.")
 
    account = get_account(account_id)
    if account is None:
        raise ValueError(f"Account #{account_id} not found.")
 
    # Make sure they have enough money
    current = float(account["balance"])
    if amount > current:
        raise ValueError(
            f"Not enough funds. Balance: ${current:.2f}, Requested: ${amount:.2f}"
        )
 
    conn   = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE accounts SET balance = balance - %s WHERE account_id = %s",
            (amount, account_id)
        )
        _log_transaction(cursor, account_id, "withdrawal", amount)
        conn.commit()
        return check_balance(account_id)
    finally:
        cursor.close()
        conn.close()
 
 
def transfer(from_id, to_id, amount):
    # Move money from one account to another at the same time
    # If anything goes wrong, neither account gets changed
    if from_id == to_id:
        raise ValueError("You cannot transfer to the same account.")
    if amount <= 0:
        raise ValueError("Transfer amount must be greater than zero.")
 
    from_acct = get_account(from_id)
    to_acct   = get_account(to_id)
 
    if from_acct is None:
        raise ValueError(f"Account #{from_id} not found.")
    if to_acct is None:
        raise ValueError(f"Account #{to_id} not found.")
 
    if float(from_acct["balance"]) < amount:
        raise ValueError(
            f"Not enough funds in account #{from_id}. "
            f"Balance: ${float(from_acct['balance']):.2f}"
        )
 
    conn   = get_connection()
    cursor = conn.cursor()
    try:
        # Take money out of the sender
        cursor.execute(
            "UPDATE accounts SET balance = balance - %s WHERE account_id = %s",
            (amount, from_id)
        )
        _log_transaction(cursor, from_id, "transfer", amount, f"Transfer to account #{to_id}")
 
        # Put money into the receiver
        cursor.execute(
            "UPDATE accounts SET balance = balance + %s WHERE account_id = %s",
            (amount, to_id)
        )
        _log_transaction(cursor, to_id, "transfer", amount, f"Transfer from account #{from_id}")
 
        conn.commit()
        return check_balance(from_id), check_balance(to_id)
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()
 
 
def get_transaction_history(account_id):
    # Get all transactions for an account, newest ones first
    if get_account(account_id) is None:
        raise ValueError(f"Account #{account_id} not found.")
 
    conn   = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT * FROM transactions WHERE account_id = %s ORDER BY created_at DESC",
            (account_id,)
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
 
 
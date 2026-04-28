# main.py
# The terminal version of the banking app.
# Use this if you don't want to run the web interface.
# Usage: python main.py
 
import os
import sys
from banking import (
    create_account, deposit, withdraw, check_balance,
    list_accounts, get_account, delete_account,
    transfer, get_transaction_history,
)
 
 
def clear():
    os.system("cls" if os.name == "nt" else "clear")
 
 
def line(char="=", width=50):
    print(char * width)
 
 
def pause():
    print()
    input("  Press Enter to continue...")
 
 
def ask_amount(label):
    while True:
        raw = input(f"  {label}: $").strip()
        try:
            val = float(raw)
            if val <= 0:
                print("  Amount must be greater than zero.")
            else:
                return round(val, 2)
        except ValueError:
            print("  Please enter a number like 100 or 49.99")
 
 
def ask_id(label="Account ID"):
    while True:
        raw = input(f"  {label}: ").strip()
        try:
            return int(raw)
        except ValueError:
            print("  Please enter a whole number.")
 
 
def show_header(title):
    clear()
    line()
    print(f"  Vault Banking  |  {title}")
    line()
    print()
 
 
def screen_create():
    show_header("Open New Account")
    name = input("  Account label: ").strip()
    if not name:
        print("  Name cannot be blank.")
        pause()
        return
    raw = input("  Opening deposit (Enter for $0): $").strip()
    initial = float(raw) if raw else 0.0
    try:
        acct_id = create_account(name, initial, user_id=1)
        print(f"\n  Account #{acct_id} opened for '{name}'")
        print(f"  Opening balance: ${initial:,.2f}")
    except ValueError as e:
        print(f"\n  Error: {e}")
    pause()
 
 
def screen_deposit():
    show_header("Deposit")
    acct_id = ask_id()
    acct    = get_account(acct_id)
    if acct is None:
        print(f"\n  Account #{acct_id} not found.")
        pause()
        return
    print(f"\n  {acct['owner_name']}  |  Current balance: ${float(acct['balance']):,.2f}\n")
    amount = ask_amount("Deposit amount")
    try:
        new_bal = deposit(acct_id, amount)
        print(f"\n  Deposited ${amount:,.2f}  |  New balance: ${new_bal:,.2f}")
    except ValueError as e:
        print(f"\n  Error: {e}")
    pause()
 
 
def screen_withdraw():
    show_header("Withdraw")
    acct_id = ask_id()
    acct    = get_account(acct_id)
    if acct is None:
        print(f"\n  Account #{acct_id} not found.")
        pause()
        return
    print(f"\n  {acct['owner_name']}  |  Current balance: ${float(acct['balance']):,.2f}\n")
    amount = ask_amount("Withdrawal amount")
    try:
        new_bal = withdraw(acct_id, amount)
        print(f"\n  Withdrew ${amount:,.2f}  |  New balance: ${new_bal:,.2f}")
    except ValueError as e:
        print(f"\n  Error: {e}")
    pause()
 
 
def screen_balance():
    show_header("Check Balance")
    acct_id = ask_id()
    acct    = get_account(acct_id)
    if acct is None:
        print(f"\n  Account #{acct_id} not found.")
        pause()
        return
    print(f"\n  Account #{acct['account_id']}  |  {acct['owner_name']}")
    print(f"  Balance: ${float(acct['balance']):,.2f}")
    print(f"  Opened:  {acct['created_at'].strftime('%B %d, %Y')}")
    pause()
 
 
def screen_list():
    show_header("All Accounts")
    accounts = list_accounts()
    if not accounts:
        print("  No accounts found.")
    else:
        line("-")
        for a in accounts:
            print(f"  [{a['account_id']:>4}]  {a['owner_name']:<25}  ${float(a['balance']):>12,.2f}")
        line("-")
        print(f"\n  Total: {len(accounts)} accounts")
    pause()
 
 
def screen_transfer():
    show_header("Transfer")
    from_id = ask_id("From Account ID")
    to_id   = ask_id("To Account ID")
    fa      = get_account(from_id)
    ta      = get_account(to_id)
    if fa is None or ta is None:
        print("\n  One of the accounts was not found.")
        pause()
        return
    print(f"\n  From: #{from_id} {fa['owner_name']}  (${float(fa['balance']):,.2f})")
    print(f"  To:   #{to_id} {ta['owner_name']}\n")
    amount  = ask_amount("Transfer amount")
    confirm = input(f"\n  Confirm transfer of ${amount:,.2f}? (yes/no): ").strip().lower()
    if confirm not in ("yes", "y"):
        print("  Transfer cancelled.")
        pause()
        return
    try:
        nf, nt = transfer(from_id, to_id, amount)
        print(f"\n  Done! #{from_id} new balance: ${nf:,.2f}  |  #{to_id} new balance: ${nt:,.2f}")
    except ValueError as e:
        print(f"\n  Error: {e}")
    pause()
 
 
def screen_history():
    show_header("Transaction History")
    acct_id = ask_id()
    acct    = get_account(acct_id)
    if acct is None:
        print(f"\n  Account #{acct_id} not found.")
        pause()
        return
    print(f"\n  #{acct_id}  {acct['owner_name']}  |  Balance: ${float(acct['balance']):,.2f}\n")
    try:
        history = get_transaction_history(acct_id)
    except ValueError as e:
        print(f"  Error: {e}")
        pause()
        return
    if not history:
        print("  No transactions yet.")
    else:
        line("-")
        for t in history:
            print(
                f"  {t['created_at'].strftime('%Y-%m-%d %H:%M')}  "
                f"{t['type']:<12}  ${float(t['amount']):>10,.2f}  "
                f"{t['note'] or ''}"
            )
        line("-")
    pause()
 
 
def screen_delete():
    show_header("Close Account")
    acct_id = ask_id()
    acct    = get_account(acct_id)
    if acct is None:
        print(f"\n  Account #{acct_id} not found.")
        pause()
        return
    print(f"\n  Account #{acct_id}  |  {acct['owner_name']}  |  Balance: ${float(acct['balance']):,.2f}")
    confirm = input("\n  Type DELETE to confirm: ").strip()
    if confirm != "DELETE":
        print("  Cancelled.")
        pause()
        return
    try:
        delete_account(acct_id)
        print(f"\n  Account #{acct_id} has been closed.")
    except ValueError as e:
        print(f"\n  Error: {e}")
    pause()
 
 
MENU = {
    "1": ("Open new account",    screen_create),
    "2": ("Deposit",             screen_deposit),
    "3": ("Withdraw",            screen_withdraw),
    "4": ("Check balance",       screen_balance),
    "5": ("List all accounts",   screen_list),
    "6": ("Transfer",            screen_transfer),
    "7": ("Transaction history", screen_history),
    "8": ("Close account",       screen_delete),
    "0": ("Exit",                None),
}
 
 
def main():
    while True:
        show_header("Main Menu")
        for key, (label, _) in MENU.items():
            print(f"    [{key}]  {label}")
        print()
        line()
        choice = input("  Enter option: ").strip()
 
        if choice not in MENU:
            print("  Invalid option.")
            pause()
            continue
 
        label, action = MENU[choice]
        if action is None:
            clear()
            print("\n  Goodbye!\n")
            sys.exit(0)
 
        action()
 
 
if __name__ == "__main__":
    main()
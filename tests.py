# tests.py
# Run this to check that all the banking functions work correctly.
# Usage: python tests.py
 
import sys
from banking import (
    create_account, deposit, withdraw, check_balance,
    list_accounts, get_account, delete_account,
    transfer, get_transaction_history,
)
 
passed = 0
failed = 0
errors = []
 
 
def run(name, fn):
    global passed, failed
    try:
        fn()
        print(f"  PASS  {name}")
        passed += 1
    except AssertionError as e:
        print(f"  FAIL  {name}  ->  {e or 'assertion failed'}")
        errors.append((name, str(e)))
        failed += 1
    except Exception as e:
        print(f"  ERROR {name}  ->  {type(e).__name__}: {e}")
        errors.append((name, str(e)))
        failed += 1
 
 
# Each test creates its own accounts and cleans them up when done
 
def test_create_basic():
    acct_id = create_account("Test User", 100.00, user_id=1)
    assert isinstance(acct_id, int) and acct_id > 0
    withdraw(acct_id, 100.00)
    delete_account(acct_id)
 
 
def test_create_zero_deposit():
    acct_id = create_account("Zero User", 0, user_id=1)
    assert check_balance(acct_id) == 0.0
    delete_account(acct_id)
 
 
def test_create_blank_name():
    try:
        create_account("   ", 50, user_id=1)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
 
 
def test_create_negative_deposit():
    try:
        create_account("Bad User", -10, user_id=1)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
 
 
def test_deposit_basic():
    acct_id = create_account("Deposit Test", 0, user_id=1)
    new_bal = deposit(acct_id, 250.00)
    assert new_bal == 250.00
    withdraw(acct_id, 250.00)
    delete_account(acct_id)
 
 
def test_deposit_multiple():
    acct_id = create_account("Multi Deposit", 0, user_id=1)
    deposit(acct_id, 100)
    deposit(acct_id, 200)
    deposit(acct_id, 50)
    assert check_balance(acct_id) == 350.00
    withdraw(acct_id, 350.00)
    delete_account(acct_id)
 
 
def test_deposit_zero_raises():
    acct_id = create_account("Zero Dep", 0, user_id=1)
    try:
        deposit(acct_id, 0)
        assert False
    except ValueError:
        pass
    finally:
        delete_account(acct_id)
 
 
def test_withdraw_basic():
    acct_id = create_account("Withdraw Test", 500, user_id=1)
    new_bal = withdraw(acct_id, 200)
    assert new_bal == 300.00
    withdraw(acct_id, 300)
    delete_account(acct_id)
 
 
def test_withdraw_full():
    acct_id = create_account("Full Withdraw", 75, user_id=1)
    assert withdraw(acct_id, 75) == 0.00
    delete_account(acct_id)
 
 
def test_withdraw_overdraft():
    acct_id = create_account("Broke", 50, user_id=1)
    try:
        withdraw(acct_id, 100)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    finally:
        withdraw(acct_id, 50)
        delete_account(acct_id)
 
 
def test_get_account_not_found():
    assert get_account(999999999) is None
 
 
def test_list_accounts_returns_list():
    assert isinstance(list_accounts(), list)
 
 
def test_delete_with_balance():
    acct_id = create_account("Cant Delete", 100, user_id=1)
    try:
        delete_account(acct_id)
        assert False
    except ValueError:
        pass
    finally:
        withdraw(acct_id, 100)
        delete_account(acct_id)
 
 
def test_transfer_basic():
    a = create_account("Sender", 500, user_id=1)
    b = create_account("Receiver", 100, user_id=1)
    na, nb = transfer(a, b, 200)
    assert na == 300.00
    assert nb == 300.00
    withdraw(a, 300)
    withdraw(b, 300)
    delete_account(a)
    delete_account(b)
 
 
def test_transfer_insufficient():
    a = create_account("Poor", 50, user_id=1)
    b = create_account("Rich", 200, user_id=1)
    try:
        transfer(a, b, 999)
        assert False
    except ValueError:
        pass
    assert check_balance(a) == 50.00
    assert check_balance(b) == 200.00
    withdraw(a, 50)
    withdraw(b, 200)
    delete_account(a)
    delete_account(b)
 
 
def test_transfer_same_account():
    acct_id = create_account("Same", 100, user_id=1)
    try:
        transfer(acct_id, acct_id, 50)
        assert False
    except ValueError:
        pass
    finally:
        withdraw(acct_id, 100)
        delete_account(acct_id)
 
 
def test_history_recorded():
    acct_id = create_account("History Test", 0, user_id=1)
    deposit(acct_id, 400)
    withdraw(acct_id, 100)
    types = [t["type"] for t in get_transaction_history(acct_id)]
    assert "deposit" in types
    assert "withdrawal" in types
    withdraw(acct_id, 300)
    delete_account(acct_id)
 
 
def test_history_unknown():
    try:
        get_transaction_history(999999999)
        assert False
    except ValueError:
        pass
 
 
ALL_TESTS = [
    ("Create account basic",           test_create_basic),
    ("Create account zero deposit",    test_create_zero_deposit),
    ("Create account blank name",      test_create_blank_name),
    ("Create account negative deposit",test_create_negative_deposit),
    ("Deposit basic",                  test_deposit_basic),
    ("Deposit multiple",               test_deposit_multiple),
    ("Deposit zero raises",            test_deposit_zero_raises),
    ("Withdraw basic",                 test_withdraw_basic),
    ("Withdraw full balance",          test_withdraw_full),
    ("Withdraw overdraft raises",      test_withdraw_overdraft),
    ("Get account not found",          test_get_account_not_found),
    ("List accounts returns list",     test_list_accounts_returns_list),
    ("Delete with balance raises",     test_delete_with_balance),
    ("Transfer basic",                 test_transfer_basic),
    ("Transfer insufficient funds",    test_transfer_insufficient),
    ("Transfer same account raises",   test_transfer_same_account),
    ("History recorded",               test_history_recorded),
    ("History unknown account",        test_history_unknown),
]
 
 
if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("  Banking System  -  Test Suite")
    print("=" * 50 + "\n")
 
    for name, fn in ALL_TESTS:
        run(name, fn)
 
    print()
    print("-" * 50)
    print(f"  {passed} passed   {failed} failed   {passed + failed} total")
    print("-" * 50)
 
    if errors:
        print("\nFailed tests:")
        for name, msg in errors:
            print(f"  {name}: {msg}")
        print()
 
    sys.exit(0 if failed == 0 else 1)
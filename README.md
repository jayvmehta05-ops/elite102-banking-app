# Elite 102 Banking System

A terminal-based banking app built with Python and MySQL for the Elite 102 final project.

---

## What It Does

- Create bank accounts
- Deposit and withdraw money
- Check account balances
- Transfer money between accounts
- View transaction history
- Close accounts

---

## How to Run It

**1. Install the required library**
```
pip install mysql-connector-python
```

**2. Set up your database credentials**

Copy `config.example.py`, rename it to `config.py`, and fill in your MySQL username and password.

**3. Create the database and tables**
```
python setup_db.py
```

**4. Run the app**
```
python main.py
```

**5. Run the tests**
```
python tests.py
```

---

## File Overview

| File | Description |
|---|---|
| `main.py` | The main app with the terminal menu |
| `banking.py` | All the banking functions |
| `db.py` | Connects to the MySQL database |
| `config.py` | My database credentials (not on GitHub) |
| `setup_db.py` | Creates the database and tables |
| `tests.py` | Tests for every banking function |

---

## Built With

- Python 3
- MySQL
- mysql-connector-python
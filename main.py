# src/bank_system/models.py
from dataclasses import dataclass

@dataclass
class BankAccount:
    client_name: str
    account_number: str
    balance: float

# src/bank_system/services.py
from bank_system.models import BankAccount

def deposit(account: BankAccount, amount: float) -> None:
    if amount > 0:
        account.balance += amount

def withdraw(account: BankAccount, amount: float) -> bool:
    if 0 < amount <= account.balance:
        account.balance -= amount
        return True
    return False

def find_account(accounts: list[BankAccount], account_number: str) -> BankAccount | None:
    return next((acc for acc in accounts if acc.account_number == account_number), None)

def calculate_total_balance(accounts: list[BankAccount]) -> float:
    return sum(acc.balance for acc in accounts)

# src/bank_system/main.py
from bank_system.models import BankAccount
from bank_system.services import deposit, withdraw, find_account, calculate_total_balance

def main() -> None:
    accounts = [
        BankAccount("Ivanov Ivan", "UA123", 1000.0),
        BankAccount("Petrenko Petro", "UA456", 2500.0)
    ]
    
    print("Initial state:")
    for acc in accounts:
        print(f"Client: {acc.client_name}, Balance: {acc.balance}")
    
    target = find_account(accounts, "UA123")
    if target:
        deposit(target, 500.0)
        print(f"\nUpdated {target.client_name} balance: {target.balance}")
        
    print(f"Total Bank Balance: {calculate_total_balance(accounts)}")

if __name__ == "__main__":
    main()

# pyproject.toml
[build-system]
requires = ["setuptools>=70"]
build-backend = "setuptools.build_meta"

[project]
name = "bank-system"
version = "0.1.0"
description = "Banking system project"
requires-python = ">=3.11"

[project.scripts]
bank-system = "bank_system.main:main"
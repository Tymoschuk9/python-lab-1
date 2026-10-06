import dataclasses
from typing import List, Optional

@dataclasses.dataclass
class BankAccount:
    owner: str
    account_number: str
    balance: float

    def deposit(self, amount: float) -> None:
        if amount > 0:
            self.balance += amount

    def withdraw(self, amount: float) -> bool:
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False

def find_account(accounts: List[BankAccount], account_number: str) -> Optional[BankAccount]:
    return next((acc for acc in accounts if acc.account_number == account_number), None)

def calculate_total_balance(accounts: List[BankAccount]) -> float:
    return sum(acc.balance for acc in accounts)

def main() -> None:
    accounts = [
        BankAccount("Ivanov Ivan", "1001", 1500.0),
        BankAccount("Petrenko Petro", "1002", 500.0),
        BankAccount("Sydorenko Anna", "1003", 2500.0)
    ]

    print(f"Total system balance: {calculate_total_balance(accounts):.2f}")
    
    target = "1002"
    acc = find_account(accounts, target)
    if acc:
        acc.deposit(200.0)
        print(f"Deposited to {target}. New balance: {acc.balance}")

if __name__ == "__main__":
    main()
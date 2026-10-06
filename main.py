# -*- coding: utf-8 -*-

"""
Проєкт: Bank Account System (Система банківських рахунків)
Варіант: 4
Організація проєкту: src-layout
"""

# ==========================================
# FILE: src/bank_system/__init__.py
# ==========================================
"""Пакет системи управління банківськими рахунками."""
__version__ = "0.1.0"


# ==========================================
# FILE: src/bank_system/exceptions.py
# ==========================================
class BankSystemError(Exception):
    """Базовий виняток для банківської системи."""
    pass


class InsufficientFundsError(BankSystemError):
    """Виняток, який виникає при спробі зняти більше коштів, ніж є на балансі."""
    pass


class AccountNotFoundError(BankSystemError):
    """Виняток, який виникає, якщо рахунок не знайдено."""
    pass


class ValidationError(BankSystemError):
    """Виняток для помилок валідації вхідних даних."""
    pass


# ==========================================
# FILE: src/bank_system/models.py
# ==========================================
from dataclasses import dataclass


@dataclass
class Account:
    """Клас моделі даних банківського рахунку."""
    client_name: str
    account_number: str
    balance: float

    def __post_init__(self) -> None:
        """Валідація початкових даних після ініціалізації."""
        if not self.client_name.strip():
            raise ValidationError("Ім'я клієнта не може бути порожнім.")
        if not self.account_number.strip():
            raise ValidationError("Номер рахунку не може бути порожнім.")
        if self.balance < 0:
            raise ValidationError("Баланс не може бути від'ємним.")


# ==========================================
# FILE: src/bank_system/services.py
# ==========================================
import re
from typing import List, Optional


# Глобальна конфігураційна константа
MIN_DEPOSIT_AMOUNT = 0.01


def deposit(account: Account, amount: float) -> None:
    """
    Поповнення рахунку.
    Raises:
        ValidationError: якщо сума менша за мінімальну.
    """
    if amount < MIN_DEPOSIT_AMOUNT:
        raise ValidationError(f"Мінімальна сума поповнення: {MIN_DEPOSIT_AMOUNT} грн.")
    account.balance += amount


def withdraw(account: Account, amount: float) -> None:
    """
    Списання коштів з рахунку.
    Raises:
        ValidationError: якщо сума списання некоректна.
        InsufficientFundsError: якщо на рахунку недостатньо коштів.
    """
    if amount <= 0:
        raise ValidationError("Сума списання повинна бути більшою за нуль.")
    if account.balance - amount < 0:
        raise InsufficientFundsError(
            f"Недостатньо коштів на рахунку {account.account_number}. "
            f"Доступно: {account.balance:.2f} грн., спроба зняти: {amount:.2f} грн."
        )
    account.balance -= amount


def find_account(accounts: List[Account], account_number: str) -> Optional[Account]:
    """
    Пошук рахунку за його номером.
    """
    for account in accounts:
        if account.account_number.strip() == account_number.strip():
            return account
    return None


def calculate_total_funds(accounts: List[Account]) -> float:
    """
    Обчислення загальної суми коштів на всіх рахунках.
    """
    return sum(account.balance for account in accounts)


def validate_account_number(account_number: str) -> bool:
    """
    Перевірка формату номера рахунку (наприклад, UA і 6 цифр).
    """
    pattern = r"^UA\d{6}$"
    return bool(re.match(pattern, account_number))


# ==========================================
# FILE: src/bank_system/main.py
# ==========================================
import sys


def create_demo_accounts() -> List[Account]:
    """Створення початкових тестових даних."""
    return [
        Account(client_name="Олексій Коваленко", account_number="UA100001", balance=15000.50),
        Account(client_name="Марія Петренко", account_number="UA100002", balance=450.00),
        Account(client_name="Іван Сірко", account_number="UA100003", balance=9800.15),
    ]


def print_menu() -> None:
    """Виведення консольного меню на екран."""
    print("\n" + "=" * 50)
    print("        СИСТЕМА КЕРУВАННЯ БАНКІВСЬКИМИ РАХУНКАМИ        ")
    print("=" * 50)
    print("1. Показати всі рахунки")
    print("2. Знайти рахунок та виконати операції")
    print("3. Створити новий рахунок")
    print("4. Показати загальну суму коштів у банку")
    print("5. Вихід")
    print("=" * 50)


def print_accounts(accounts: List[Account]) -> None:
    """Форматований вивід списку рахунків."""
    if not accounts:
        print("\n[!] Немає відкритих рахунків.")
        return

    print("\n" + "-" * 65)
    print(f"{'Клієнт':<25} | {'Номер рахунку':<15} | {'Баланс (грн)':>18}")
    print("-" * 65)
    for acc in accounts:
        print(f"{acc.client_name:<25} | {acc.account_number:<15} | {acc.balance:>18.2f}")
    print("-" * 65)


def handle_account_operations(account: Account) -> None:
    """Підменю для роботи з конкретним рахунком."""
    while True:
        print(f"\n--- Рахунок {account.account_number} ({account.client_name}) ---")
        print("Баланс:", f"{account.balance:.2f} грн.")
        print("1. Поповнити баланс")
        print("2. Списати кошти")
        print("3. Назад до головного меню")

        choice = input("Оберіть операцію: ").strip()

        if choice == "1":
            try:
                amount_str = input("Введіть суму для поповнення: ").strip()
                amount = float(amount_str)
                deposit(account, amount)
                print(f"[+] Рахунок успішно поповнено на {amount:.2f} грн.")
            except ValueError:
                print("[Помилка] Будь ласка, введіть коректне число.")
            except ValidationError as e:
                print(f"[Помилка валідації] {e}")

        elif choice == "2":
            try:
                amount_str = input("Введіть суму для списання: ").strip()
                amount = float(amount_str)
                withdraw(account, amount)
                print(f"[-] З рахунку списано {amount:.2f} грн.")
            except ValueError:
                print("[Помилка] Будь ласка, введіть коректне число.")
            except (ValidationError, InsufficientFundsError) as e:
                print(f"[Помилка операції] {e}")

        elif choice == "3":
            break
        else:
            print("[!] Невідома операція. Спробуйте ще раз.")


def run() -> None:
    """Основний цикл роботи консольної програми."""
    accounts = create_demo_accounts()

    while True:
        print_menu()
        choice = input("Оберіть пункт меню: ").strip()

        if choice == "1":
            print_accounts(accounts)

        elif choice == "2":
            acc_num = input("Введіть номер рахунку (наприклад, UA100001): ").strip()
            account = find_account(accounts, acc_num)
            if account:
                handle_account_operations(account)
            else:
                print(f"[!] Рахунок з номером '{acc_num}' не знайдено.")

        elif choice == "3":
            print("\n--- Створення нового рахунку ---")
            name = input("Введіть повне ім'я клієнта: ").strip()
            acc_num = input("Введіть новий номер рахунку (формат: UAxxxxxx, де x - цифри): ").strip()

            if not validate_account_number(acc_num):
                print("[Помилка] Номер рахунку має бути у форматі 'UA' та 6 цифр (наприклад, UA999999).")
                continue

            if find_account(accounts, acc_num):
                print("[Помилка] Рахунок з таким номером уже існує в базі.")
                continue

            try:
                bal_str = input("Введіть початковий баланс (грн): ").strip()
                balance = float(bal_str)
                new_acc = Account(client_name=name, account_number=acc_num, balance=balance)
                accounts.append(new_acc)
                print(f"[+] Рахунок для '{name}' успішно створено!")
            except ValueError:
                print("[Помилка] Баланс має бути числовим значенням.")
            except ValidationError as e:
                print(f"[Помилка валідації] {e}")

        elif choice == "4":
            total = calculate_total_funds(accounts)
            print(f"\n[i] Загальна сума на всіх банківських рахунках: {total:.2f} грн.")

        elif choice == "5":
            print("\nДякуємо, що користуєтесь нашими банківськими послугами. До зустрічі!")
            sys.exit(0)

        else:
            print("[!] Невідомий пункт меню. Спробуйте ще раз.")


if __name__ == "__main__":
    run()
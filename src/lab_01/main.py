# ==============================================================================
# FILE: src/bank_system/exceptions.py
# ==============================================================================
"""Модуль для визначення користувацьких винятків системи."""

class BankSystemError(Exception):
    """Базовий клас для всіх винятків у системі банківських рахунків."""
    pass


class InsufficientFundsError(BankSystemError):
    """Виникає, коли баланс рахунку недостатній для зняття або переказу коштів."""
    pass


class NegativeAmountError(BankSystemError):
    """Виникає при спробі виконати операцію з нульовою чи від'ємною сумою."""
    pass


class AccountNotFoundError(BankSystemError):
    """Виникає, коли рахунок не знайдено в системі."""
    pass


# ==============================================================================
# FILE: src/bank_system/models.py
# ==============================================================================
"""Модуль, що містить описи моделей даних (Data Models)."""

from dataclasses import dataclass


@dataclass
class BankAccount:
    """Клас для представлення банківського рахунку клієнта."""
    client_name: str
    account_number: str
    balance: float

    def __post_init__(self) -> None:
        """Валідація початкових даних після ініціалізації."""
        if self.balance < 0:
            raise ValueError("Початковий баланс не може бути від'ємним.")
        
        if not self.client_name.strip():
            raise ValueError("Ім'я клієнта не може бути порожнім.")
            
        if not self.account_number.strip():
            raise ValueError("Номер рахунку не може бути порожнім.")


# ==============================================================================
# FILE: src/bank_system/services.py
# ==============================================================================
"""Модуль для реалізації бізнес-логіки (Business Logic) системи рахунків."""

from bank_system.models import BankAccount
from bank_system.exceptions import InsufficientFundsError, NegativeAmountError


def deposit(account: BankAccount, amount: float) -> None:
    """Поповнення рахунку на задану суму."""
    if amount <= 0:
        raise NegativeAmountError("Сума поповнення повинна бути строго більшою за нуль.")
    account.balance += amount


def withdraw(account: BankAccount, amount: float) -> None:
    """Списання коштів з рахунку з контролем від'ємного балансу."""
    if amount <= 0:
        raise NegativeAmountError("Сума списання повинна бути строго більшою за нуль.")
    if account.balance < amount:
        raise InsufficientFundsError(
            f"Недостатньо коштів на рахунку {account.account_number}. "
            f"Баланс: {account.balance:.2f} UAH. Запитувано: {amount:.2f} UAH."
        )
    account.balance -= amount


def find_account(accounts: list[BankAccount], account_number: str) -> BankAccount | None:
    """Пошук рахунку за його унікальним номером (ігноруючи зайві пробіли)."""
    cleaned_num = account_number.strip()
    for account in accounts:
        if account.account_number.strip() == cleaned_num:
            return account
    return None


def calculate_total_funds(accounts: list[BankAccount]) -> float:
    """Обчислення сумарного обсягу коштів на всіх банківських рахунках."""
    return sum(account.balance for account in accounts)


def sort_accounts_by_balance(accounts: list[BankAccount], descending: bool = True) -> list[BankAccount]:
    """Сортування рахунків за балансом (за замовчуванням у порядку спадання)."""
    return sorted(accounts, key=lambda x: x.balance, reverse=descending)


# ==============================================================================
# FILE: src/bank_system/main.py
# ==============================================================================
"""Основний модуль, точка входу в програму. Консольний інтерфейс користувача."""

import sys
from bank_system.models import BankAccount
from bank_system.exceptions import BankSystemError
from bank_system.services import (
    deposit,
    withdraw,
    find_account,
    calculate_total_funds,
    sort_accounts_by_balance,
)


def create_demo_accounts() -> list[BankAccount]:
    """Створення демонстраційного набору даних."""
    return [
        BankAccount(client_name="Олександр Петренко", account_number="UA100200", balance=15000.50),
        BankAccount(client_name="Марія Коваленко", account_number="UA300400", balance=2800.00),
        BankAccount(client_name="Ігор Шевченко", account_number="UA500600", balance=450.75),
        BankAccount(client_name="Олена Бойко", account_number="UA700800", balance=98500.00),
    ]


def print_accounts_table(accounts: list[BankAccount]) -> None:
    """Форматоване виведення списку рахунків у вигляді таблиці."""
    if not accounts:
        print("\n[!] Рахунки в системі відсутні.")
        return

    print("\n" + "=" * 65)
    print(f"{'Номер рахунку':<15} | {'Ім’я клієнта':<25} | {'Баланс (UAH)':>18}")
    print("-" * 65)
    for acc in accounts:
        print(f"{acc.account_number:<15} | {acc.client_name:<25} | {acc.balance:>18.2f}")
    print("=" * 65)


def get_float_input(prompt: str) -> float:
    """Безпечне зчитування дійсного числа з консолі."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("[Помилка] Будь ласка, введіть числове значення.")


def show_menu() -> None:
    """Виведення списку команд інтерактивного меню."""
    print("\n--- СИСТЕМА БАНКІВСЬКИХ РАХУНКІВ ---")
    print("1. Показати всі рахунки")
    print("2. Перевірити баланс окремого рахунку")
    print("3. Поповнити рахунок")
    print("4. Списати кошти з рахунку")
    print("5. Переказати кошти між рахунками")
    print("6. Пошук рахунку за номером")
    print("7. Обчислити загальний капітал банку")
    print("8. Створити новий рахунок")
    print("9. Сортувати рахунки за балансом")
    print("10. Вийти з програми")


def main() -> None:
    """Головна керуюча функція."""
    accounts = create_demo_accounts()

    while True:
        show_menu()
        choice = input("\nОберіть пункт меню (1-10): ").strip()

        try:
            if choice == "1":
                print_accounts_table(accounts)

            elif choice == "2":
                num = input("Введіть номер рахунку: ").strip()
                acc = find_account(accounts, num)
                if acc:
                    print(f"\n[Успішно] Клієнт: {acc.client_name}")
                    print(f"Поточний баланс рахунку {acc.account_number}: {acc.balance:.2f} UAH")
                else:
                    print("[!] Рахунок не знайдено.")

            elif choice == "3":
                num = input("Введіть номер рахунку: ").strip()
                acc = find_account(accounts, num)
                if acc:
                    amount = get_float_input("Введіть суму поповнення (UAH): ")
                    deposit(acc, amount)
                    print(f"[Успішно] Рахунок поповнено! Поточний баланс: {acc.balance:.2f} UAH")
                else:
                    print("[!] Рахунок не знайдено.")

            elif choice == "4":
                num = input("Введіть номер рахунку: ").strip()
                acc = find_account(accounts, num)
                if acc:
                    amount = get_float_input("Введіть суму списання (UAH): ")
                    withdraw(acc, amount)
                    print(f"[Успішно] Списання виконано! Поточний баланс: {acc.balance:.2f} UAH")
                else:
                    print("[!] Рахунок не знайдено.")

            elif choice == "5":
                sender_num = input("Введіть номер рахунку відправника: ").strip()
                sender = find_account(accounts, sender_num)
                if not sender:
                    print("[!] Рахунок відправника не знайдено.")
                    continue

                receiver_num = input("Введіть номер рахунку отримувача: ").strip()
                receiver = find_account(accounts, receiver_num)
                if not receiver:
                    print("[!] Рахунок отримувача не знайдено.")
                    continue

                if sender == receiver:
                    print("[!] Помилка: рахунки відправника та отримувача збігаються.")
                    continue

                amount = get_float_input("Введіть суму переказу (UAH): ")
                withdraw(sender, amount)
                deposit(receiver, amount)
                print(f"[Успішно] Переказ {amount:.2f} UAH проведено.")
                print(f"Новий баланс відправника ({sender.account_number}): {sender.balance:.2f} UAH")

            elif choice == "6":
                num = input("Введіть номер рахунку: ").strip()
                acc = find_account(accounts, num)
                if acc:
                    print(f"\n[Знайдено рахунок]:")
                    print(f"  Власник:        {acc.client_name}")
                    print(f"  Номер рахунку:  {acc.account_number}")
                    print(f"  Поточний баланс:{acc.balance:.2f} UAH")
                else:
                    print("[!] Рахунок не знайдено.")

            elif choice == "7":
                total_funds = calculate_total_funds(accounts)
                print(f"\n[Капіталізація] Загальна сума на всіх рахунках: {total_funds:.2f} UAH")

            elif choice == "8":
                name = input("Введіть ім'я та прізвище клієнта: ").strip()
                num = input("Введіть бажаний унікальний номер рахунку: ").strip()
                
                if find_account(accounts, num):
                    print("[!] Помилка: Рахунок з таким номером вже зареєстровано в системі.")
                    continue
                
                bal = get_float_input("Введіть початковий баланс: ")
                new_acc = BankAccount(client_name=name, account_number=num, balance=bal)
                accounts.append(new_acc)
                print(f"[Успішно] Рахунок для '{name}' створено!")

            elif choice == "9":
                order = input("Сортувати за спаданням? (y/n): ").strip().lower()
                descending = order != "n"
                sorted_accs = sort_accounts_by_balance(accounts, descending=descending)
                print_accounts_table(sorted_accs)

            elif choice == "10":
                print("\n[Програма] Роботу завершено. Дякуємо, що обрали наш банк!")
                sys.exit(0)

            else:
                print("[!] Невідома опція меню. Будь ласка, введіть число від 1 до 10.")

        except BankSystemError as e:
            print(f"\n[Помилка банківської системи] {e}")
        except ValueError as e:
            print(f"\n[Помилка вхідних даних] {e}")


if __name__ == "__main__":
    main()


# ==============================================================================
# FILE: src/bank_system/__init__.py
# ==============================================================================
"""Ініціалізаційний модуль пакету bank_system."""

__version__ = "0.1.0"


# ==============================================================================
# FILE: pyproject.toml
# ==============================================================================
# [build-system]
# requires = ["setuptools>=70"]
# build-backend = "setuptools.build_meta"
# 
# [project]
# name = "bank-system"
# version = "0.1.0"
# description = "Laboratory project implementing a modular Bank Account Management system"
# requires-python = ">=3.11"
# 
# [project.scripts]
# bank-system = "bank_system.main:main"


# ==============================================================================
# FILE: .gitignore
# ==============================================================================
# .venv/
# __pycache__/
# *.pyc
# .pytest_cache/
# .idea/
# .vscode/
# dist/
# build/
# *.egg-info/
# .env
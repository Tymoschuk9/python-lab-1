import os
import sys
from pathlib import Path

# ==========================================
# 1. КОНСТАНТИ ВМІСТУ ФАЙЛІВ ПРОЄКТУ
# ==========================================

INIT_CONTENT = """\"\"\"Bank Account System package.\"\"\"

__version__ = "0.1.0"
"""

MODELS_CONTENT = """from dataclasses import dataclass


class InsufficientFundsError(Exception):
    \"\"\"Виникає, коли на рахунку недостатньо коштів для списання.\"\"\"
    pass


class InvalidAmountError(Exception):
    \"\"\"Виникає, коли вказано некоректну суму (від'ємну або нульову).\"\"\"
    pass


@dataclass
class Account:
    client_name: str
    account_number: str
    balance: float

    def __post_init__(self) -> None:
        if self.balance < 0:
            raise ValueError("Початковий баланс не може бути від'ємним.")
"""

SERVICES_CONTENT = """from bank_system.models import Account, InsufficientFundsError, InvalidAmountError

# Конфігураційна константа
MIN_TRANSACTION_AMOUNT = 0.01


def deposit(account: Account, amount: float) -> None:
    \"\"\"Поповнює рахунок на вказану суму.\"\"\"
    if amount < MIN_TRANSACTION_AMOUNT:
        raise InvalidAmountError(
            f"Сума поповнення повинна бути не меншою за {MIN_TRANSACTION_AMOUNT} UAH."
        )
    account.balance += amount


def withdraw(account: Account, amount: float) -> None:
    \"\"\"Списує вказану суму з рахунку. Запобігає від'ємному балансу.\"\"\"
    if amount < MIN_TRANSACTION_AMOUNT:
        raise InvalidAmountError(
            f"Сума списання повинна бути не меншою за {MIN_TRANSACTION_AMOUNT} UAH."
        )
    if account.balance - amount < 0:
        raise InsufficientFundsError(
            f"Недостатньо коштів на рахунку {account.account_number}. "
            f"Доступно: {account.balance:.2f} UAH, запитано: {amount:.2f} UAH."
        )
    account.balance -= amount


def find_account(accounts: list[Account], account_number: str) -> Account | None:
    \"\"\"Шукає рахунок за його унікальним номером (без урахування регістру та пробілів).\"\"\"
    cleaned_num = account_number.strip().lower()
    for account in accounts:
        if account.account_number.strip().lower() == cleaned_num:
            return account
    return None


def search_accounts(accounts: list[Account], query: str) -> list[Account]:
    \"\"\"Шукає рахунки за іменем клієнта або номером рахунку (частковий збіг).\"\"\"
    cleaned_query = query.strip().lower()
    return [
        acc for acc in accounts
        if cleaned_query in acc.client_name.lower() or cleaned_query in acc.account_number.lower()
    ]


def calculate_total_funds(accounts: list[Account]) -> float:
    \"\"\"Обчислює загальну суму коштів на всіх рахунках.\"\"\"
    return sum(acc.balance for acc in accounts)


def sort_accounts_by_balance(accounts: list[Account], descending: bool = True) -> list[Account]:
    \"\"\"Повертає відсортований список рахунків за балансом.\"\"\"
    return sorted(accounts, key=lambda acc: acc.balance, reverse=descending)
"""

MAIN_CONTENT = """import sys
from bank_system.models import Account, InsufficientFundsError, InvalidAmountError
from bank_system.services import (
    deposit,
    withdraw,
    find_account,
    search_accounts,
    calculate_total_funds,
    sort_accounts_by_balance,
)


def create_demo_accounts() -> list[Account]:
    \"\"\"Створює демонстраційні банківські рахунки.\"\"\"
    return [
        Account("Олександр Шевченко", "UA89300001", 15000.50),
        Account("Марія Коваленко", "UA89300002", 4500.00),
        Account("Дмитро Лисенко", "UA89300003", 750.25),
        Account("Анна Петренко", "UA89300004", 98200.00),
    ]


def print_accounts(accounts: list[Account]) -> None:
    \"\"\"Виводить таблицю рахунків.\"\"\"
    if not accounts:
        print("Список рахунків порожній.")
        return
    print(f"\\n{'Клієнт':<25} | {'Номер рахунку':<15} | {'Баланс (UAH)':>15}")
    print("-" * 62)
    for acc in accounts:
        print(f"{acc.client_name:<25} | {acc.account_number:<15} | {acc.balance:>15.2f}")


def get_float_input(prompt: str) -> float:
    \"\"\"Валідує введення дійсного числа користувачем.\"\"\"
    while True:
        try:
            return float(input(prompt).strip())
        except ValueError:
            print("Помилка: Введіть коректне числове значення.")


def print_menu() -> None:
    print("\\n=== СИСТЕМА БАНКІВСЬКИХ РАХУНКІВ ===")
    print("1. Показати всі рахунки")
    print("2. Знайти рахунок (ім'я / номер)")
    print("3. Поповнити рахунок")
    print("4. Списати кошти")
    print("5. Переказати кошти іншому клієнту")
    print("6. Показати загальний капітал банку")
    print("7. Сортувати рахунки за балансом")
    print("8. Створити новий рахунок")
    print("9. Вийти")


def main() -> None:
    accounts = create_demo_accounts()

    while True:
        print_menu()
        choice = input("Оберіть опцію (1-9): ").strip()

        if choice == "1":
            print("\\n--- Список усіх банківських рахунків ---")
            print_accounts(accounts)

        elif choice == "2":
            print("\\n--- Пошук рахунку ---")
            query = input("Введіть ім'я клієнта або номер рахунку: ")
            results = search_accounts(accounts, query)
            print(f"Знайдено рахунків: {len(results)}")
            print_accounts(results)

        elif choice == "3":
            print("\\n--- Поповнення рахунку ---")
            acc_num = input("Введіть номер рахунку: ")
            account = find_account(accounts, acc_num)
            if account:
                amount = get_float_input("Введіть суму поповнення (UAH): ")
                try:
                    deposit(account, amount)
                    print(f"Успішно! Новий баланс рахунку {account.account_number}: {account.balance:.2f} UAH")
                except InvalidAmountError as e:
                    print(f"Помилка виконання операції: {e}")
            else:
                print("Помилка: Рахунок не знайдено.")

        elif choice == "4":
            print("\\n--- Списання коштів ---")
            acc_num = input("Введіть номер рахунку: ")
            account = find_account(accounts, acc_num)
            if account:
                amount = get_float_input("Введіть суму списання (UAH): ")
                try:
                    withdraw(account, amount)
                    print(f"Успішно! Новий баланс рахунку {account.account_number}: {account.balance:.2f} UAH")
                except (InvalidAmountError, InsufficientFundsError) as e:
                    print(f"Помилка виконання транзакції: {e}")
            else:
                print("Помилка: Рахунок не знайдено.")

        elif choice == "5":
            print("\\n--- Міжбанківський переказ коштів ---")
            sender_num = input("Введіть номер рахунку відправника: ")
            sender = find_account(accounts, sender_num)
            if not sender:
                print("Помилка: Рахунок відправника не знайдено.")
                continue

            receiver_num = input("Введіть номер рахунку одержувача: ")
            receiver = find_account(accounts, receiver_num)
            if not receiver:
                print("Помилка: Рахунок одержувача не знайдено.")
                continue

            if sender == receiver:
                print("Помилка: Рахунок відправника та одержувача не можуть бути однаковими.")
                continue

            amount = get_float_input("Введіть суму переказу (UAH): ")
            try:
                withdraw(sender, amount)
                deposit(receiver, amount)
                print("Транзакція пройшла успішно!")
                print(f"Баланс відправника ({sender.account_number}): {sender.balance:.2f} UAH")
                print(f"Баланс одержувача ({receiver.account_number}): {receiver.balance:.2f} UAH")
            except (InvalidAmountError, InsufficientFundsError) as e:
                print(f"Помилка транзакції переказу: {e}")

        elif choice == "6":
            total = calculate_total_funds(accounts)
            print(f"\\nЗагальна сума на всіх рахунках банку: {total:.2f} UAH")

        elif choice == "7":
            print("\\n--- Сортування рахунків ---")
            order = input("Сортувати за спаданням балансу? (y/n, за замовчуванням 'y'): ").strip().lower()
            descending = order != 'n'
            sorted_list = sort_accounts_by_balance(accounts, descending=descending)
            print_accounts(sorted_list)

        elif choice == "8":
            print("\\n--- Створення нового рахунку ---")
            name = input("Введіть ПІБ клієнта: ").strip()
            if not name:
                print("Помилка: ПІБ не може бути порожнім.")
                continue
            acc_num = input("Введіть унікальний номер рахунку (наприклад, UA89300005): ").strip()
            if not acc_num:
                print("Помилка: Номер рахунку не може бути порожнім.")
                continue
            if find_account(accounts, acc_num):
                print("Помилка: Рахунок з таким номером вже існує в системі.")
                continue
            balance = get_float_input("Введіть початковий баланс (UAH): ")
            try:
                new_acc = Account(client_name=name, account_number=acc_num, balance=balance)
                accounts.append(new_acc)
                print(f"Рахунок {acc_num} для клієнта '{name}' успішно зареєстровано!")
            except ValueError as e:
                print(f"Помилка створення рахунку: {e}")

        elif choice == "9":
            print("Вихід із системи. Дякуємо, що користуєтесь нашими послугами!")
            break
        else:
            print("Помилка: Невідома опція меню. Спробуйте ще раз.")


if __name__ == "__main__":
    main()
"""

PYPROJECT_CONTENT = """[build-system]
requires = ["setuptools>=70"]
build-backend = "setuptools.build_meta"

[project]
name = "bank-system"
version = "0.1.0"
description = "Laboratory work #1: Bank Account System in Python"
requires-python = ">=3.11"

[project.scripts]
bank-system = "bank_system.main:main"
"""

GITIGNORE_CONTENT = """.venv/
__pycache__/
*.pyc
.pytest_cache/
.idea/
.vscode/
dist/
build/
*.egg-info/
.env
"""

README_CONTENT = """# Bank Account System

Консольний застосунок для керування банківськими рахунками. Лабораторна робота №1 з дисципліни «Професійний Python» (Варіант №4).

## Вимоги

* Python 3.11+

## Структура проєкту

Створена за принципом `src-layout`:
text
bank_system/
├── pyproject.toml
├── README.md
├── .gitignore
├── src/
│   └── bank_system/
│       ├── __init__.py
│       ├── main.py
│       ├── models.py
│       └── services.py
└── tests/


## Встановлення

1. Створіть та активуйте віртуальне середовище:
   bash
   python -m venv .venv
   # Windows:
   .venv\\Scripts\\activate
   # macOS/Linux:
   source .venv/bin/activate
   
2. Встановіть локальний пакет у режимі редагування (editable mode):
   bash
   python -m pip install -e .
   

## Запуск програми

Запуск як модуля Python:
bash
python -m bank_system.main

Або через згенеровану консольну команду:
bash
bank-system

"""

# ==========================================
# 2. АВТОМАТИЧНА ГЕНЕРАЦІЯ СТРУКТУРИ ПРОЄКТУ
# ==========================================


def generate_project_structure() -> None:
    print("[*] Початок створення структури проєкту за принципом src-layout...")

    # Створення директорій
    base_dir = Path.cwd()
    src_dir = base_dir / "src" / "bank_system"
    tests_dir = base_dir / "tests"

    src_dir.mkdir(parents=True, exist_ok=True)
    tests_dir.mkdir(exist_ok=True)

    # Визначення шляхів до файлів
    files = {
        base_dir / ".gitignore": GITIGNORE_CONTENT,
        base_dir / "pyproject.toml": PYPROJECT_CONTENT,
        base_dir / "README.md": README_CONTENT,
        src_dir / "__init__.py": INIT_CONTENT,
        src_dir / "models.py": MODELS_CONTENT,
        src_dir / "services.py": SERVICES_CONTENT,
        src_dir / "main.py": MAIN_CONTENT,
    }

    # Запис вмісту у відповідні файли
    for file_path, content in files.items():
        file_path.write_text(content, encoding="utf-8")
        print(f"  [+] Створено файл: {file_path.relative_to(base_dir)}")

    print("[*] Усі файли проєкту успішно згенеровано.")


if __name__ == "__main__":
    # Створюємо файлову структуру проєкту на диску у поточній робочій теці
    generate_project_structure()

    # Додаємо шлях до згенерованих файлів у sys.path для можливості прямого імпорту
    sys.path.insert(0, str(Path.cwd() / "src"))

    print("\n" + "=" * 50)
    print(" ПРОЄКТ ЗГЕНЕРОВАНО ТА ГОТОВИЙ ДО ЗАПУСКУ!")
    print(" Запуск інтерактивної консолі програми...")
    print("=" * 50 + "\n")

    # Безпосередній запуск програми для демонстрації працездатності
    import bank_system.main

    bank_system.main.main()
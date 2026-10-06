# ==============================================================================
# FILE: src/bank_system/__init__.py
# ==============================================================================
"""
Пакет системи управління банківськими рахунками.
"""

__version__ = "0.1.0"


# ==============================================================================
# FILE: src/bank_system/models.py
# ==============================================================================
from dataclasses import dataclass


@dataclass
class BankAccount:
    """
    Клас, що представляє банківський рахунок клієнта.
    """
    client_name: str
    account_number: str
    balance: float

    def __post_init__(self) -> None:
        """
        Валідація початкових даних при створенні об'єкта.
        """
        if self.balance < 0:
            raise ValueError("Початковий баланс не може бути від'ємним.")
        if not self.client_name.strip():
            raise ValueError("Ім'я клієнта не може бути порожнім.")
        if not self.account_number.strip():
            raise ValueError("Номер рахунку не може бути порожнім.")


# ==============================================================================
# FILE: src/bank_system/services.py
# ==============================================================================
# Конфігураційна константа мінімальної суми операції
MIN_TRANSACTION_AMOUNT = 0.01


class BankSystemError(Exception):
    """Базовий клас для винятків банківської системи."""
    pass


class InsufficientFundsError(BankSystemError):
    """Виняток, який виникає при спробі зняти суму, що перевищує баланс."""
    pass


class InvalidAmountError(BankSystemError):
    """Виняток, який виникає при некоректній сумі транзакції (менше ліміту або від'ємна)."""
    pass


class AccountNotFoundError(BankSystemError):
    """Виняток, який виникає, коли рахунок не знайдено в системі."""
    pass


def deposit(account: BankAccount, amount: float) -> None:
    """
    Поповнення банківського рахунку.
    """
    if amount < MIN_TRANSACTION_AMOUNT:
        raise InvalidAmountError(
            f"Сума поповнення повинна бути не меншою за {MIN_TRANSACTION_AMOUNT} грн."
        )
    account.balance += amount


def withdraw(account: BankAccount, amount: float) -> None:
    """
    Списання коштів з банківського рахунку. Не дозволяє від'ємний баланс.
    """
    if amount < MIN_TRANSACTION_AMOUNT:
        raise InvalidAmountError(
            f"Сума списання повинна бути не меншою за {MIN_TRANSACTION_AMOUNT} грн."
        )
    if account.balance - amount < 0:
        raise InsufficientFundsError(
            f"Недостатньо коштів на рахунку {account.account_number}. "
            f"Доступно: {account.balance:.2f} грн, запитано: {amount:.2f} грн."
        )
    account.balance -= amount


def find_account_by_number(accounts: list[BankAccount], account_number: str) -> BankAccount:
    """
    Пошук рахунку за точним номером рахунку.
    """
    for account in accounts:
        if account.account_number == account_number:
            return account
    raise AccountNotFoundError(f"Рахунок з номером '{account_number}' не знайдено.")


def search_accounts_by_client(accounts: list[BankAccount], query: str) -> list[BankAccount]:
    """
    Пошук рахунків за ім'ям клієнта (частковий збіг без урахування регістру).
    """
    query_lower = query.strip().lower()
    return [
        acc for acc in accounts
        if query_lower in acc.client_name.lower()
    ]


def calculate_total_funds(accounts: list[BankAccount]) -> float:
    """
    Обчислення загальної суми всіх коштів у банку.
    """
    return sum(account.balance for account in accounts)


def sort_accounts_by_balance(accounts: list[BankAccount], descending: bool = True) -> list[BankAccount]:
    """
    Сортування рахунків за балансом.
    """
    return sorted(accounts, key=lambda x: x.balance, reverse=descending)


# ==============================================================================
# FILE: src/bank_system/main.py
# ==============================================================================
import sys


def create_demo_accounts() -> list[BankAccount]:
    """
    Створення початкових тестових даних.
    """
    return [
        BankAccount(client_name="Олексій Коваленко", account_number="UA12345", balance=15000.50),
        BankAccount(client_name="Марія Бондар", account_number="UA67890", balance=450.00),
        BankAccount(client_name="Іван Шевченко", account_number="UA54321", balance=98000.00),
        BankAccount(client_name="Олена Мельник", account_number="UA11223", balance=3200.75),
    ]


def print_accounts(accounts: list[BankAccount]) -> None:
    """
    Форматоване виведення списку рахунків.
    """
    if not accounts:
        print("Список рахунків порожній.")
        return

    print("\n" + "=" * 65)
    print(f"{'Клієнт':<25} | {'Номер рахунку':<15} | {'Баланс (грн)':>18}")
    print("-" * 65)
    for acc in accounts:
        print(f"{acc.client_name:<25} | {acc.account_number:<15} | {acc.balance:>18.2f}")
    print("=" * 65)


def get_float_input(prompt: str) -> float:
    """
    Валідація введення дійсного числа користувачем.
    """
    while True:
        try:
            val = float(input(prompt).strip())
            return val
        except ValueError:
            print("Помилка введення! Будь ласка, введіть числове значення.")


def print_menu() -> None:
    """
    Консольне меню системи.
    """
    print("\n--- СИСТЕМА БАНКІВСЬКИХ РАХУНКІВ ---")
    print("1. Показати всі рахунки (сортування за балансом)")
    print("2. Поповнити рахунок")
    print("3. Списати кошти")
    print("4. Перевірити баланс за номером")
    print("5. Пошук рахунків за ім'ям клієнта")
    print("6. Загальна сума коштів у банку")
    print("7. Створити новий рахунок")
    print("8. Вийти")


def run() -> None:
    """
    Основна точка входу для логіки виконання меню.
    """
    accounts = create_demo_accounts()

    while True:
        print_menu()
        choice = input("Виберіть опцію (1-8): ").strip()

        try:
            if choice == "1":
                sorted_accs = sort_accounts_by_balance(accounts)
                print("\nСписок рахунків (відсортовано за спаданням балансу):")
                print_accounts(sorted_accs)

            elif choice == "2":
                acc_num = input("Введіть номер рахунку для поповнення: ").strip()
                account = find_account_by_number(accounts, acc_num)
                amount = get_float_input("Введіть суму поповнення: ")
                deposit(account, amount)
                print(f"Успішно поповнено! Новий баланс рахунку {acc_num}: {account.balance:.2f} грн.")

            elif choice == "3":
                acc_num = input("Введіть номер рахунку для списання: ").strip()
                account = find_account_by_number(accounts, acc_num)
                amount = get_float_input("Введіть суму списання: ")
                withdraw(account, amount)
                print(f"Успішно списано! Новий баланс рахунку {acc_num}: {account.balance:.2f} грн.")

            elif choice == "4":
                acc_num = input("Введіть номер рахунку: ").strip()
                account = find_account_by_number(accounts, acc_num)
                print(f"\nРахунок: {account.account_number}")
                print(f"Власник: {account.client_name}")
                print(f"Поточний баланс: {account.balance:.2f} грн.")

            elif choice == "5":
                query = input("Введіть ім'я клієнта або його частину для пошуку: ").strip()
                found = search_accounts_by_client(accounts, query)
                print(f"\nЗнайдено рахунків за запитом '{query}': {len(found)}")
                print_accounts(found)

            elif choice == "6":
                total = calculate_total_funds(accounts)
                print(f"\nЗагальний обсяг коштів у банку: {total:.2f} грн.")

            elif choice == "7":
                name = input("Введіть ім'я та прізвище клієнта: ").strip()
                acc_num = input("Введіть новий унікальний номер рахунку: ").strip()
                
                # Перевірка на унікальність номера рахунку
                try:
                    find_account_by_number(accounts, acc_num)
                    print("Помилка! Рахунок з таким номером уже існує.")
                    continue
                except AccountNotFoundError:
                    pass
                
                balance = get_float_input("Введіть початковий баланс рахунку: ")
                
                new_acc = BankAccount(client_name=name, account_number=acc_num, balance=balance)
                accounts.append(new_acc)
                print(f"Рахунок {acc_num} успішно створено для клієнта {name}.")

            elif choice == "8":
                print("Дякуємо, що скористалися послугами нашого банку. До побачення!")
                sys.exit(0)

            else:
                print("Некоректний вибір. Спробуйте ще раз (1-8).")

        except BankSystemError as e:
            print(f"\n[Банківська помилка] {e}")
        except ValueError as e:
            print(f"\n[Помилка валідації даних] {e}")
        except Exception as e:
            print(f"\n[Непередбачена помилка] {e}")


def main() -> None:
    """
    Запуск застосунку.
    """
    run()


if __name__ == "__main__":
    main()
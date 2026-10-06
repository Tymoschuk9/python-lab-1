# src/bank_system/exceptions.py

class BankError(Exception):
    """Базовий клас для всіх виняткових ситуацій банківської системи."""
    pass


class InsufficientFundsError(BankError):
    """Виникає, якщо на рахунку недостатньо коштів для списання."""
    pass


class InvalidAmountError(BankError):
    """Виникає при введенні некоректної суми (наприклад, від'ємної)."""
    pass


class AccountNotFoundError(BankError):
    """Виникає, якщо рахунок із вказаним номером не знайдено."""
    pass


# src/bank_system/models.py

from dataclasses import dataclass
from bank_system.exceptions import InsufficientFundsError, InvalidAmountError


@dataclass
class Account:
    """Модель банківського рахунку."""
    client_name: str
    account_number: str
    balance: float

    def deposit(self, amount: float) -> None:
        """Поповнення рахунку на вказану суму."""
        if amount <= 0:
            raise InvalidAmountError("Сума поповнення має бути більшою за нуль.")
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        """Списання коштів з рахунку."""
        if amount <= 0:
            raise InvalidAmountError("Сума списання має бути більшою за нуль.")
        if self.balance - amount < 0:
            raise InsufficientFundsError(
                f"Операція відхилена. Недостатньо коштів. "
                f"Поточний баланс: {self.balance:.2f} грн. Спроба списання: {amount:.2f} грн."
            )
        self.balance -= amount


# src/bank_system/services.py

from bank_system.models import Account
from bank_system.exceptions import AccountNotFoundError, InvalidAmountError

# Константа мінімального початкового внеску
MIN_INITIAL_DEPOSIT = 50.0


class BankService:
    """Клас для управління бізнес-логікою банківської системи."""

    def __init__(self) -> None:
        self._accounts: list[Account] = []

    def create_account(self, name: str, number: str, initial_deposit: float) -> Account:
        """Створення нового унікального рахунку."""
        if not name.strip():
            raise ValueError("Ім'я клієнта не може бути порожнім.")
        if not number.strip():
            raise ValueError("Номер рахунку не може бути порожнім.")
        if initial_deposit < MIN_INITIAL_DEPOSIT:
            raise InvalidAmountError(
                f"Початковий внесок повинен бути не менше {MIN_INITIAL_DEPOSIT:.2f} грн."
            )
        
        # Перевірка на унікальність номера рахунку
        if self.find_account_silent(number) is not None:
            raise ValueError(f"Рахунок з номером {number} вже зареєстровано.")

        new_account = Account(client_name=name.strip(), account_number=number.strip(), balance=initial_deposit)
        self._accounts.append(new_account)
        return new_account

    def find_account_silent(self, number: str) -> Account | None:
        """Пошук рахунку без генерації винятку (повертає None, якщо не знайдено)."""
        for account in self._accounts:
            if account.account_number == number:
                return account
        return None

    def find_account(self, number: str) -> Account:
        """Пошук рахунку із генерацією винятку AccountNotFoundError."""
        account = self.find_account_silent(number)
        if account is None:
            raise AccountNotFoundError(f"Рахунок з номером '{number}' не знайдено.")
        return account

    def search_by_client_name(self, query: str) -> list[Account]:
        """Пошук рахунків за частиною імені власника (case-insensitive)."""
        cleaned_query = query.strip().lower()
        if not cleaned_query:
            return []
        return [
            acc for acc in self._accounts 
            if cleaned_query in acc.client_name.lower()
        ]

    def get_total_bank_funds(self) -> float:
        """Обчислення загальної суми коштів у банку."""
        return sum(account.balance for account in self._accounts)

    def get_all_accounts(self, sort_by_balance: bool = False) -> list[Account]:
        """Отримання всіх рахунків (з можливістю сортування за балансом)."""
        if sort_by_balance:
            return sorted(self._accounts, key=lambda acc: acc.balance, reverse=True)
        return sorted(self._accounts, key=lambda acc: acc.client_name)


# src/bank_system/main.py

import sys
from bank_system.services import BankService, MIN_INITIAL_DEPOSIT
from bank_system.exceptions import BankError


def get_float_input(prompt: str) -> float:
    """Функція безпечного зчитування дійсного числа з консолі."""
    while True:
        try:
            val = input(prompt).strip()
            return float(val)
        except ValueError:
            print("Помилка введення: будь ласка, введіть коректне число.")


def print_menu() -> None:
    """Вивід консольного меню інтерфейсу."""
    print("\n" + "=" * 50)
    print("         СИСТЕМА БАНКІВСЬКИХ РАХУНКІВ")
    print("=" * 50)
    print("1. Переглянути всі рахунки")
    print("2. Створити новий рахунок")
    print("3. Поповнити рахунок")
    print("4. Списати кошти з рахунку")
    print("5. Перевірити баланс за номером рахунку")
    print("6. Пошук рахунків за ім'ям клієнта")
    print("7. Показати загальний капітал банку")
    print("8. Вихід з програми")
    print("=" * 50)


def seed_demo_data(service: BankService) -> None:
    """Заповнення системи тестовими даними для демонстрації."""
    try:
        service.create_account("Олександр Шевченко", "UA450122", 15200.50)
        service.create_account("Марія Коваленко", "UA890344", 450.00)
        service.create_account("Дмитро Мельник", "UA230455", 73500.00)
        service.create_account("Анна Бойко", "UA120566", 1200.00)
    except Exception as e:
        print(f"Помилка завантаження демо-даних: {e}")


def main() -> None:
    service = BankService()
    seed_demo_data(service)

    while True:
        print_menu()
        choice = input("Оберіть пункт меню (1-8): ").strip()

        if choice == "1":
            print("\nОберіть сортування:")
            print("a. За ім'ям власника (алфавітний порядок)")
            print("b. За балансом (від більшого до меншого)")
            sort_choice = input("Ваш вибір (a/b): ").strip().lower()
            
            sort_by_balance = (sort_choice == "b")
            accounts = service.get_all_accounts(sort_by_balance=sort_by_balance)
            
            if not accounts:
                print("У системі немає зареєстрованих рахунків.")
                continue

            print("\n" + "-" * 65)
            print(f"{'Клієнт':<25} | {'Номер рахунку':<15} | {'Баланс (грн)':<18}")
            print("-" * 65)
            for acc in accounts:
                print(f"{acc.client_name:<25} | {acc.account_number:<15} | {acc.balance:<18.2f}")
            print("-" * 65)

        elif choice == "2":
            print("\n--- СТВОРЕННЯ НОВОГО РАХУНКУ ---")
            name = input("Ім'я клієнта: ").strip()
            number = input("Номер рахунку (наприклад, UAXXXXXX): ").strip()
            print(f"Примітка: мінімальний початковий внесок становить {MIN_INITIAL_DEPOSIT:.2f} грн.")
            initial_deposit = get_float_input("Введіть початковий баланс: ")

            try:
                acc = service.create_account(name, number, initial_deposit)
                print(f"\nРахунок успішно активовано! Власник: {acc.client_name}, Баланс: {acc.balance:.2f} грн.")
            except (ValueError, BankError) as e:
                print(f"\nПомилка створення рахунку: {e}")

        elif choice == "3":
            print("\n--- ПОПОВНЕННЯ РАХУНКУ ---")
            number = input("Введіть номер рахунку: ").strip()
            try:
                account = service.find_account(number)
                amount = get_float_input("Введіть суму поповнення: ")
                account.deposit(amount)
                print(f"Рахунок успішно поповнено. Новий баланс рахунку {number}: {account.balance:.2f} грн.")
            except BankError as e:
                print(f"\nПомилка транзакції: {e}")

        elif choice == "4":
            print("\n--- СПИСАННЯ КОШТІВ ---")
            number = input("Введіть номер рахунку: ").strip()
            try:
                account = service.find_account(number)
                amount = get_float_input("Введіть суму для зняття: ")
                account.withdraw(amount)
                print(f"Операція успішна. Новий баланс рахунку {number}: {account.balance:.2f} грн.")
            except BankError as e:
                print(f"\nПомилка транзакції: {e}")

        elif choice == "5":
            print("\n--- ПЕРЕВІРКА БАЛАНСУ ---")
            number = input("Введіть номер рахунку: ").strip()
            try:
                account = service.find_account(number)
                print(f"Власник рахунку: {account.client_name}")
                print(f"Поточний баланс: {account.balance:.2f} грн.")
            except BankError as e:
                print(f"\nПомилка: {e}")

        elif choice == "6":
            print("\n--- ПОШУК РАХУНКІВ ---")
            query = input("Введіть ім'я власника (або його частину): ").strip()
            results = service.search_by_client_name(query)
            if not results:
                print("Рахунків за вказаними критеріями не знайдено.")
            else:
                print(f"\nЗнайдено рахунків: {len(results)}")
                print("-" * 65)
                for acc in results:
                    print(f"- {acc.client_name} (Рахунок: {acc.account_number}) | Баланс: {acc.balance:.2f} грн.")
                print("-" * 65)

        elif choice == "7":
            total = service.get_total_bank_funds()
            print(f"\nЗагальна сума коштів на всіх рахунках банку: {total:.2f} грн.")

        elif choice == "8":
            print("\nДякуємо, що користуєтесь нашими банківськими послугами. До зустрічі!")
            sys.exit(0)

        else:
            print("\nПомилка: Невідомий пункт меню. Будь ласка, оберіть значення від 1 до 8.")


if __name__ == "__main__":
    main()


# src/bank_system/__init__.py

"""Пакет системи банківських рахунків."""

__version__ = "0.1.0"
from dataclasses import dataclass
from typing import List, Optional


class BankSystemError(Exception):
    """Базовий клас для винятків у системі банківських рахунків."""
    pass


class InsufficientFundsError(BankSystemError):
    """Виняток, що виникає при спробі зняти суму, яка перевищує баланс."""
    pass


class InvalidAmountError(BankSystemError):
    """Виняток, що виникає при введенні некоректної суми (меншої або рівної нулю)."""
    pass


class AccountNotFoundError(BankSystemError):
    """Виняток, що виникає, коли рахунок не знайдено в системі."""
    pass


class AccountAlreadyExistsError(BankSystemError):
    """Виняток, що виникає при спробі створити рахунок з уже існуючим номером."""
    pass


@dataclass
class BankAccount:
    """Модель даних, що представляє банківський рахунок клієнта."""
    client_name: str
    account_number: str
    balance: float = 0.0

    def deposit(self, amount: float) -> None:
        """Поповнення рахунку на вказану суму."""
        if amount <= 0:
            raise InvalidAmountError("Сума поповнення має бути більшою за нуль.")
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        """Списання коштів з рахунку. Запобігає від'ємному балансу."""
        if amount <= 0:
            raise InvalidAmountError("Сума списання має бути більшою за нуль.")
        if self.balance - amount < 0:
            raise InsufficientFundsError(
                f"Недостатньо коштів. Поточний баланс: {self.balance:.2f} грн. "
                f"Спроба зняти: {amount:.2f} грн."
            )
        self.balance -= amount


def find_account(accounts: List[BankAccount], account_number: str) -> BankAccount:
    """
    Пошук рахунку за його унікальним номером.
    Повертає об'єкт рахунку або генерує помилку AccountNotFoundError.
    """
    cleaned_number = account_number.strip().upper()
    for acc in accounts:
        if acc.account_number.upper() == cleaned_number:
            return acc
    raise AccountNotFoundError(f"Рахунок з номером {account_number} не знайдено.")


def calculate_total_funds(accounts: List[BankAccount]) -> float:
    """Обчислення загальної суми коштів на всіх рахунках банку."""
    return sum(acc.balance for acc in accounts)


def add_new_account(accounts: List[BankAccount], name: str, number: str, initial_balance: float) -> BankAccount:
    """
    Створення та додавання нового рахунку до загальної бази даних.
    Перевіряє унікальність номера рахунку та коректність початкового балансу.
    """
    if not name.strip():
        raise InvalidAmountError("Ім'я клієнта не може бути порожнім.")
    if not number.strip():
        raise InvalidAmountError("Номер рахунку не може бути порожнім.")
    if initial_balance < 0:
        raise InvalidAmountError("Початковий баланс не може бути від'ємним.")
    
    cleaned_number = number.strip().upper()
    for acc in accounts:
        if acc.account_number.upper() == cleaned_number:
            raise AccountAlreadyExistsError(f"Рахунок з номером {number} вже існує.")
            
    new_acc = BankAccount(client_name=name.strip(), account_number=cleaned_number, balance=initial_balance)
    accounts.append(new_acc)
    return new_acc


def create_demo_accounts() -> List[BankAccount]:
    """Створення демонстраційного набору даних для перевірки роботи системи."""
    return [
        BankAccount("Олександр Петренко", "UA8932203300000026001234561", 15250.50),
        BankAccount("Марія Коваленко", "UA5630201100000026009876542", 4800.00),
        BankAccount("Дмитро Шевченко", "UA1230984400000026001112223", 350.75),
        BankAccount("Анна Лисенко", "UA4455667700000026009998887", 120500.00)
    ]


def get_float_input(prompt: str) -> float:
    """Безпечне зчитування дійсного числа з консолі з валідацією."""
    while True:
        try:
            val = float(input(prompt).strip())
            return val
        except ValueError:
            print("Помилка введення! Будь ласка, введіть коректне число (наприклад, 150.50).")


def print_menu() -> None:
    """Вивід головного інтерактивного меню програми."""
    print("\n" + "=" * 50)
    print("      СИСТЕМА УПРАВЛІННЯ БАНКІВСЬКИМИ РАХУНКАМИ")
    print("=" * 50)
    print("1. Показати список усіх рахунків")
    print("2. Знайти рахунок за номером")
    print("3. Перевірити поточний баланс рахунку")
    print("4. Поповнити рахунок (Deposit)")
    print("5. Списати кошти з рахунку (Withdraw)")
    print("6. Розрахувати загальну суму коштів у банку")
    print("7. Відкрити новий банківський рахунок")
    print("8. Вийти з програми")
    print("=" * 50)


def main() -> None:
    """Головна функція запуску консольного інтерфейсу застосунку."""
    accounts = create_demo_accounts()
    print("Систему успішно ініціалізовано демонстраційними даними.")

    while True:
        print_menu()
        choice = input("Оберіть пункт меню (1-8): ").strip()

        try:
            if choice == "1":
                print("\n--- Список зареєстрованих рахунків ---")
                if not accounts:
                    print("База даних рахунків порожня.")
                for acc in accounts:
                    print(f"Клієнт: {acc.client_name:<22} | Рахунок: {acc.account_number:<27} | Баланс: {acc.balance:12.2f} грн")
            
            elif choice == "2":
                num = input("Введіть номер рахунку для пошуку: ").strip()
                acc = find_account(accounts, num)
                print("\n--- Інформація про рахунок ---")
                print(f"Власник рахунку: {acc.client_name}")
                print(f"Номер рахунку:   {acc.account_number}")
                print(f"Поточний баланс: {acc.balance:.2f} грн")

            elif choice == "3":
                num = input("Введіть номер рахунку для перевірки балансу: ").strip()
                acc = find_account(accounts, num)
                print(f"\nПоточний баланс рахунку {acc.account_number} ({acc.client_name}): {acc.balance:.2f} грн")

            elif choice == "4":
                num = input("Введіть номер рахунку для поповнення: ").strip()
                acc = find_account(accounts, num)
                amount = get_float_input("Введіть суму поповнення (грн): ")
                acc.deposit(amount)
                print(f"\nРахунок успішно поповнено на {amount:.2f} грн.")
                print(f"Новий баланс рахунку {acc.account_number}: {acc.balance:.2f} грн.")

            elif choice == "5":
                num = input("Введіть номер рахунку для списання коштів: ").strip()
                acc = find_account(accounts, num)
                amount = get_float_input("Введіть суму списання (грн): ")
                acc.withdraw(amount)
                print(f"\nЗ рахунку успішно списано {amount:.2f} грн.")
                print(f"Новий баланс рахунку {acc.account_number}: {acc.balance:.2f} грн.")

            elif choice == "6":
                total = calculate_total_funds(accounts)
                print(f"\nЗагальна сума коштів на всіх рахунках банку: {total:.2f} грн.")

            elif choice == "7":
                print("\n--- Реєстрація нового рахунку ---")
                name = input("Введіть ім'я та прізвище клієнта: ").strip()
                number = input("Введіть унікальний номер рахунку (наприклад, UA...): ").strip()
                initial_balance = get_float_input("Введіть початковий баланс (грн): ")
                
                new_acc = add_new_account(accounts, name, number, initial_balance)
                print(f"\nРахунок успішно створено!")
                print(f"Клієнт: {new_acc.client_name} | Рахунок: {new_acc.account_number} | Баланс: {new_acc.balance:.2f} грн.")

            elif choice == "8":
                print("\nДякуємо, що скористалися нашою системою. До побачення!")
                break
            
            else:
                print("Некоректний вибір. Будь ласка, введіть цифру від 1 до 8.")

        except BankSystemError as e:
            print(f"\n[БАНКІВСЬКА ПОМИЛКА] {e}")
        except Exception as e:
            print(f"\n[КРИТИЧНА ПОМИЛКА] Щось пішло не так: {e}")


if __name__ == "__main__":
    main()
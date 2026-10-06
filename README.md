<div align="center">
  <b>МІНІСТЕРСТВО ОСВІТИ І НАУКИ УКРАЇНИ</b><br>
  <b>ЛЬВІВСЬКИЙ НАЦІОНАЛЬНИЙ УНІВЕРСИТЕТ ІМЕНІ ІВАНА ФРАНКА</b><br>
  <b>Факультет прикладної математики та інформатики</b><br>
  <b>Кафедра програмування</b><br><br><br><br>

  <h1>ЗВІТ</h1>
  <h3>про виконання лабораторної роботи №1<br>з навчальної дисципліни «Професійний Python»</h3><br>
  
  <b>Тема: «Організація професійного Python-проєкту та Git»</b><br>
  <b>Варіант: «3»</b><br><br><br><br>
</div>

<div align="right">
  <b>Виконав:</b><br>
  студент групи ФеП-31<br>
  <b>Тимощук Владислав</b><br><br>
  
  <b>Перевірив:</b><br>
  доцент Куньо Іван Михайлович<br><br><br>
</div>

<div align="center">
  Львів — 2026
</div>

---

# Мета

Ознайомитися з основними принципами побудови професійних Python-проєктів відповідно до сучасних стандартів розробки. Навчитись створювати ізольовані віртуальні середовища (`venv`), структурувати код за шаблоном `src-layout`, розділяти програму на окремі модулі (слабке пов'язання та сильна зв'язність), використовувати декларації типів (Type Hints), конфігурувати метадані проєкту за допомогою `pyproject.toml`, налаштовувати ігнорування системних файлів через `.gitignore` та супроводжувати репозиторій професійною документацією в `README.md`. Також робота спрямована на закріплення навичок роботи з розподіленою системою контролю версій Git для фіксації логічних етапів розробки.

---

## Опис алгоритму

Для реалізації індивідуального варіанта №4 **«Система банківських рахунків»** було розроблено консольний застосунок, побудований на принципах чистої архітектури та об'єктно-орієнтованого моделювання.

### 1. Архітектурне структурування та бізнес-логіка
Програма розподілена на три логічні шари відповідно до принципу `src-layout`:
*   **Шар даних та моделей (`src/bank_system/models.py`):**
    Ключовим об'єктом є дата-клас `BankAccount`, який інкапсулює стан окремого рахунку (ім'я клієнта `client_name`, унікальний номер `account_number` та поточний баланс `balance`). Всередині класу реалізовані атомарні операції зміни стану: метод `deposit` (поповнення балансу з попередньою перевіркою позитивного значення суми) та метод `withdraw` (безпечне списання коштів із перевіркою наявності достатньої суми для запобігання виникненню від'ємного балансу).
*   **Шар бізнес-логіки та сервісів (`src/bank_system/services.py`):**
    Сервісний шар містить чисті функції для маніпулювання колекцією об'єктів рахунків:
    *   `find_account` — пошук конкретного рахунку у реєстрі за унікальним номером. Реалізовано нормалізацію рядків та обробку ситуації відсутності результату шляхом викидання спеціалізованого винятку.
    *   `calculate_total_funds` — агрегуюча функція для підрахунку сумарного фінансового обсягу банку.
    *   `add_new_account` — функція реєстрації нового користувача, яка забезпечує унікальність номерів рахунків у системі (бізнес-валідація).
*   **Шар взаємодії з користувачем та точка входу (`src/bank_system/main.py`):**
    Керує життєвим циклом програми. Забезпечує інтерактивне консольне меню (Menu-driven interface), валідацію користувацького введення (захист від введення текстових значень замість чисел, обробка порожніх рядків), а також перехоплення та централізовану обробку кастомних винятків.

### 2. Спеціалізовані класи винятків
Створено ієрархію винятків для детального інформування про логічні помилки під час роботи програми:
*   `BankSystemError` (базовий виняток)
    *   `InsufficientFundsError` (недостатньо коштів на рахунку)
    *   `InvalidAmountError` (некоректна сума транзакції)
    *   `AccountNotFoundError` (рахунок не знайдено)
    *   `AccountAlreadyExistsError` (спроба дублювання номера рахунку)

---

### Структура проєкту на диску

Застосування `src-layout` є сучасним стандартом у Python-спільноті (рекомендований PyPA), оскільки він гарантує, що код може бути імпортований та протестований лише після його повноцінного встановлення в середовище (локально або в editable mode). Це запобігає випадковим імпортам локальних файлів з поточної робочої директорії.

```text
bank_system/
│
├── .gitignore
├── pyproject.toml
├── README.md
│
├── src/
│   └── bank_system/
│       ├── __init__.py
│       ├── main.py
│       ├── models.py
│       └── services.py
│
└── tests/
```

---

### Текст окремих файлів проєкту

#### Файл `src/bank_system/__init__.py`
```python
"""Bank Account Management System package."""

__version__ = "0.1.0"
```

#### Файл `src/bank_system/models.py`
```python
from dataclasses import dataclass
from bank_system.exceptions import InvalidAmountError, InsufficientFundsError

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
```

#### Файл `src/bank_system/services.py`
```python
from typing import List
from bank_system.models import BankAccount
from bank_system.exceptions import AccountNotFoundError, AccountAlreadyExistsError, InvalidAmountError

def find_account(accounts: List[BankAccount], account_number: str) -> BankAccount:
    """Пошук рахунку за його унікальним номером."""
    cleaned_number = account_number.strip().upper()
    for acc in accounts:
        if acc.account_number.upper() == cleaned_number:
            return acc
    raise AccountNotFoundError(f"Рахунок з номером {account_number} не знайдено.")

def calculate_total_funds(accounts: List[BankAccount]) -> float:
    """Обчислення загальної суми коштів на всіх рахунках банку."""
    return sum(acc.balance for acc in accounts)

def add_new_account(accounts: List[BankAccount], name: str, number: str, initial_balance: float) -> BankAccount:
    """Створення та додавання нового рахунку до реєстру."""
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
```

#### Файл `src/bank_system/exceptions.py`
```python
class BankSystemError(Exception):
    """Базовий клас для винятків у системі банківських рахунків."""
    pass

class InsufficientFundsError(BankSystemError):
    """Виняток для недостатнього балансу."""
    pass

class InvalidAmountError(BankSystemError):
    """Виняток для некоректної суми транзакції."""
    pass

class AccountNotFoundError(BankSystemError):
    """Виняток, коли рахунок не знайдено."""
    pass

class AccountAlreadyExistsError(BankSystemError):
    """Виняток, коли номер рахунку вже зайнято."""
    pass
```

#### Файл `src/bank_system/main.py`
```python
import sys
from typing import List
from bank_system.models import BankAccount
from bank_system.services import find_account, calculate_total_funds, add_new_account
from bank_system.exceptions import BankSystemError

def create_demo_accounts() -> List[BankAccount]:
    """Ініціалізація демонстраційних даних."""
    return [
        BankAccount("Олександр Петренко", "UA8932203300000026001234561", 15250.50),
        BankAccount("Марія Коваленко", "UA5630201100000026009876542", 4800.00),
        BankAccount("Дмитро Шевченко", "UA1230984400000026001112223", 350.75),
        BankAccount("Анна Лисенко", "UA4455667700000026009998887", 120500.00)
    ]

def get_float_input(prompt: str) -> float:
    """Безпечне зчитування дійсного числа з консолі."""
    while True:
        try:
            val = float(input(prompt).strip())
            return val
        except ValueError:
            print("Помилка введення! Будь ласка, введіть число (наприклад, 150.50).")

def print_menu() -> None:
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
    accounts = create_demo_accounts()
    print("Систему успішно ініціалізовано.")

    while True:
        print_menu()
        choice = input("Оберіть пункт меню (1-8): ").strip()

        try:
            if choice == "1":
                print("\n--- Список зареєстрованих рахунків ---")
                for acc in accounts:
                    print(f"Клієнт: {acc.client_name:<22} | Рахунок: {acc.account_number:<27} | Баланс: {acc.balance:12.2f} грн")
            
            elif choice == "2":
                num = input("Введіть номер рахунку: ").strip()
                acc = find_account(accounts, num)
                print(f"\nЗнайдено рахунок:\nВласник: {acc.client_name}\nНомер: {acc.account_number}\nБаланс: {acc.balance:.2f} грн")

            elif choice == "3":
                num = input("Введіть номер рахунку: ").strip()
                acc = find_account(accounts, num)
                print(f"\nБаланс рахунку {acc.account_number}: {acc.balance:.2f} грн")

            elif choice == "4":
                num = input("Введіть номер рахунку: ").strip()
                acc = find_account(accounts, num)
                amount = get_float_input("Введіть суму поповнення (грн): ")
                acc.deposit(amount)
                print(f"\nРахунок успішно поповнено. Новий баланс: {acc.balance:.2f} грн.")

            elif choice == "5":
                num = input("Введіть номер рахунку: ").strip()
                acc = find_account(accounts, num)
                amount = get_float_input("Введіть суму списання (грн): ")
                acc.withdraw(amount)
                print(f"\nЗ рахунку успішно списано кошти. Новий баланс: {acc.balance:.2f} грн.")

            elif choice == "6":
                total = calculate_total_funds(accounts)
                print(f"\nЗагальна сума коштів на всіх рахунках банку: {total:.2f} грн.")

            elif choice == "7":
                name = input("Введіть ім'я та прізвище клієнта: ").strip()
                number = input("Введіть номер рахунку (наприклад, UA...): ").strip()
                initial_balance = get_float_input("Введіть початковий баланс (грн): ")
                new_acc = add_new_account(accounts, name, number, initial_balance)
                print(f"\nРахунок успішно створено!")

            elif choice == "8":
                print("\nДо побачення!")
                break
            else:
                print("Некоректний вибір. Введіть цифру від 1 до 8.")
        except BankSystemError as e:
            print(f"\n[БАНКІВСЬКА ПОМИЛКА] {e}")
        except Exception as e:
            print(f"\n[КРИТИЧНА ПОМИЛКА] {e}")

if __name__ == "__main__":
    main()
```

---

### Конфігураційні файли проєкту

#### Файл `pyproject.toml`
Конфігураційний файл сумісний з сучасними стандартами розгортання Python-пакетів (PEP 517 / PEP 621) і використовує `setuptools` як складальну систему.
```toml
[build-system]
requires = ["setuptools>=70"]
build-backend = "setuptools.build_meta"

[project]
name = "bank-system"
version = "0.1.0"
description = "Professional Bank Account Management System built with Python"
readme = "README.md"
requires-python = ">=3.11"
authors = [
    { name = "Python Developer", email = "developer@bank.local" }
]
classifiers = [
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
    "Operating System :: OS Independent",
]

[project.scripts]
bank-system = "bank_system.main:main"
```

#### Файл `.gitignore`
Забезпечує ігнорування системних файлів, віртуальних середовищ, локальних налаштувань середовища розробки (IDE) та кешу компілятора Python.
```text
.venv/
__pycache__/
*.pyc
.pytest_cache/
.idea/
.vscode/
dist/
build/
*.egg-info/
.env
```

#### Файл `README.md`
```markdown
# Bank Account Management System

Консольний застосунок для управління банківськими рахунками, створений у межах лабораторної роботи №1 з дисципліни «Професійний Python».

## Особливості
- Побудовано за принципом **src-layout**.
- Інтерактивне консольне меню з валідацією введення.
- Надійна обробка логічних винятків (запобігання від'ємному балансу, дублюванню рахунків).
- Повне покриття Type Hints.

## Встановлення

1. Створіть та активуйте віртуальне середовище:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Для Linux/macOS
   .venv\Scripts\activate     # Для Windows
   ```

2. Встановіть застосунок в інтерактивному (editable) режимі:
   ```bash
   python -m pip install -e .
   ```

## Запуск програми

Запуск через модуль Python:
```bash
python -m bank_system.main
```
Або за допомогою автоматично створеного консольного скрипта:
```bash
bank-system
```
```

---

### Робота з Git

Ініціалізація та налаштування локального репозиторію відбувалися за наступним сценарієм (імітація виводів терміналу):

```bash
# 1. Ініціалізація репозиторію та додавання конфігурацій
git init
git add .gitignore pyproject.toml
git commit -m "Create project structure and core configuration files"

# 2. Додавання бізнес-моделей та сервісних функцій
git add src/bank_system/__init__.py src/bank_system/models.py src/bank_system/services.py src/bank_system/exceptions.py
git commit -m "Add BankAccount model, business logic services, and custom exceptions"

# 3. Додавання інтерфейсу взаємодії з користувачем та README.md
git add src/bank_system/main.py README.md
git commit -m "Add main CLI application, demo data initialization, and README documentation"
```

#### Результат виконання команди `git status`
```text
On branch main
nothing to commit, working tree clean
```

#### Результат виконання команди `git log --oneline`
```text
9d2f11a Add main CLI application, demo data initialization, and README documentation
4a382cf Add BankAccount model, business logic services, and custom exceptions
1f77d3b Create project structure and core configuration files
```

---

### Відповіді на контрольні запитання

1. **Що таке Python-проєкт?**  
   Це структурована сукупність вихідного коду, конфігураційних файлів, документації, тестів та залежностей, що утворюють єдину програмну систему чи пакет, готовий до розповсюдження та підтримки.
2. **Чим проєкт відрізняється від одного Python script?**  
   Проєкт є масштабованим і складається з багатьох модулів із розмежованою відповідальністю, має чіткі інструкції збирання (`pyproject.toml`), залежності та документацію, тоді як один скрипт є монолітним файлом для виконання простих або локальних завдань.
3. **Що таке Python module?**  
   Це окремий файл із розширенням `.py`, який містить визначення функцій, класів, змінних та виконуваний код, що може бути імпортований іншими модулями.
4. **Що таке Python package?**  
   Це каталог, який містить інші модулі та пакети, а також зазвичай містить файл `__init__.py` для позначення простору імен (namespace package).
5. **Для чого потрібний `__init__.py`?**  
   Він вказує інтерпретатору Python, що каталог є пакетом. У ньому також можна визначати експортований інтерфейс пакету (`__all__`), метадані пакета (`__version__`) та виконувати початкову ініціалізацію.
6. **Що таке `src-layout`?**  
   Це архітектурний шаблон організації коду, за якого всі вихідні файли пакетів розміщуються в окремому кореневому каталозі `src/`.
7. **Які переваги має `src-layout`?**  
   Він запобігає випадковому імпорту локального коду без його попереднього встановлення у середовище розробки, полегшує тестування і гарантує збіжність структури під час збирання дистрибутиву (`wheel`).
8. **Для чого використовується virtual environment?**  
   Для ізоляції залежностей та бібліотек конкретного проєкту від глобальної системи та інших проєктів, усуваючи конфлікти версій.
9. **Як створити `.venv`?**  
   За допомогою вбудованого модуля `venv`: `python -m venv .venv`.
10. **Як активувати virtual environment?**  
    У Windows: `.venv\Scripts\activate`, у Linux/macOS: `source .venv/bin/activate`.
11. **Для чого використовується `pip`?**  
    Це стандартна система керування пакетами в Python, яка дозволяє встановлювати, оновлювати та видаляти сторонні бібліотеки з репозиторію PyPI.
12. **Чому рекомендується `python -m pip`?**  
    Цей синтаксис гарантує, що `pip` буде запущено саме для тієї версії інтерпретатора Python, яка викликана, запобігаючи використанню системного `pip` замість віртуального середовища.
13. **Для чого потрібний `pyproject.toml`?**  
    Це єдиний уніфікований конфігураційний файл проєкту (PEP 518), який визначає складальну систему (build system), метадані проєкту, залежності та налаштування інструментів розробки.
14. **Що містить секція `[project]`?**  
    Метадані проєкту: ім'я, версію, опис, вимоги до версії Python, залежності, авторів, ліцензію та точки входу консольних скриптів.
15. **Що таке `editable installation`?**  
    Режим встановлення пакету (`pip install -e .`), за якого зміни у вихідному коді проєкту миттєво відображаються в середовищі розробки без необхідності повторного встановлення.
16. **Для чого використовується `if __name__ == "__main__"`?**  
    Ця конструкція гарантує, що блок коду під нею буде виконано лише при безпосередньому запуску цього файлу як скрипта, а не при його імпортуванні як модуля в інший файл.
17. **Що таке Git?**  
    Це розподілена система контролю версій, яка відстежує зміни у файлах проєкту, дозволяє працювати в командах, створювати гілки та повертатися до попередніх станів коду.
18. **Що таке repository?**  
    Сховище даних (локальне чи віддалене), де зберігається вся історія версій, метадані та поточний стан файлів проєкту під контролем Git.
19. **Що таке commit?**  
    Це знімок (snapshot) стану проєкту на певний момент часу, зафіксований в історії Git з унікальним хешем та описом змін.
20. **Для чого використовується `git status`?**  
    Для перегляду поточного стану робочої директорії: змінених, створених, видалених файлів та файлів, що готуються до коміту (staged).
21. **Для чого `git add`?**  
    Для додавання змін у файлах до індексу (staging area) перед фіксацією коммітом.
22. **Для чого `git commit`?**  
    Для збереження підготовлених змін з індексу в локальну історію репозиторію.
23. **Що показує `git log`?**  
    Хронологічний список комітів у поточному репозиторії з інформацією про авторів, дати та описи змін.
24. **Для чого потрібен `.gitignore`?**  
    Для визначення шаблонів шляхів та файлів, які система Git має ігнорувати і ніколи не додавати до репозиторію (наприклад, віртуальні середовища, паролі, кеші).
25. **Чому `.venv` не потрібно комітити?**  
    Оскільки віртуальне середовище містить системно-залежні бінарні файли та велику кількість сторонніх пакетів. Воно легко відтворюється на іншій машині за допомогою файлу конфігурації.
26. **Для чого потрібний README?**  
    Для ознайомлення користувачів та розробників з проєктом: його призначенням, вимогами, процесом встановлення, запуску та використання.
27. **Що таке type hints?**  
    Це статичні інструкції типів даних для змінних, параметрів функцій та значень, що повертаються, які полегшують аналіз коду IDE та статичними аналізаторами (наприклад, MyPy).
28. **Для чого програму розділяють на modules?**  
    Для спрощення навігації, покращення читабельності коду, запобігання дублюванню коду, забезпечення принципу модульності та полегшення тестування окремих компонентів.
29. **Що таке business logic?**  
    Це сукупність правил, алгоритмів та обмежень, які відображають логіку предметної області (наприклад, у банківській системі: правила розрахунку балансу, валідація унікальності рахунку).
30. **Чому потрібно відокремлювати application entry point від business logic?**  
    Щоб забезпечити незалежність ядра системи від способу взаємодії з користувачем (інтерфейсу). Це дозволяє легко змінити консольний інтерфейс на веб-додаток (API або GUI) без внесення змін у перевірені бізнес-алгоритми.

---

## Висновок

У ході виконання лабораторної роботи було успішно засвоєно навички створення професійного Python-проєкту від початкової ініціалізації до документування. Побудована за архітектурою `src-layout` система банківських рахунків наочно продемонструвала переваги низької зв'язності компонентів (Loose Coupling) завдяки чіткому поділу на моделі даних, сервіси бізнес-логіки та клієнтський консольний інтерфейс. Було опановано інструменти віртуального середовища `venv` та пакетного менеджера `pip`. Написання конфігураційного файлу `pyproject.toml` заклало фундамент для автоматизованого збирання пакунків. Робота з Git дозволила виробити дисципліну комітів для фіксації логічно завершених етапів розробки. Створений проєкт відповідає вимогам PEP 8 та готовий до подальшого розширення модулями тестування та інтеграції з базами даних.
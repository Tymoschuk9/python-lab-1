<div align="center">
  <b>МІНІСТЕРСТВО ОСВІТИ І НАУКИ УКРАЇНИ</b><br>
  <b>ЛЬВІВСЬКИЙ НАЦІОНАЛЬНИЙ УНІВЕРСИТЕТ ІМЕНІ ІВАНА ФРАНКА</b><br>
  <b>Факультет електроніки та комп'ютерних технологій</b><br>
  <b>Кафедра системного проєктування</b><br><br><br><br>

  <h1>ЗВІТ</h1>
  <h3>про виконання лабораторної роботи №1<br>з навчальної дисципліни «Професійний Python»</h3><br>
  
  <b>Тема: «Організація професійного Python-проєкту та Git»</b><br>
  <b>Варіант №3</b><br>
  <b>Варіант: 3</b><br><br><br><br>
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
Ознайомлення з принципами організації професійного Python-проєкту, опанування src-layout, роботи з virtual environment, Git та інструментами керування пакетами (pyproject.toml).

## Опис алгоритму (Варіант №3)

Проєкт «Інтернет-магазин» реалізовано з використанням модульної структури:
1. **models.py**: Містить клас `Product` (dataclass) для опису структури товару та обчислювану властивість для вартості залишків.
2. **services.py**: Містить бізнес-логіку: додавання товарів, фільтрація за категорією, пошук за назвою та визначення найдорожчого товару.
3. **main.py**: Точка входу, що демонструє роботу сервісів та взаємодію з даними.

### Реалізація основних компонентів:

**src/shop_manager/models.py**
```python
from dataclasses import dataclass

@dataclass
class Product:
    name: str
    category: str
    price: float
    quantity: int

    @property
    def total_value(self) -> float:
        return self.price * self.quantity
```

**src/shop_manager/services.py**
```python
from shop_manager.models import Product

def calculate_total_inventory_value(products: list[Product]) -> float:
    return sum(p.total_value for p in products)

def find_product(products: list[Product], name: str) -> Product | None:
    return next((p for p in products if p.name.lower() == name.lower()), None)

def filter_by_category(products: list[Product], category: str) -> list[Product]:
    return [p for p in products if p.category.lower() == category.lower()]

def get_most_expensive(products: list[Product]) -> Product | None:
    return max(products, key=lambda p: p.price, default=None)
```

**Файл pyproject.toml**
```toml
[build-system]
requires = ["setuptools>=70"]
build-backend = "setuptools.build_meta"

[project]
name = "shop-manager"
version = "0.1.0"
description = "Internet shop inventory management"
requires-python = ">=3.11"

[project.scripts]
shop-manager = "shop_manager.main:main"
```

## Висновок
У ході лабораторної роботи було створено структурований Python-проєкт з використанням `src-layout`. Програма розділена на модулі, що забезпечує чітке відокремлення даних від бізнес-логіки. Використання Git дозволило відстежити етапи розробки, а `pyproject.toml` та віртуальне середовище забезпечили ізоляцію залежностей та можливість інсталяції проєкту в режимі розробки. Отримані навички є базовими для подальшої професійної роботи над складнішими програмними продуктами.
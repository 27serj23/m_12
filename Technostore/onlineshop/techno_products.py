#!/usr/bin/env python
import os
import django
import random
import argparse
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlineshop.settings')
django.setup()

from store.models import Category, Brand, Tag, Product

fake_ru = Faker('ru_RU')
fake_en = Faker('en_US')

# ---------- Предопределённые данные (без фабрик) ----------
TECH_CATEGORIES = [
    'Ноутбуки', 'Смартфоны', 'Наушники', 'Планшеты',
    'Мониторы', 'Клавиатуры', 'Компьютерные мыши', 'Колонки'
]

TECH_BRANDS = [
    {'name': 'Apple', 'country': 'США'},
    {'name': 'Samsung', 'country': 'Южная Корея'},
    {'name': 'Sony', 'country': 'Япония'},
    {'name': 'Xiaomi', 'country': 'Китай'},
    {'name': 'Dell', 'country': 'США'},
    {'name': 'HP', 'country': 'США'},
    {'name': 'Lenovo', 'country': 'Китай'},
    {'name': 'Asus', 'country': 'Тайвань'},
    {'name': 'Acer', 'country': 'Тайвань'},
    {'name': 'Microsoft', 'country': 'США'},
    {'name': 'Logitech', 'country': 'Швейцария'},
    {'name': 'JBL', 'country': 'США'},
    {'name': 'Beats', 'country': 'США'},
    {'name': 'Razer', 'country': 'США'},
    {'name': 'Corsair', 'country': 'США'},
]

TECH_TAGS = [
    'новинка', 'хит продаж', 'акция', 'распродажа',
    'игровой', 'для работы', 'бюджетный', 'премиум',
    'беспроводной', 'Bluetooth', 'USB-C', 'механический',
    'OLED', '4K', 'Retina', 'шумоподавление',
]


# ---------- Очистка ----------
def clear_products():
    count = Product.objects.count()
    Product.objects.all().delete()
    print(f"🗑️ Удалено продуктов: {count}")


def clear_all():
    print("🗑️ Полная очистка БД...")
    prod_count = Product.objects.count()
    tag_count = Tag.objects.count()
    brand_count = Brand.objects.count()
    cat_count = Category.objects.count()

    Product.objects.all().delete()
    Tag.objects.all().delete()
    Brand.objects.all().delete()
    Category.objects.all().delete()

    print(f"   - Продукты: {prod_count}")
    print(f"   - Теги: {tag_count}")
    print(f"   - Бренды: {brand_count}")
    print(f"   - Категории: {cat_count}")
    print("✅ База данных очищена.")


# ---------- Создание базовых объектов ----------
def create_categories():
    created = 0
    for name in TECH_CATEGORIES:
        _, flag = Category.objects.get_or_create(name=name)
        if flag:
            created += 1
    print(f"✅ Категории: создано {created}, всего {Category.objects.count()}")
    return Category.objects.all()


def create_brands():
    created = 0
    for b in TECH_BRANDS:
        _, flag = Brand.objects.get_or_create(
            name=b['name'],
            defaults={'country_of_origin': b['country']}
        )
        if flag:
            created += 1
    print(f"✅ Бренды: создано {created}, всего {Brand.objects.count()}")
    return Brand.objects.all()


def create_tags():
    created = 0
    for name in TECH_TAGS:
        _, flag = Tag.objects.get_or_create(name=name)
        if flag:
            created += 1
    print(f"✅ Теги: создано {created}, всего {Tag.objects.count()}")
    return Tag.objects.all()


# ---------- Генерация продуктов (без фабрик!) ----------
def generate_products(count=50):
    categories = list(Category.objects.all())
    brands = list(Brand.objects.all())
    tags = list(Tag.objects.all())

    if not categories or not brands or not tags:
        print("❌ Не хватает базовых данных. Сначала выполните создание категорий/брендов/тегов.")
        return []

    products = []
    for i in range(count):
        category = random.choice(categories)
        brand = random.choice(brands)

        # Генерация имени в зависимости от категории
        cat_name = category.name.lower()
        if 'ноутбук' in cat_name:
            name = f"{random.choice(['MacBook', 'XPS', 'ThinkPad', 'ROG'])} {fake_en.bothify(text='??###')}"
        elif 'смартфон' in cat_name:
            name = f"{random.choice(['iPhone', 'Galaxy', 'Xiaomi'])} {fake_en.numerify(text='##')}"
        elif 'наушник' in cat_name:
            name = f"{random.choice(['AirPods', 'WH-1000XM', 'Galaxy Buds'])} {fake_en.numerify(text='##')}"
        elif 'планшет' in cat_name:
            name = f"{random.choice(['iPad', 'Galaxy Tab', 'Surface'])} {fake_en.bothify(text='?###')}"
        elif 'монитор' in cat_name:
            name = f"{random.choice(['UltraSharp', 'Predator', 'ROG'])} {fake_en.numerify(text='##')}\""
        elif 'клавиатур' in cat_name:
            name = f"{random.choice(['G915', 'K70', 'BlackWidow'])} {fake_en.bothify(text='??##')}"
        elif 'мыш' in cat_name:
            name = f"{random.choice(['G502', 'DeathAdder', 'MX Master'])} {fake_en.bothify(text='??##')}"
        elif 'колонк' in cat_name:
            name = f"{random.choice(['JBL Flip', 'Sony SRS', 'Bose'])} {fake_en.numerify(text='##')}"
        else:
            name = f"{fake_en.company()} {fake_en.bothify(text='??##')}"

        price = round(random.uniform(1000, 200000) / 100) * 100
        stock = random.randint(0, 50)

        # Создаём продукт напрямую, без фабрики
        product = Product.objects.create(
            name=name,
            price=price,
            stock=stock,
            category=category,
            brand=brand,
        )
        # Добавляем от 1 до 3 случайных тегов ИЗ ПРЕДОПРЕДЕЛЁННОГО СПИСКА
        selected_tags = random.sample(tags, random.randint(1, min(3, len(tags))))
        product.tags.set(selected_tags)

        products.append(product)

        if (i + 1) % 10 == 0:
            print(f"  ... создано {i + 1} продуктов")

    return products


# ---------- Главная функция ----------
def main():
    parser = argparse.ArgumentParser(description='Генерация техно-товаров для TechStore')
    parser.add_argument('--clear', action='store_true', help='Удалить только продукты перед генерацией')
    parser.add_argument('--clear-all', action='store_true',
                        help='Полностью очистить БД (продукты, теги, бренды, категории)')
    parser.add_argument('--count', type=int, default=50, help='Количество продуктов (по умолчанию 50)')
    args = parser.parse_args()

    print("🚀 Запуск генерации техно-продуктов для TechStore")
    print("-" * 50)

    if args.clear_all:
        clear_all()
    elif args.clear:
        clear_products()

    # Создаём базовые сущности (если их нет)
    create_categories()
    create_brands()
    create_tags()

    print(f"\n📦 Генерация продуктов ({args.count} шт.):")
    products = generate_products(args.count)
    print(f"\n✅ Создано {len(products)} продуктов")

    print("\n📊 Статистика после генерации:")
    print(f"  Категории: {Category.objects.count()}")
    print(f"  Бренды:    {Brand.objects.count()}")
    print(f"  Теги:      {Tag.objects.count()} (из них предопределённых: {len(TECH_TAGS)})")
    print(f"  Продукты:  {Product.objects.count()}")
    print("\n🎉 Готово!")


if __name__ == "__main__":
    main()
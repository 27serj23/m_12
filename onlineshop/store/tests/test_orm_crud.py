# store/tests/test_orm_crud.py
from django.test import TestCase
from django.db import connection
from decimal import Decimal
from ..models import Product, Category, Brand, Tag
from ..factories import CategoryFactory, BrandFactory


class ORMCRUDTest(TestCase):
    """
    Тесты для операций добавления и удаления объектов через ORM.
    Проверка выполняется прямыми SQL-запросами к БД (PostgreSQL).
    """

    def test_add_product(self):
        """Добавление товара через ORM и проверка через SQL."""
        category = CategoryFactory(name="Electronics")
        brand = BrandFactory(name="TestBrand", country_of_origin="TestCountry")

        product = Product.objects.create(
            name="Test Product",
            price=Decimal("199.99"),
            category=category,
            brand=brand,
            stock=10
        )

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, price, category_id, brand_id, stock "
                "FROM store_product WHERE id = %s",
                [product.id]
            )
            row = cursor.fetchone()

        self.assertIsNotNone(row, "Товар не найден в БД")
        self.assertEqual(row[1], "Test Product")
        self.assertEqual(row[2], Decimal("199.99"))
        self.assertEqual(row[3], category.id)
        self.assertEqual(row[4], brand.id)
        self.assertEqual(row[5], 10)

    def test_add_category(self):
        """Добавление категории через ORM и проверка через SQL."""
        category = Category.objects.create(name="New Category")

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, name FROM store_category WHERE id = %s",
                [category.id]
            )
            row = cursor.fetchone()

        self.assertIsNotNone(row, "Категория не найдена в БД")
        self.assertEqual(row[1], "New Category")

    def test_add_tag(self):
        """Добавление тега через ORM и проверка через SQL."""
        tag = Tag.objects.create(name="New Tag")

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, name FROM store_tag WHERE id = %s",
                [tag.id]
            )
            row = cursor.fetchone()

        self.assertIsNotNone(row, "Тег не найден в БД")
        self.assertEqual(row[1], "New Tag")

    def test_delete_product(self):
        """Удаление товара через ORM и проверка через SQL."""
        category = CategoryFactory()
        brand = BrandFactory()
        product = Product.objects.create(
            name="ToDelete",
            price=Decimal("100.00"),
            category=category,
            brand=brand,
            stock=5
        )
        product_id = product.id

        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM store_product WHERE id = %s", [product_id])
            self.assertIsNotNone(cursor.fetchone(), "Товар не создан перед удалением")

        product.delete()

        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM store_product WHERE id = %s", [product_id])
            row = cursor.fetchone()
        self.assertIsNone(row, "Товар не удалён из БД")

        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM store_category WHERE id = %s", [category.id])
            self.assertIsNotNone(cursor.fetchone(), "Категория не должна была удалиться")

            cursor.execute("SELECT id FROM store_brand WHERE id = %s", [brand.id])
            self.assertIsNotNone(cursor.fetchone(), "Бренд не должен был удалиться")
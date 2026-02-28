# store/tests/test_orm_relationships.py
from django.test import TestCase
from django.db import connection
from decimal import Decimal
from ..models import Product, Category, Brand, Tag
from ..factories import TagFactory


class ORMRelationshipsTest(TestCase):
    """
    Тесты для операций добавления и удаления связей
    (аналог студентов и курсов). Совместимо с PostgreSQL.
    """

    def setUp(self):
        """Создаём общие объекты для тестов."""
        self.category = Category.objects.create(name="Test Category")
        self.brand = Brand.objects.create(name="Test Brand", country_of_origin="Test Country")

    def test_add_tag_to_product(self):
        """Добавление тега к товару (создание связи) и проверка через SQL."""
        product = Product.objects.create(
            name="Test Product",
            price=Decimal("100.00"),
            category=self.category,
            brand=self.brand,
            stock=10
        )
        tag = TagFactory(name="Test Tag")

        product.tags.add(tag)

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT product_id, tag_id FROM store_product_tags "
                "WHERE product_id = %s AND tag_id = %s",
                [product.id, tag.id]
            )
            row = cursor.fetchone()

        self.assertIsNotNone(row, "Связь товара с тегом не найдена в БД")
        self.assertEqual(row[0], product.id)
        self.assertEqual(row[1], tag.id)

    def test_delete_product_removes_tag_links(self):
        """Удаление товара должно удалить все его связи с тегами."""
        product = Product.objects.create(
            name="ToDelete",
            price=Decimal("100.00"),
            category=self.category,
            brand=self.brand,
            stock=5
        )
        tags = TagFactory.create_batch(3)
        product.tags.add(*tags)

        # Проверяем, что связи создались (3 записи)
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) FROM store_product_tags WHERE product_id = %s",
                [product.id]
            )
            count = cursor.fetchone()[0]
            self.assertEqual(count, 3, "Неверное количество связей перед удалением")

        product.delete()

        # Проверяем, что все связи удалены
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) FROM store_product_tags WHERE product_id = %s",
                [product.id]
            )
            count = cursor.fetchone()[0]
            self.assertEqual(count, 0, "Связи с тегами не удалились после удаления товара")

        # Проверяем, что сами теги остались
        for tag in tags:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id FROM store_tag WHERE id = %s", [tag.id])
                self.assertIsNotNone(cursor.fetchone(), f"Тег {tag.id} не должен был удалиться")
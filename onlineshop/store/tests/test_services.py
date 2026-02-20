from django.test import TestCase
from ..models import Product, Category, Brand, Tag
from ..services import (
    get_products_with_category,
    get_product_by_id,
    get_categories,
)
from ..factories import ProductFactory, CategoryFactory, BrandFactory, TagFactory


class GetProductsWithCategoryTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cat1 = CategoryFactory(name="Electronics")
        cls.cat2 = CategoryFactory(name="Books")

    def test_default_returns_10_products_in_stock(self):
        ProductFactory.create_batch(10, stock=5)
        ProductFactory.create_batch(5, stock=0)
        result = get_products_with_category()
        self.assertEqual(len(result), 10)
        for p in result:
            self.assertGreater(p.stock, 0)

    def test_count_none_returns_all_products(self):
        ProductFactory.create_batch(20)
        result = get_products_with_category(count=None, in_stock_only=False)
        self.assertEqual(len(result), 20)

    def test_filter_by_category(self):
        ProductFactory.create_batch(3, category=self.cat1)
        ProductFactory.create_batch(2, category=self.cat2)
        result = get_products_with_category(
            count=None, in_stock_only=False, category_id=self.cat1.id
        )
        self.assertEqual(len(result), 3)
        for p in result:
            self.assertEqual(p.category_id, self.cat1.id)

    def test_in_stock_only_combined_with_category(self):
        ProductFactory.create_batch(4, category=self.cat1, stock=5)
        ProductFactory.create_batch(3, category=self.cat1, stock=0)
        result = get_products_with_category(
            count=None, in_stock_only=True, category_id=self.cat1.id
        )
        self.assertEqual(len(result), 4)
        for p in result:
            self.assertGreater(p.stock, 0)
            self.assertEqual(p.category_id, self.cat1.id)


class GetProductByIdTest(TestCase):
    def test_existing_product(self):
        product = ProductFactory()
        retrieved = get_product_by_id(product.id)
        self.assertEqual(retrieved, product)
        # Проверяем, что prefetch_related сработал (необязательно)
        self.assertTrue(hasattr(retrieved, '_prefetched_objects_cache'))
        self.assertIn('tags', retrieved._prefetched_objects_cache)

    def test_non_existing_product_returns_none(self):
        self.assertIsNone(get_product_by_id(99999))


class GetCategoriesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        CategoryFactory.create_batch(15)

    def test_default_returns_10_categories(self):
        result = get_categories()
        self.assertEqual(len(result), 10)

    def test_count_none_returns_all(self):
        result = get_categories(count=None)
        self.assertEqual(len(result), 15)

    def test_custom_count(self):
        result = get_categories(count=3)
        self.assertEqual(len(result), 3)

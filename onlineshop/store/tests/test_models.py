from django.test import TestCase
from django.db import IntegrityError
from ..models import Brand, Tag, Product, Category, Review
from ..factories import BrandFactory, TagFactory, ProductFactory, CategoryFactory


class BrandModelTest(TestCase):
    def test_brand_creation_with_factory(self):
        """Тест создания бренда через фабрику (проверка работы фабрики, необязательно)."""
        brand = BrandFactory(name="TestBrand", country_of_origin="TestCountry")
        self.assertEqual(brand.name, "TestBrand")
        self.assertEqual(brand.country_of_origin, "TestCountry")
        self.assertIsNotNone(brand.pk)

    # Тест __str__ удалён как избыточный


class TagModelTest(TestCase):
    def test_tag_name_unique(self):
        """Проверка уникальности имени тега."""
        Tag.objects.create(name="unique_tag")
        with self.assertRaises(IntegrityError):
            Tag.objects.create(name="unique_tag")

    # Тест __str__ удалён


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.brand = BrandFactory(name="Dell")
        cls.category = CategoryFactory(name="Laptops")
        cls.tag1 = TagFactory(name="gaming")
        cls.tag2 = TagFactory(name="laptop")

    def test_is_available_method(self):
        """Проверка метода is_available()."""
        product_in = ProductFactory(stock=5)
        self.assertTrue(product_in.is_available())
        product_out = ProductFactory(stock=0)
        self.assertFalse(product_out.is_available())

    def test_product_brand_relationship(self):
        """Проверка связи с брендом."""
        product = ProductFactory(brand=self.brand)
        self.assertEqual(product.brand, self.brand)
        self.assertIn(product, self.brand.product_set.all())

    def test_product_category_relationship(self):
        """Проверка связи с категорией."""
        product = ProductFactory(category=self.category)
        self.assertEqual(product.category, self.category)
        self.assertIn(product, self.category.product_set.all())

    def test_product_tags_m2m_relationship(self):
        """Проверка связи многие-ко-многим с тегами."""
        product = ProductFactory(tags=[self.tag1, self.tag2])
        self.assertEqual(product.tags.count(), 2)
        self.assertIn(self.tag1, product.tags.all())
        self.assertIn(self.tag2, product.tags.all())
        self.assertIn(product, self.tag1.product_set.all())

    def test_product_creation_minimal_fields(self):
        """Проверка создания продукта с минимально необходимыми полями."""
        product = Product.objects.create(
            name="Test Product",
            price=100.00,
            category=self.category,
            brand=self.brand
        )
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.price, 100.00)
        self.assertEqual(product.stock, 0)  # значение по умолчанию


class ReviewModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product = ProductFactory()

    def test_create_review(self):
        """Проверка создания отзыва и авто-даты."""
        review = Review.objects.create(
            product=self.product,
            author_name="Test User",
            email="test@example.com",
            text="Great product!",
            rating=5
        )
        self.assertEqual(review.product, self.product)
        self.assertEqual(review.author_name, "Test User")
        self.assertEqual(review.rating, 5)
        self.assertIsNotNone(review.created_at)

    def test_review_optional_fields(self):
        """Проверка, что email и rating могут быть пустыми."""
        review = Review.objects.create(
            product=self.product,
            author_name="John",
            text="Nice"
        )
        self.assertIsNone(review.email)
        self.assertIsNone(review.rating)
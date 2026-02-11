from django.test import TestCase
from django.db import IntegrityError
from ..models import Brand, Tag, Product
from ..services import BrandFactory, TagFactory, ProductFactory, CategoryFactory


class BrandModelTest(TestCase):
    def test_create_brand(self):
        brand = BrandFactory()
        self.assertIsNotNone(brand.pk)
        self.assertTrue(brand.name)
        self.assertTrue(brand.country_of_origin)

    def test_brand_str_method(self):
        brand = BrandFactory(name="TestBrand")
        self.assertEqual(str(brand), "TestBrand")


class TagModelTest(TestCase):
    def test_create_tag(self):
        tag = TagFactory()
        self.assertIsNotNone(tag.pk)
        self.assertTrue(tag.name)

    def test_tag_name_unique(self):
        Tag.objects.create(name="unique_tag")
        with self.assertRaises(IntegrityError):
            Tag.objects.create(name="unique_tag")

    def test_tag_str_method(self):
        tag = TagFactory(name="TestTag")
        self.assertEqual(str(tag), "TestTag")


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаём базовые объекты один раз для всего класса
        cls.brand = BrandFactory(name="Dell")
        cls.category = CategoryFactory(name="Laptops")
        cls.tag1 = TagFactory(name="gaming")
        cls.tag2 = TagFactory(name="laptop")

    def test_create_product(self):
        product = ProductFactory(
            category=self.category,
            brand=self.brand,
            tags=[self.tag1, self.tag2]
        )
        self.assertIsNotNone(product.pk)
        self.assertTrue(product.name)
        self.assertGreater(product.price, 0)
        self.assertEqual(product.category, self.category)
        self.assertEqual(product.brand, self.brand)
        self.assertGreaterEqual(product.stock, 0)
        self.assertEqual(product.tags.count(), 2)

    def test_is_available_method(self):
        product_in = ProductFactory(stock=5)
        self.assertTrue(product_in.is_available())
        product_out = ProductFactory(stock=0)
        self.assertFalse(product_out.is_available())

    def test_product_brand_relationship(self):
        product = ProductFactory(brand=self.brand)
        self.assertEqual(product.brand, self.brand)
        self.assertIn(product, self.brand.product_set.all())

    def test_product_tags_m2m_relationship(self):
        product = ProductFactory(tags=[self.tag1, self.tag2])
        self.assertEqual(product.tags.count(), 2)
        self.assertIn(self.tag1, product.tags.all())
        self.assertIn(self.tag2, product.tags.all())
        self.assertIn(product, self.tag1.product_set.all())

    def test_filter_products_by_brand(self):
        brand_a = BrandFactory(name="BrandA")
        brand_b = BrandFactory(name="BrandB")
        ProductFactory.create_batch(3, brand=brand_a)
        ProductFactory.create_batch(2, brand=brand_b)

        self.assertEqual(Product.objects.filter(brand=brand_a).count(), 3)
        self.assertEqual(Product.objects.filter(brand=brand_b).count(), 2)

    def test_filter_products_by_tag(self):
        tag_new = TagFactory(name="new")
        tag_sale = TagFactory(name="sale")
        ProductFactory(tags=[tag_new])
        ProductFactory(tags=[tag_new, tag_sale])
        ProductFactory(tags=[tag_sale])

        self.assertEqual(Product.objects.filter(tags=tag_new).count(), 2)
        self.assertEqual(Product.objects.filter(tags=tag_sale).count(), 2)

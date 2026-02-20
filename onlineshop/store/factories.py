import factory
import random
from factory.django import DjangoModelFactory
from faker import Faker
from .models import Category, Brand, Tag, Product

fake_ru = Faker('ru_RU')
fake_en = Faker('en_US')


def generate_tech_product_name(category_name: str) -> str:
    """Генерирует реалистичное название продукта на основе категории."""
    cat = category_name.lower()
    if 'ноутбук' in cat:
        models = ['MacBook Pro', 'XPS', 'ThinkPad', 'ROG Strix', 'IdeaPad', 'Swift', 'Gram', 'Surface Laptop']
        return f"{fake_en.random_element(models)} {fake_en.bothify(text='??###')}"
    elif 'смартфон' in cat or 'телефон' in cat:
        models = ['iPhone', 'Galaxy S', 'Pixel', 'Xperia', 'Mi', 'Redmi', 'Nova', 'OnePlus']
        return f"{fake_en.random_element(models)} {fake_en.numerify(text='##')}"
    elif 'планшет' in cat:
        models = ['iPad', 'Galaxy Tab', 'MatePad', 'Lenovo Tab', 'Surface Go']
        return f"{fake_en.random_element(models)} {fake_en.bothify(text='??##')}"
    elif 'наушник' in cat:
        models = ['AirPods', 'WH-1000XM', 'Galaxy Buds', 'Mi True Wireless', 'QuietComfort', 'Momentum']
        return f"{fake_en.random_element(models)} {fake_en.numerify(text='##')}"
    elif 'колонк' in cat:
        models = ['JBL Flip', 'Sony SRS', 'Marshall Stanmore', 'Xiaomi Mi', 'HomePod', 'Echo']
        return f"{fake_en.random_element(models)} {fake_en.numerify(text='##')}"
    elif 'монитор' in cat:
        models = ['UltraSharp', 'Predator', 'ROG Swift', 'Smart Monitor', 'Pro Display']
        return f"{fake_en.random_element(models)} {fake_en.numerify(text='##')}\""
    elif 'клавиатур' in cat:
        models = ['G915', 'K70', 'BlackWidow', 'MX Keys', 'Craft', 'Ornata']
        return f"{fake_en.random_element(models)} {fake_en.bothify(text='??##')}"
    elif 'мыш' in cat:
        models = ['G502', 'DeathAdder', 'MX Master', 'Razer Viper', 'M590', 'Glorious']
        return f"{fake_en.random_element(models)} {fake_en.bothify(text='??##')}"
    elif 'веб-камер' in cat:
        models = ['C920', 'StreamCam', 'Brio', 'Webcam']
        return f"{fake_en.random_element(models)} {fake_en.numerify(text='##')}"
    elif 'жестк' in cat or 'ssd' in cat:
        models = ['My Passport', 'T7', 'BarraCuda', 'WD Black', 'Samsung SSD']
        return f"{fake_en.random_element(models)} {fake_en.numerify(text='##')}GB"
    else:
        return f"{fake_en.catch_phrase()} {fake_en.bothify(text='???###')}"


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ('name',)

    name = factory.LazyFunction(lambda: fake_ru.unique.word())


class BrandFactory(DjangoModelFactory):
    class Meta:
        model = Brand
        django_get_or_create = ('name',)

    name = factory.LazyFunction(lambda: fake_en.unique.company())
    country_of_origin = factory.LazyFunction(lambda: fake_en.country())


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag
        django_get_or_create = ('name',)

    name = factory.LazyFunction(lambda: fake_ru.unique.word())


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.LazyAttribute(lambda o: generate_tech_product_name(o.category.name))
    price = factory.LazyFunction(lambda: round(fake_ru.pyfloat(left_digits=4, right_digits=2, positive=True), 2))
    stock = factory.LazyFunction(lambda: fake_ru.random_int(min=0, max=100))
    category = factory.LazyFunction(lambda: Category.objects.order_by('?').first() or CategoryFactory())
    brand = factory.SubFactory(BrandFactory)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.tags.add(tag)
        else:
            tags_count = fake_ru.random_int(min=1, max=3)
            existing_tags = list(Tag.objects.all())
            if existing_tags:
                selected_tags = random.sample(existing_tags, min(tags_count, len(existing_tags)))
                self.tags.add(*selected_tags)
            else:
                new_tags = TagFactory.create_batch(tags_count)
                self.tags.add(*new_tags)


def generate_products(count: int = 100) -> list[Product]:
    """Создаёт указанное количество случайных продуктов (использует фабрики)."""
    return ProductFactory.create_batch(count)
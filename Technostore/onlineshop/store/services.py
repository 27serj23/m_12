import factory
from factory.django import DjangoModelFactory
from faker import Faker
from .models import Category, Brand, Tag, Product

# -------------------------------------------------------------------
# Faker instance
# -------------------------------------------------------------------
fake = Faker()

# -------------------------------------------------------------------
# Фабрики для генерации тестовых данных
# -------------------------------------------------------------------

class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ('name',)

    name = factory.LazyFunction(lambda: fake.unique.word())


class BrandFactory(DjangoModelFactory):
    class Meta:
        model = Brand
        django_get_or_create = ('name',)

    name = factory.LazyFunction(lambda: fake.unique.company())
    country_of_origin = factory.LazyFunction(lambda: fake.country())


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag
        django_get_or_create = ('name',)

    name = factory.LazyFunction(lambda: fake.unique.word())


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.LazyFunction(lambda: fake.unique.catch_phrase())
    price = factory.LazyFunction(lambda: round(fake.pyfloat(left_digits=4, right_digits=2, positive=True), 2))
    stock = factory.LazyFunction(lambda: fake.random_int(min=0, max=100))
    category = factory.SubFactory(CategoryFactory)
    brand = factory.SubFactory(BrandFactory)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.tags.add(tag)
        else:
            tags_count = fake.random_int(min=1, max=3)
            tags = TagFactory.create_batch(tags_count)
            self.tags.add(*tags)


# -------------------------------------------------------------------
# Вспомогательная функция массовой генерации продуктов
# -------------------------------------------------------------------
def generate_products(count: int = 100) -> list[Product]:
    """Создаёт указанное количество случайных продуктов."""
    return ProductFactory.create_batch(count)


# -------------------------------------------------------------------
# Сервисные функции (бизнес-логика)
# -------------------------------------------------------------------

def get_products_with_category(count: int = 10,
                               in_stock_only: bool = True,
                               category_id: int = None):
    queryset = Product.objects.select_related('category', 'brand').prefetch_related('tags')
    if in_stock_only:
        queryset = queryset.filter(stock__gt=0)
    if category_id:
        queryset = queryset.filter(category_id=category_id)
    if count is None:
        return queryset
    return queryset[:count]


def get_product_by_id(product_id: int) -> Product | None:
    try:
        return Product.objects.select_related('category', 'brand') \
                              .prefetch_related('tags') \
                              .get(id=product_id)
    except Product.DoesNotExist:
        return None


def get_categories(count: int = 10):
    queryset = Category.objects.all()
    if count is None:
        return queryset
    return queryset[:count]
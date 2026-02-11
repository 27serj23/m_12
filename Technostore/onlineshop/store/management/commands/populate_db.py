import random
from django.core.management.base import BaseCommand
from faker import Faker
from ...models import Category, Product, Order, OrderItem

fake = Faker('ru_RU')


class Command(BaseCommand):
    help = 'Заполняет базу тестовыми данными'

    def handle(self, *args, **options):
        # Категории
        categories = ['Ноутбуки', 'Смартфоны', 'Планшеты', 'Наушники', 'Мониторы']
        for cat_name in categories:
            Category.objects.get_or_create(name=cat_name)
        self.stdout.write('Категории созданы')

        # Товары
        products = []
        categories = list(Category.objects.all())
        for _ in range(30):
            name = fake.word().capitalize() + ' ' + fake.random_element(['Pro', 'Lite', 'Max', 'Air', 'Ultra'])
            price = round(random.uniform(1000, 150000), 2)
            category = random.choice(categories)
            stock = random.randint(0, 50)
            product = Product.objects.create(
                name=name,
                price=price,
                category=category,
                stock=stock
            )
            products.append(product)
        self.stdout.write('Товары созданы')

        # Заказы
        for _ in range(20):
            customer = fake.name()
            order = Order.objects.create(customer_name=customer)
            for _ in range(random.randint(1, 5)):
                product = random.choice(products)
                quantity = random.randint(1, 3)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity
                )
        self.stdout.write('Заказы созданы')
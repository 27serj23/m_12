from django.core.management.base import BaseCommand
from django.conf import settings
from ...factories import generate_products
from ...models import Category, Brand, Tag, Product

# ... остальной код без изменений

# Категории на русском
TECH_CATEGORIES = [
    'Ноутбуки',
    'Смартфоны',
    'Планшеты',
    'Наушники',
    'Колонки',
    'Мониторы',
    'Клавиатуры',
    'Компьютерные мыши',
    'Веб-камеры',
    'Внешние жесткие диски',
]

# Бренды с английскими названиями
TECH_BRANDS = [
    {'name': 'Apple', 'country': 'USA'},
    {'name': 'Samsung', 'country': 'South Korea'},
    {'name': 'Xiaomi', 'country': 'China'},
    {'name': 'Huawei', 'country': 'China'},
    {'name': 'Honor', 'country': 'China'},
    {'name': 'Sony', 'country': 'Japan'},
    {'name': 'LG', 'country': 'South Korea'},
    {'name': 'Philips', 'country': 'Netherlands'},
    {'name': 'Panasonic', 'country': 'Japan'},
    {'name': 'Canon', 'country': 'Japan'},
    {'name': 'HP', 'country': 'USA'},
    {'name': 'Dell', 'country': 'USA'},
    {'name': 'Lenovo', 'country': 'China'},
    {'name': 'Asus', 'country': 'Taiwan'},
    {'name': 'Acer', 'country': 'Taiwan'},
    {'name': 'MSI', 'country': 'Taiwan'},
    {'name': 'Gigabyte', 'country': 'Taiwan'},
    {'name': 'Logitech', 'country': 'Switzerland'},
    {'name': 'Razer', 'country': 'USA'},
    {'name': 'Corsair', 'country': 'USA'},
    {'name': 'JBL', 'country': 'USA'},
    {'name': 'Marshall', 'country': 'UK'},
    {'name': 'Beats', 'country': 'USA'},
]

# Теги на русском
TECH_TAGS = [
    'новинка',
    'хит продаж',
    'акция',
    'распродажа',
    'игровой',
    'для работы',
    'бюджетный',
    'премиум',
    'беспроводной',
    'Bluetooth',
    'USB-C',
    'механический',
    'OLED',
    '4K',
    'Retina',
    'шумоподавление',
    'водонепроницаемый',
    'быстрая зарядка',
    'долгая работа',
    'компактный',
]


class Command(BaseCommand):
    help = 'Наполняет БД техно-товарами (только для DEBUG)'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=50, help='Количество продуктов (по умолчанию 50)')
        parser.add_argument('--force', action='store_true', help='Пропустить предупреждение безопасности')

    def handle(self, *args, **options):
        if not settings.DEBUG and not options['force']:
            self.stderr.write(self.style.ERROR('Команда доступна только в режиме DEBUG.'))
            self.stderr.write('Используйте --force для принудительного выполнения.')
            return

        if not options['force']:
            confirm = input('Вы уверены? Это удалит все существующие данные в приложении store! (y/N): ')
            if confirm.lower() != 'y':
                self.stdout.write('Отменено.')
                return

        # Очистка существующих данных
        self.stdout.write('Очистка старых данных...')
        Product.objects.all().delete()
        Tag.objects.all().delete()
        Brand.objects.all().delete()
        Category.objects.all().delete()

        # Создание категорий
        self.stdout.write('Создание категорий...')
        for cat_name in TECH_CATEGORIES:
            Category.objects.get_or_create(name=cat_name)

        # Создание брендов
        self.stdout.write('Создание брендов...')
        for b in TECH_BRANDS:
            Brand.objects.get_or_create(name=b['name'], defaults={'country_of_origin': b['country']})

        # Создание тегов
        self.stdout.write('Создание тегов...')
        for tag_name in TECH_TAGS:
            Tag.objects.get_or_create(name=tag_name)

        # Генерация продуктов
        count = options['count']
        self.stdout.write(f'Генерация {count} продуктов...')
        generate_products(count)

        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена.'))
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    """Категория товара (например, Ноутбуки, Смартфоны)."""
    name = models.CharField(
        max_length=100,
        verbose_name="Название"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Brand(models.Model):
    """Бренд производителя (Apple, Samsung, Sony и т.д.)."""
    name = models.CharField(
        max_length=100,
        verbose_name="Бренд"
    )
    country_of_origin = models.CharField(
        max_length=100,
        verbose_name="Страна производитель"
    )

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Тег для маркировки товаров (новинка, хитродаж, игровой и т.п.)."""
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Тег"
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Product(models.Model):
    """Товар интернет-магазина."""
    name = models.CharField(
        max_length=100,
        verbose_name="Название"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категория"
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        verbose_name="Бренд"
    )
    stock = models.IntegerField(
        default=0,
        verbose_name="Количество на складе"
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        verbose_name="Теги"
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name

    def is_available(self) -> bool:
        """Проверка наличия товара на складе."""
        return self.stock > 0


class Contact(models.Model):
    """Обратная связь"""
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"

    def __str__(self):
        return f"{self.name} - {self.email}"


class Review(models.Model):
    """Отзыв на товар"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Товар"
    )
    author_name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email", blank=True, null=True)
    text = models.TextField(verbose_name="Текст отзыва")
    rating = models.PositiveSmallIntegerField(
        verbose_name="Оценка",
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        blank=True,
        null=True,
        help_text="Оцените товар от 1 до 5"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отзыва")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author_name} - {self.product.name}"
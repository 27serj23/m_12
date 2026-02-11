from django.db import models


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
        unique=True,                # обязательная уникальность
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
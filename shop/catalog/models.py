"""
Модели продуктов, категорий, отзывов 
"""

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    """
    Модель категории товаров
    """

    title = models.CharField(
        max_length=100, blank=False, unique=True, verbose_name="Название категории"
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="subcategories",
        verbose_name="Родительская категория",
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        # Проверяем уровень вложенности
        if self.parent and self.parent.parent:
            raise ValidationError("Максимальный уровень вложенности для категории — 2.")
        super().save(*args, **kwargs)


def category_image_directory_path(instance: "CategoryImage", filename: str) -> str:
    """Путь к изображению категории"""
    return "categories/category_{pk}/image/{filename}".format(
        pk=instance.category.pk,
        filename=filename,
    )


class CategoryImage(models.Model):
    """Модель категории"""

    category = models.OneToOneField(
        Category, on_delete=models.CASCADE, related_name="image"
    )
    src = models.ImageField(
        upload_to=category_image_directory_path, verbose_name="Ссылка"
    )
    alt = models.CharField(
        max_length=100, null=False, blank=True, verbose_name="Описание"
    )

    class Meta:
        verbose_name = "Изображение категории"

    def __str__(self) -> str:
        return self.alt


class Product(models.Model):
    """
    Модель товара
    """

    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name="products"
    )
    price = models.DecimalField(
        default=0, max_digits=8, decimal_places=2, blank=False, verbose_name="Цена"
    )
    count = models.IntegerField(default=0, blank=False, verbose_name="Количество")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата")
    title = models.CharField(max_length=100, blank=False, verbose_name="Название")
    description = models.CharField(max_length=100, blank=True, verbose_name="Описание")
    fullDescription = models.TextField(
        null=False, blank=True, verbose_name="Полное описание"
    )
    freeDelivery = models.BooleanField(
        default=False, verbose_name="Бесплатная доставка"
    )
    rating = models.DecimalField(
        default=0, max_digits=3, decimal_places=2, verbose_name="Рейтинг"
    )
    limited = models.BooleanField(default=False, verbose_name="Лимитированный товар")

    available = models.BooleanField(default=True, verbose_name="В наличии")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.title

    def current_price(self):
        current_date = timezone.now().date()

        active_sale = self.sales.filter(
            dateFrom__lte=current_date, dateTo__gte=current_date
        ).aggregate(min_price=models.Min("salePrice"))["min_price"]

        if active_sale is not None:
            return active_sale

        return self.price


def product_images_directory_path(instance: "ProductImage", filename: str) -> str:
    """Путь к изображению товара"""
    return "products/product_{pk}/images/{filename}".format(
        pk=instance.product.pk,
        filename=filename,
    )


class ProductImage(models.Model):
    """Изображения товара"""

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    src = models.ImageField(
        upload_to=product_images_directory_path, verbose_name="Ссылка"
    )
    alt = models.CharField(
        max_length=100, null=False, blank=True, verbose_name="Описание"
    )

    class Meta:
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товара"

    def __str__(self):
        return self.alt


class Tag(models.Model):
    """Модель тега"""

    products = models.ManyToManyField(Product, blank=True, related_name="tags")
    name = models.CharField(
        max_length=20, blank=True, unique=True, verbose_name="Название"
    )

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"

    def __str__(self) -> str:
        return self.name


class Review(models.Model):
    """Модель отзыва"""

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    email = models.EmailField(verbose_name="email")
    text = models.TextField(blank=True, verbose_name="Текст")
    rate = models.IntegerField(default=0, verbose_name="Рейтинг")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"Отзыв {self.pk} от {self.date}"


class ProductSpecification(models.Model):
    """Модель характеристики товара"""

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="specifications"
    )
    name = models.CharField(max_length=100, blank=True, verbose_name="Наименование")
    value = models.CharField(max_length=100, verbose_name="Значение")

    class Meta:
        verbose_name = "Характеристика"
        verbose_name_plural = "Характеристики"

    def __str__(self):
        return self.name


class Sale(models.Model):
    """Модель скидки"""

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="sales", verbose_name="Скидки"
    )
    salePrice = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, verbose_name="Цена со скидкой"
    )
    dateFrom = models.DateField(auto_now_add=False, verbose_name="Действует с")
    dateTo = models.DateField(auto_now_add=False, verbose_name="Дейсвтвует до")

    class Meta:
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"

    def __str__(self) -> str:
        return f"{self.product}"


class Banner(models.Model):
    sale = models.OneToOneField(
        Sale, on_delete=models.CASCADE, related_name="banneer", verbose_name="Баннер"
    )
    titul = models.CharField(
        max_length=100, blank=True, null=False, verbose_name="Название баннера"
    )

    class Meta:
        verbose_name = "Баннер"
        verbose_name_plural = "Баннеры"

    def __str__(self) -> str:
        return f"{self.sale}"

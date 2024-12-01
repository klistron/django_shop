from django.db import models
from django.contrib.auth.models import User

from catalog.models import Product


class Basket(models.Model):
    """Класс для корзины"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Корзина")

    class Meta:
        verbose_name = "Корзина"

    def __str__(self) -> str:
        return f"Корзина пользователя {self.user}"


class BasketItem(models.Model):
    """Класс для товаров в корзине"""

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Товар в корзине",
    )
    basket = models.ForeignKey(
        Basket,
        on_delete=models.CASCADE,
        related_name="basket_items",
        blank=True,
        null=True,
    )
    session = models.CharField(max_length=100, null=True, blank=True)
    basket_count = models.PositiveIntegerField(
        default=1, verbose_name="Количество товаров"
    )
    date = models.DateTimeField(auto_now=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"

    def __str__(self) -> str:
        return f"{self.product}"

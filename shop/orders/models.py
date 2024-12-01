from django.db import models
from django.contrib.auth.models import User
from catalog.models import Product


class Order(models.Model):
    """Класс для заказа"""

    created_add = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания заказа"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    products = models.ManyToManyField(Product, related_name="orders")
    deliveryType = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Тип доставки"
    )
    paymentType = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Тип оплаты"
    )
    totalCost = models.DecimalField(
        default=0,
        blank=True,
        null=True,
        decimal_places=2,
        max_digits=10,
        verbose_name="Общая стоимость",
    )
    status = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Статус"
    )
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name="Город")
    address = models.CharField(
        max_length=200, blank=True, null=True, verbose_name="Адрес"
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self) -> str:
        return f"Order {self.pk} пользователя {self.user}"

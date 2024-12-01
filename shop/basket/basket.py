from decimal import Decimal
from django.conf import settings
from catalog.models import Product


class BasketSession(object):

    def __init__(self, request):
        """
        Инициализируем корзину
        """
        self.session = request.session
        basket = self.session.get(settings.CART_SESSION_ID)
        if not basket:
            # save an empty cart in the session
            basket = self.session[settings.CART_SESSION_ID] = {}
        self.basket = basket

    def add(self, product, quantity=1, update_quantity=False):
        """
        Добавить продукт в корзину или обновить его количество.
        """
        product_id = str(product.id)
        if product_id not in self.basket:
            self.basket[product_id] = {'quantity': 0,
                                    'price': str(product.price)}
        if update_quantity:
            self.basket[product_id]['quantity'] = quantity
        else:
            self.basket[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Обновление сессии basket
        self.session[settings.CART_SESSION_ID] = self.basket
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, product, quantity):
        """
        Удаление товара из корзины.
        """
        product_id = str(product.id)
        if self.basket[product_id]['quantity'] == 1:
            del self.basket[product_id]
        else:
            self.basket[product_id]['quantity'] -= quantity
        self.save()

    def __iter__(self):
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """
        product_ids = self.basket.keys()
        # получение объектов product и добавление их в корзину
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.basket[str(product.id)]['product'] = product

        for item in self.basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
            
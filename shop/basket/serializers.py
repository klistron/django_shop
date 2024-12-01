from rest_framework import serializers
from catalog.serializers import ProductCatalogSerializer
from catalog.models import Product


class BasketSerializer(ProductCatalogSerializer):

    count = serializers.SerializerMethodField()

    def get_count(self, instance):
        basket_items = self.context["basket_items"]
        basket_item = basket_items.filter(product=instance).first()
        return basket_item.basket_count if basket_item else 0

    class Meta:
        model = Product
        fields = (
            "id",
            "title",
            "description",
            "category",
            "freeDelivery",
            "count",  # Поле count теперь берется из BasketItem
            "price",
            "date",
            "images",
            "tags",
            "rating",
            "reviews",
        )


class BasketSerializerSession(ProductCatalogSerializer):

    class Meta:
        model = Product
        fields = (
            "id",
            "title",
            "description",
            "category",
            "freeDelivery",
            "price",
            "date",
            "images",
            "tags",
            "rating",
            "reviews",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        basket = self.context.get("basket")

        if basket and str(instance.id) in basket:
            representation["count"] = basket[str(instance.id)]["quantity"]
        else:
            representation["count"] = 0

        return representation

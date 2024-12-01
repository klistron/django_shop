from django.db.models import Avg
from rest_framework import serializers
from .models import (
    Category,
    CategoryImage,
    Product,
    ProductImage,
    ProductSpecification,
    Review,
    Tag,
    Sale,
)


class CategoryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryImage
        fields = ["src", "alt"]


class CategorySerializer(serializers.ModelSerializer):
    image = CategoryImageSerializer()
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "title", "image", "subcategories"]

    def get_subcategories(self, obj):
        serializer = CategorySerializer(obj.subcategories.all(), many=True)
        return serializer.data


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["src", "alt"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            "name",
        ]


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    date = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Review
        fields = ["author", "text", "rate", "date"]

    def get_author(self, obj):
        # Предполагается, что у вас есть связь между Review и User через ForeignKey
        return obj.author.username if obj.author else None


class ProductSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecification
        fields = ["name", "value"]


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)
    tags = TagSerializer(many=True)
    reviews = ReviewSerializer(many=True)
    specifications = ProductSpecificationSerializer(many=True)
    date = serializers.DateTimeField(format="%a %b %d %Y %H:%M:%S GMT%z (%Z)")
    rating = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "fullDescription",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "specifications",
            "rating",
        ]

    def get_rating(self, instance: "Product"):
        reviews = instance.reviews.all()
        if reviews:
            return round(reviews.aggregate(Avg("rate"))["rate__avg"], 1)

    def get_price(self, instance: "Product"):
        return instance.current_price()


class ProductCatalogSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)
    tags = serializers.SerializerMethodField()
    freeDelivery = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    def get_price(self, instance: "Product"):
        return instance.current_price()

    def get_reviews(self, instance: "Product"):
        return instance.reviews.count()

    def get_tags(self, instance: "Product"):
        tags = [
            {
                "id": tag.id,
                "name": tag.name,
            }
            for tag in instance.tags.all()
        ]
        return tags

    def get_freeDelivery(self, instance: "Product"):
        return instance.freeDelivery

    def get_rating(self, instance: "Product"):
        reviews = instance.reviews.all()
        if reviews:
            return round(reviews.aggregate(Avg("rate"))["rate__avg"], 1)

    class Meta:
        model = Product
        fields = (
            "id",
            "title",
            "description",
            "category",
            "freeDelivery",
            "count",
            "price",
            "date",
            "images",
            "tags",
            "rating",
            "reviews",
        )

class SaleProductSerializer(serializers.ModelSerializer):
    salePrice = serializers.SerializerMethodField()
    dateFrom = serializers.SerializerMethodField()
    dateTo = serializers.SerializerMethodField()
    images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'price', 'salePrice', 'dateFrom', 'dateTo', 'title', 'images']

    def get_salePrice(self, obj):
        sale = obj.sales.first()
        return sale.salePrice if sale else None

    def get_dateFrom(self, obj):
        sale = obj.sales.first()
        return sale.dateFrom.strftime("%m-%d") if sale else None

    def get_dateTo(self, obj):
        sale = obj.sales.first()
        return sale.dateTo.strftime("%m-%d") if sale else None
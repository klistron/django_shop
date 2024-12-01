from django.contrib import admin

from .models import (
    Category,
    CategoryImage,
    Product,
    ProductImage,
    Tag,
    Review,
    ProductSpecification,
    Sale,
    Banner
)


class CategoryImagesInline(admin.TabularInline):
    model = CategoryImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "parent",
    )
    inlines = [
        CategoryImagesInline,
    ]


class ProductImagesInline(admin.TabularInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "price",
        "count",
        "date",
        "description",
        "fullDescription",
        "freeDelivery",
        "rating",
        "limited",
    )
    inlines = [
        ProductImagesInline,
    ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "product",
        "text",
        "rate",
        "date",
    )

@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "name",
        "value",
    )

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "salePrice",
        "dateFrom",
        "dateTo",
    )

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = (
        "sale",
        "titul",
    )
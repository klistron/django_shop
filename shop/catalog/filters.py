from django.db.models import QuerySet, Count, Q
from rest_framework.filters import BaseFilterBackend
from rest_framework.request import Request
from .models import Category

class ProductFilter(BaseFilterBackend):
    def filter_queryset(self, request: Request, queryset: QuerySet, view):
        params = request.query_params
        ordering = params.get("sort")
        sort_type = params.get("sortType")
        name = params.get("filter[name]")
        min_price = params.get("filter[minPrice]")
        max_price = params.get("filter[maxPrice]")
        category = params.get("category")
        subcategory = params.get("subcategory")
        free_delivery = True if params.get("filter[freeDelivery]") == "true" else False
        available = True if params.get("filter[available]") == "true" else False
        tags = params.get("tags[]")

        if name:
            queryset = queryset.filter(title__icontains=name)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if free_delivery:
            queryset = queryset.filter(freeDelivery=free_delivery)
        if available:
            queryset = queryset.filter(available=True)
        if tags:
            tags = list(tags)
            queryset = queryset.filter(tags__in=tags)
        if category:
            # queryset = queryset.filter(category_id=category)
            subcategories = Category.objects.filter(Q(id=category) | Q(parent=category))
            queryset = queryset.filter(category__in=subcategories)


        if ordering == "price" and sort_type == "inc":
            queryset = queryset.order_by("price")
        elif ordering == "price" and sort_type == "dec":
            queryset = queryset.order_by("-price")
        elif ordering == "date" and sort_type == "inc":
            queryset = queryset.order_by("-date")
        elif ordering == "date" and sort_type == "dec":
            queryset = queryset.order_by("date")
        elif ordering == "reviews" and sort_type == "inc":
            queryset = queryset.annotate(reviews_count=Count("reviews")).order_by(
                "-reviews_count"
            )
        elif ordering == "reviews" and sort_type == "dec":
            queryset = queryset.annotate(reviews_count=Count("reviews")).order_by(
                "reviews_count"
            )
        elif ordering == "rating" and sort_type == "inc":
            queryset = queryset.annotate(orders_count=Count("reviews")).order_by(
                "-orders_count"
            )
        elif ordering == "rating" and sort_type == "dec":
            queryset = queryset.annotate(orders_count=Count("reviews")).order_by(
                "orders_count"
            )
        else:
            queryset = queryset.order_by("price")
        return queryset

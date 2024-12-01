from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, RetrieveAPIView, ListAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, exceptions
from django.db.models import Count, Avg
from django.utils import timezone
from .models import Category, Product, Review, Banner
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ReviewSerializer,
    ProductCatalogSerializer,
    SaleProductSerializer,
)
from .paginators import CatalogPagination
from .filters import ProductFilter


class CategoriesListView(ListAPIView):
    serializer_class = CategorySerializer
    pagination_class = None

    def get_queryset(self):
        # Фильтруем категории, которые имеют хотя бы одну подкатегорию
        # и хотя бы один доступный товар
        queryset = (
            Category.objects.annotate(
                subcategory_count=Count("subcategories"),
            )
            .filter(subcategory_count__gt=0)
            .order_by("id")
        )
        return queryset


class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        product = Product.objects.get(pk=pk)

        review = Review.objects.create(
            author=request.user,
            product=Product.objects.get(pk=pk),
            email=request.user.profile.email,
            text=request.data["text"],
            rate=request.data["rate"],
        )

        avg_rating = Review.objects.filter(product=product).aggregate(Avg("rate"))[
            "rate__avg"
        ]

        # Обновляем рейтинг продукта
        product.rating = round(avg_rating, 2) if avg_rating else 0
        product.save()

        serializer = ReviewSerializer(review)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def handle_exception(self, exc):
        if isinstance(exc, exceptions.NotAuthenticated):
            return Response(
                {"detail": "Необходимо авторизоваться для добавления отзыва."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return super().handle_exception(exc)


class CatalogAPIView(ListModelMixin, GenericAPIView):
    queryset = (
        Product.objects.all()
        .prefetch_related("images")
        .prefetch_related("tags")
        .prefetch_related("reviews")
        # .select_related("sale")
    )
    pagination_class = CatalogPagination
    serializer_class = ProductCatalogSerializer

    filter_backends = [ProductFilter]

    def get(self, request):
        return self.list(request)


class PopularProductsView(APIView):
    def get(self, request):
        popular_products = Product.objects.order_by("-rating")[:8]

        serializer = ProductCatalogSerializer(popular_products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LimitedProductsView(APIView):
    def get(self, request):
        limited_products = Product.objects.filter(limited=True)[:16]

        serializer = ProductCatalogSerializer(limited_products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class SaleView(ListModelMixin, GenericAPIView):
    pagination_class = CatalogPagination
    serializer_class = SaleProductSerializer

    def get_queryset(self):
        current_date = timezone.now().date()
        return Product.objects.filter(
            sales__dateFrom__lte=current_date, sales__dateTo__gte=current_date
        ).distinct()

    def get(self, request):
        return self.list(request)


class BannerProductsView(ListAPIView):
    serializer_class = ProductCatalogSerializer

    def get_queryset(self):
        current_date = timezone.now().date()
        active_banners = Banner.objects.filter(
            sale__dateTo__gte=current_date
        ).select_related("sale__product")

        products = [banner.sale.product for banner in active_banners]
        return products

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

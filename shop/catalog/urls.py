from django.urls import path
from .views import (
    ProductDetailView,
    ProductReviewView,
    CatalogAPIView,
    CategoriesListView,
    PopularProductsView,
    LimitedProductsView,
    SaleView,
    BannerProductsView,
)

app_name = "catalog"

urlpatterns = [
    path("api/categories/", CategoriesListView.as_view(), name="categories"),
    path("api/product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("api/product/<int:pk>/reviews", ProductReviewView.as_view(), name="review"),
    path("api/products/popular", PopularProductsView.as_view(), name="popular"),
    path("api/products/limited", LimitedProductsView.as_view(), name="limited"),
    path("api/catalog", CatalogAPIView.as_view(), name="catalog"),
    path("api/sales", SaleView.as_view(), name="sales"),
    path("api/banners", BannerProductsView.as_view(), name="banners"),
]

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

# from rest_framework.permissions import IsAuthenticated
from catalog.models import Product

# from catalog.serializers import ProductCatalogSerializer

# from catalog.serializers import ProductSerializer
from .models import Basket, BasketItem
from .serializers import BasketSerializer, BasketSerializerSession
from .basket import BasketSession


class BasketView(APIView):

    def get_basket_products(self, user):
        basket_items = BasketItem.objects.filter(basket__user=user)
        if not basket_items:
            return Product.objects.none()
        return Product.objects.filter(id__in=basket_items.values("product_id"))

    def get(self, request):
        if request.user.is_authenticated:
            products = self.get_basket_products(request.user)
            basket_items = BasketItem.objects.filter(basket__user=request.user)
            serializer = BasketSerializer(
                products, many=True, context={"basket_items": basket_items}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            basket = BasketSession(request)
            product_ids = list(basket.basket.keys())
            products = Product.objects.filter(id__in=product_ids)
            serializer = BasketSerializerSession(
                products, many=True, context={"basket": basket.basket}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        product_id = request.data.get("id")
        count = request.data.get("count", 1)
        product = Product.objects.get(id=product_id)
        if request.user.is_authenticated:
            basket, _ = Basket.objects.get_or_create(user=request.user)
            basket_item, created = BasketItem.objects.get_or_create(
                basket=basket, product=product
            )
            if not created:
                basket_item.basket_count += count
            else:
                basket_item.basket_count = count

            basket_item.save()
            products = self.get_basket_products(request.user)
            basket_items = BasketItem.objects.filter(basket__user=request.user)
            serializer = BasketSerializer(
                products, many=True, context={"basket_items": basket_items}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            basket = BasketSession(request)
            basket.add(product, quantity=count)
            product_ids = list(basket.basket.keys())
            products = Product.objects.filter(id__in=product_ids)
            serializer = BasketSerializerSession(
                products, many=True, context={"basket": basket.basket}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        product_id = request.data.get("id")
        count = request.data.get("count", 1)

        if request.user.is_authenticated:
            basket = Basket.objects.get(user=request.user)
            basket_item = BasketItem.objects.get(basket=basket, product__id=product_id)
            if basket_item.basket_count > count:
                basket_item.basket_count -= count
                basket_item.save()
            elif basket_item.basket_count == count:
                basket_item.delete()
            else:
                return Response(
                    {"error": "Количество для удаления больше, чем в корзине."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            remaining_products = self.get_basket_products(request.user)
            basket_items = BasketItem.objects.filter(basket__user=request.user)
            serializer = BasketSerializer(
                remaining_products, many=True, context={"basket_items": basket_items}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            basket = BasketSession(request)
            product = Product.objects.get(id=product_id)
            basket.remove(product, quantity=count)
            product_ids = list(basket.basket.keys())
            products = Product.objects.filter(id__in=product_ids)
            serializer = BasketSerializerSession(
                products, many=True, context={"basket": basket.basket}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)

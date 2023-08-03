from django.db.models import F
from django.db.models.functions import Round
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from main.serializers import ProductSerializer
from .models import PriceWinguardMain


class ProductByCategoryAndNumber(APIView):
    def get(self, request, category, number):
        if isinstance(category, int):
            category = [category]
        product = PriceWinguardMain.objects.filter(
            price_winguard_sketch__category__in=category,
            price_winguard_sketch__number=number
        ).annotate(
            percent=(F('price_winguard_sketch__id') % 3 + 1) * 10 + (F('price_winguard_sketch__id') % 2 * 5),
            stars_count=(F('price_winguard_sketch__id') % 10 + F('price_winguard_sketch__id') % 3 + F(
                'price_winguard_sketch__id') % 7 + F('price_winguard_sketch__id') % 5 + F(
                'price_winguard_sketch__id') % 11),
            path_folder=F('price_winguard_sketch__category'),
            path_file=F('price_winguard_sketch__number'),
            price=F('price_b2c'),
            saleprice=Round(F('price_b2c') / (1 - F('percent') / 100), -1)
        )
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data)

from django.db.models import F, Min, Max
from django.db.models.functions import Round
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from main.serializers import *
from .models import PriceWinguardMain, PriceWinguardSketch

# TODO(Drebedenb): add support for caching

class ProductByCategoryAndNumber(ListAPIView):
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
        serializer = ManyProductsSerializer(product, many=True)
        return Response(serializer.data)

class Products(ListAPIView):
    def get(self, request):
        # get parameters from /products?limit=1000&category_number=1...

        category_ids = request.query_params.getlist('category') or [1,2,3,4,5,6,7,8]
        category_ids = [int(cid) for cid in category_ids]
        min_price = int(request.GET.get('min_price') or 0)
        max_price = int(request.GET.get('max_price') or 9999999)
        order_by_name = request.GET.get('order_by_name') or 'id'
        order_scending = request.GET.get('order_scending') or 'asc'
        limit = int(request.GET.get('limit')  or 9999)
        order_by_name = order_by_name if order_scending == 'asc' else '-' + order_by_name
        queryset = PriceWinguardMain.objects.filter(
            price_winguard_sketch__category__in=category_ids
        ).annotate(
            percent=(F('price_winguard_sketch__id') % 3 + 1) * 10 + (F('price_winguard_sketch__id') % 2 * 5),
            stars_count=(F('price_winguard_sketch__id') % 10 + F('price_winguard_sketch__id') % 3 + F(
                'price_winguard_sketch__id') % 7 + F('price_winguard_sketch__id') % 5 + F(
                'price_winguard_sketch__id') % 11),
            path_folder=F('price_winguard_sketch__category'),
            path_file=F('price_winguard_sketch__number'),
            price=F('price_b2c'),
            saleprice=Round(F('price_b2c') / (1 - F('percent') / 100), -1),
            popularity=F('price_winguard_sketch__popularity')
        ).values('price_winguard_sketch__id').annotate(
            id=F('price_winguard_sketch__id'),
            percent=Min('percent'),
            stars_count=Min('stars_count'),
            path_folder=Min('path_folder'),
            path_file=Min('path_file'),
            price=Min('price_b2c'),
            saleprice=Min('saleprice'),
            popularity=Min('popularity')
        ).filter(
            price__gt=min_price,
            price__lt=max_price
        ).order_by(f'{order_by_name}')[:limit]
        serializer = ManyProductsSerializer(queryset, many=True)
        return Response(serializer.data)

class MinPriceOfCategories(RetrieveAPIView):
    def get(self, request):
        category_ids = request.query_params.getlist('category') or [1, 2, 3, 4, 5, 6, 7, 8]
        category_ids = [int(cid) for cid in category_ids]
        min_price = \
            PriceWinguardMain.objects.filter(price_winguard_sketch__category__in=category_ids).aggregate(
                Min('price_b2c'))[
                'price_b2c__min']
        return Response({'min_price': min_price})

class MaxPriceOfCategories(RetrieveAPIView):
    def get(self, request):
        category_ids = request.query_params.getlist('category') or [1, 2, 3, 4, 5, 6, 7, 8]
        category_ids = [int(cid) for cid in category_ids]
        max_price = PriceWinguardMain.objects.filter(price_winguard_sketch__category__in=category_ids).values(
            'price_winguard_sketch__id') \
            .annotate(min_price=Min('price_b2c')).values('min_price').aggregate(Max('min_price'))['min_price__max']
        return Response({'max_price': max_price})

class CountOfProductsByCategory(RetrieveAPIView):
    def get(self, request):
        category_ids = request.query_params.getlist('category') or [1, 2, 3, 4, 5, 6, 7, 8]
        category_ids = [int(cid) for cid in category_ids]
        count = PriceWinguardSketch.objects.filter(category__in=category_ids).count()
        return Response({'count': count})

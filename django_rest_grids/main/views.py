from django.db.models import F, Min, Max
from django.db.models.functions import Round
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from django.core.cache import cache

from .serializers import ManyProductsSerializer
from .models import PriceWinguardMain, PriceWinguardSketch

TTL_OF_CACHE_SECONDS = 60 * 60 * 24


class ProductByCategoryAndNumber(RetrieveAPIView):
    def get(self, request, category, number):
        if isinstance(category, int):
            category = [category]

        cache_key = "product_" + str(category) + "_" + str(number)
        product = cache.get(cache_key)
        if product is None:
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
            product = ManyProductsSerializer(product, many=True).data
            cache.set(cache_key, product, TTL_OF_CACHE_SECONDS)
        return Response({'product': product})


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

        cache_key = "category_" + str(category_ids) + "_" + str(min_price) + \
                    str(max_price) + order_by_name + order_scending + str(limit)
        products_list = cache.get(cache_key)

        if products_list is None:
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
            products_list = ManyProductsSerializer(queryset, many=True).data
            cache.set(cache_key, products_list, TTL_OF_CACHE_SECONDS)
        return Response({'grids_list': products_list})


class MinPriceOfCategories(RetrieveAPIView):
    def get(self, request):
        category_ids = request.query_params.getlist('category') or [1, 2, 3, 4, 5, 6, 7, 8]
        category_ids = [int(cid) for cid in category_ids]

        cache_key = "min_price_" + str(category_ids)
        min_price = cache.get(cache_key)

        if min_price is None:
            min_price = \
                PriceWinguardMain.objects.filter(price_winguard_sketch__category__in=category_ids).aggregate(
                    Min('price_b2c'))[
                    'price_b2c__min']
            cache.set(cache_key, min_price, TTL_OF_CACHE_SECONDS)
        return Response({'min_price': min_price})


class MaxPriceOfCategories(RetrieveAPIView):
    def get(self, request):
        category_ids = request.query_params.getlist('category') or [1, 2, 3, 4, 5, 6, 7, 8]
        category_ids = [int(cid) for cid in category_ids]

        cache_key = "max_price_" + str(category_ids)
        max_price = cache.get(cache_key)

        if max_price is None:
            max_price = PriceWinguardMain.objects.filter(price_winguard_sketch__category__in=category_ids).values(
                'price_winguard_sketch__id') \
                .annotate(min_price=Min('price_b2c')).values('min_price').aggregate(Max('min_price'))['min_price__max']
            cache.set(cache_key, max_price, TTL_OF_CACHE_SECONDS)
        return Response({'max_price': max_price})


class CountOfProductsByCategory(RetrieveAPIView):
    def get(self, request):
        category_ids = request.query_params.getlist('category') or [1, 2, 3, 4, 5, 6, 7, 8]
        category_ids = [int(cid) for cid in category_ids]

        cache_key = "count_" + str(category_ids)
        count = cache.get(cache_key)

        if count is None:
            count = PriceWinguardSketch.objects.filter(category__in=category_ids).count()
            cache.set(cache_key, {'count': count}, TTL_OF_CACHE_SECONDS)
        return Response({'count': count})

from rest_framework import serializers
from .models import PriceWinguardMain


class ManyProductsSerializer(serializers.ModelSerializer):
    percent = serializers.IntegerField()
    stars_count = serializers.IntegerField()
    path_folder = serializers.IntegerField()
    path_file = serializers.IntegerField()
    price = serializers.IntegerField()
    saleprice = serializers.IntegerField()
    class Meta:
        model = PriceWinguardMain
        fields = ['id', 'price_winguard_sketch_id', 'percent', 'stars_count','path_folder','path_file', 'price', 'saleprice']
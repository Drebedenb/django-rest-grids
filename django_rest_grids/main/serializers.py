from rest_framework import serializers
from .models import PriceWinguardMain


class ManyProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceWinguardMain
        fields = ['id', 'price_winguard_sketch_id', 'percent', 'stars_count','path_folder','path_file', 'price', 'saleprice']
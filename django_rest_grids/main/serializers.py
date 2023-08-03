from rest_framework import serializers
from .models import PriceWinguardMain


class ProductSerializer(serializers.ModelSerializer):
    percent = serializers.IntegerField()
    stars_count = serializers.IntegerField()
    price = serializers.IntegerField()
    saleprice = serializers.IntegerField()

    class Meta:
        model = PriceWinguardMain
        fields = ['id', 'price_winguard_sketch_id', 'percent', 'stars_count', 'price', 'saleprice']
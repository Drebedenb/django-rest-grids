from rest_framework import serializers
from .models import PriceWinguardMain


class PriceWinguardMainSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceWinguardMain
        fields = ['id', 'price_winguard_sketch_id', 'price_b2c', 'name']
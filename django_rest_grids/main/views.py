from rest_framework import generics
from . import serializers
from main.serializers import PriceWinguardMainSerializer
from .models import PriceWinguardMain

class PriceWinguardMainList(generics.ListCreateAPIView):
    queryset = PriceWinguardMain.objects.all()
    serializer_class = serializers.PriceWinguardMainSerializer



# class PostDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = serializers.PostSerializer
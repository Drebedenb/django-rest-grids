from django.urls import path
from .views import *

urlpatterns = [
    path('mainGrids/', PriceWinguardMainList.as_view()),
]
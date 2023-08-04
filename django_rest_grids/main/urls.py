from django.urls import path
from .views import *

urlpatterns = [
    path('products/<int:category>/<int:number>/', ProductByCategoryAndNumber.as_view()),
    path('products', Products.as_view()),
    path('min_price', MinPriceOfCategories.as_view()),
    path('max_price', MaxPriceOfCategories.as_view()),
    path('count', CountOfProductsByCategory.as_view()),
]
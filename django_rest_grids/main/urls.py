from django.urls import path
from .views import *

urlpatterns = [
    path('products/<int:category>/<int:number>/', ProductByCategoryAndNumber.as_view())
]
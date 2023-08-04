from django.db import models


class PriceWinguardMain(models.Model):
    price_winguard_sketch = models.ForeignKey('PriceWinguardSketch', on_delete=models.PROTECT)
    salary = models.IntegerField()
    price_b2c = models.IntegerField()
    price_b2b = models.IntegerField()
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'price_winguard_main'


class PriceWinguardSketch(models.Model):
    category = models.IntegerField()
    number = models.IntegerField()
    popularity = models.IntegerField()
    orders = models.IntegerField()
    date = models.DateField()
    variants = models.IntegerField()
    active = models.IntegerField()
    min_price_for_sort = models.IntegerField()

    class Meta:
        db_table = 'price_winguard_sketch'
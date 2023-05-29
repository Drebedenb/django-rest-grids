from django.db import models


class PriceWinguardMain(models.Model):
    price_winguard_sketch = models.ForeignKey('PriceWinguardSketch', on_delete=models.PROTECT)
    salary = models.IntegerField()
    price_b2c = models.IntegerField()
    price_b2b = models.IntegerField()
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'price_winguard_main'


class PriceWinguardFiles(models.Model):
    price_winguard_FilesType_id = models.IntegerField()
    price_winguard_sketch = models.ForeignKey('PriceWinguardSketch', on_delete=models.PROTECT)
    path = models.CharField(max_length=255)

    class Meta:
        db_table = 'price_winguard_files'



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
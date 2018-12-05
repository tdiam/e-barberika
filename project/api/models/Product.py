from django.db import models

class Product(models.Model):
    # Model for product
    # Contains name, price and store name
    product_name = models.CharField(max_length=50)
    store_name = models.CharField(max_length=50)
    price = models.DecimalField()

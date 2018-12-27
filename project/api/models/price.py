from django.db import models
from django.contrib.auth import get_user_model

class Shop_tmp(models.Model):
    pass

class Product_tmp(models.Model):
    pass

#########################

class Price(models.Model):
    shop = models.ForeignKey(Shop_tmp, on_delete=models.CASCADE)
    product = models.ForeignKey(Product_tmp, on_delete=models.CASCADE)

    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)

    price = models.DecimalField(decimal_places=2, max_digits=10)

    date_from = models.DateField(auto_now=False, auto_now_add=True)
    date_to = models.DateField(null=True, default=None)

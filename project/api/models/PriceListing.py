from django.db import models
from django.contrib.auth.models import User

class shopplaceholder(models.Model):
    pass

class productplaceholder(models.Model):
    pass

class prices(models.Model):
    # These should be replaced with the actual models
    shop = models.ForeignKey(shopplaceholder, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(productplaceholder, on_delete=models.CASCADE, null=True)
    # NOTE : should we delete when the user is deleted ?
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    price = models.DecimalField(decimal_places=2, max_digits=10)

    date_inserted = models.DateField(auto_now=False, auto_now_add=True)
    date_invalidated = models.DateField(null=True, default=None)

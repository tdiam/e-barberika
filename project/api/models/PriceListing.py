from django.db import models

class PriceListing(models.Model):
    # These should be replaced with the actual models
    store_name = models.CharField(max_length=50)
    product_name = models.CharField(max_length=50)
    user_name = models.CharField(max_length=50)

    price = models.DecimalField(decimal_places=2, max_digits=10)

    date_inserted = models.DateField()
    date_invalidated = models.DateField()

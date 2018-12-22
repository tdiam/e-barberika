from django.contrib import admin
from .models import prices, shopplaceholder, productplaceholder

# Register Price Listing model
admin.site.register(prices)
admin.site.register(shopplaceholder)
admin.site.register(productplaceholder)

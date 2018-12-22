from django.contrib import admin

# Register your models here.
from .models import Shop, ShopTag


admin.site.register(Shop)
admin.site.register(ShopTag)

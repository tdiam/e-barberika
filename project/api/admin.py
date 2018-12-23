from django.contrib import admin

# Register your models here.
from .models import Shop, ShopTag

from .models import Price


admin.site.register(Shop)
admin.site.register(ShopTag)

admin.site.register(Price)
from django.contrib import admin
from products.models import Product, ProductLocalData, ProductExtraField


admin.site.register(Product)
admin.site.register(ProductLocalData)
admin.site.register(ProductExtraField)

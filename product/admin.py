from django.contrib import admin
from product.models import MainCategory, Category, SubCategory, AdditionalInformation, Product, Review

# Register your models here.
admin.site.register(MainCategory)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(AdditionalInformation)
admin.site.register(Product)
admin.site.register(Review)
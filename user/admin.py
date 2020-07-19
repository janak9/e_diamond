from django.contrib import admin
from user.models import Address, Cart, Compare, Feedback, Wishlist, Order

# Register your models here.
admin.site.register(Address)
admin.site.register(Cart)
admin.site.register(Compare)
admin.site.register(Feedback)
admin.site.register(Wishlist)
admin.site.register(Order)
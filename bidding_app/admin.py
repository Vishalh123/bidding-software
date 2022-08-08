from django.contrib import admin
from . models import AddProduct, BidProduct


# Register your models here.
@admin.register(AddProduct)
class AddProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'name', 'description')

admin.site.register(BidProduct)
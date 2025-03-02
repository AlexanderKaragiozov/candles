from django.contrib import admin

# Register your models here.

from .models import Candle,Gallery,CandleOrder,Customer

@admin.register(Candle)
class CandleAdmin(admin.ModelAdmin):
    list_display = ('name','cent', 'description', 'price', 'image','date_added','reviews')

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['image']

@admin.register(CandleOrder)
class CandleOrder(admin.ModelAdmin):
    pass

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass
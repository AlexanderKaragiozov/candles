from django.contrib import admin

# Register your models here.

from .models import Candle,Gallery,CandleOrder,Customer

@admin.register(Candle)
class CandleAdmin(admin.ModelAdmin):
    list_display = ('name','cent', 'description', 'price', 'image','date_added','reviews')
    list_filter = ('monthly',)  # Add filter for 'monthly'
    search_fields = ('name', 'cent')  # Add search functionality
    fieldsets = (
        ("Основна информация", {
            "fields": ("name", "description", "cent"),
        }),
        ("Цени и наличности", {
            "fields": ("price", "promotion_price", "quantity"),
        }),
        ("Изображения 1-вото задължително!", {
            "fields": ("image", "image_2", "image_3", "image_4"),
            "classes": ("collapse",),
        }),
        ("Ако е Месечна Кутия", {
            "fields": ("monthly", "end_date"),
            "classes": ("collapse",),
        }),
        ("Други : Незадължително", {
            "fields": ("reviews",),
            "classes": ("collapse",),
        }),
    )
@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['image']

@admin.register(CandleOrder)
class CandleOrder(admin.ModelAdmin):
    list_display = ('customer','candle','quantity','confirmed','order_date')
    list_filter = ('confirmed',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass
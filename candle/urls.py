from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Your main view
    path('gallery/' , views.gallery, name='gallery'),
    path('products/', views.products, name='products'),
    path('view_product/<int:candle_id>/', views.view_product, name='view_product'),
    path('fast_buy/<int:candle_id>/', views.fast_buy, name='fast_buy'),
    path('order_complete/<str:order_url_code>/', views.order_complete, name='order_complete'),
    path('place_order/', views.place_order, name='place_order'),
    path('request_help/', views.request_help, name='request_help'),
    path('add_to_cart/<int:candle_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart_view/', views.cart_view, name='cart_view'),
    path('increase-quantity/<int:candle_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease-quantity/<int:candle_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('remove-from-cart/<int:candle_id>/', views.remove_from_cart, name='remove_from_cart'),

]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
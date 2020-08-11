from django.urls import path

from . import views

app_name = 'baskets'

urlpatterns = [
    path('basket/', views.BasketAPIView.as_view(), name='basket'),
    path('basket/share/', views.BasketShareAPIView.as_view(), name='basket-share'),
    path('basket/products/<uuid:product_id>/', views.BasketProductsAPIView.as_view(), name='basket-products'),
]

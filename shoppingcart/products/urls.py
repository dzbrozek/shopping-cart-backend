from rest_framework.routers import DefaultRouter

from . import views

app_name = 'products'

router = DefaultRouter()

router.register(r'products', views.ProductViewSet, basename='product')

urlpatterns = router.urls

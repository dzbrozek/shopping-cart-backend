from __future__ import annotations

from django.db.models import QuerySet
from products.models import Product
from products.serializers import ProductSerializer
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from utils.permissions import IsAdmin
from utils.views import ActionConfigViewSetMixin


class ProductViewSet(
    ActionConfigViewSetMixin, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, GenericViewSet
):
    serializer_class = ProductSerializer
    action_config = {
        'create': {'permission_classes': [IsAuthenticated, IsAdmin], 'authentication_classes': [SessionAuthentication]},
        'destroy': {
            'permission_classes': [IsAuthenticated, IsAdmin],
            'authentication_classes': [SessionAuthentication],
        },
    }
    lookup_field = 'uuid'

    def get_queryset(self) -> QuerySet[Product]:
        return Product.objects.all()

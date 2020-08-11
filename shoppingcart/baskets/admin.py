from baskets.models import Basket, BasketProductRelation
from django.contrib import admin


@admin.register(BasketProductRelation)
class BasketProductRelationAdmin(admin.ModelAdmin):
    list_display = ('id', 'uuid', 'product', 'basket', 'quantity')
    search_fields = ('id', 'uuid')
    raw_id_fields = ('product', 'basket')


class BasketProductRelationInline(admin.TabularInline):
    model = BasketProductRelation
    raw_id_fields = ('product',)


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('id', 'uuid')
    search_fields = ('id', 'uuid')
    list_filter = ('updated',)
    inlines = [BasketProductRelationInline]

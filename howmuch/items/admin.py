from django.contrib import admin
from howmuch.items.models import ItemsCatA, ItemsCatB, ItemsCatC

admin.site.register(ItemsCatA)
admin.site.register(ItemsCatB)
admin.site.register(ItemsCatC)
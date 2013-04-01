#!/usr/bin/env python
import os

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "howmuch.localsettings")

from howmuch.category.models import Category
Category.objects.create(name="videojuegos")
Category.objects.create(name="hogar")
Category.objects.create(name="electrodomesticos")
Category.objects.create(name="peliculas_series_dvds")
Category.objects.create(name="electronica_accesorios")
Category.objects.create(name="celulares_accesorios")
Category.objects.create(name="ropa_accesorios")
Category.objects.create(name="libros_revistas")
Category.objects.create(name="coleccionables")
Category.objects.create(name="computacion_accesorios")
Category.objects.create(name="instrumentos_musicales")
Category.objects.create(name="juguetes")
Category.objects.create(name="joyas_relojes")
from django.db import models

import tagging

class Category(models.Model):
	name = models.CharField(max_length=25)


tagging.register(Category)

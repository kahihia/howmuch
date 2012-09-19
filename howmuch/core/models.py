from django.db import models
from django.contrib.auth.models import User

class RequestItem(models.Model):
	price = models.IntegerField()
	title = models.CharField(max_length=100, help_text="Titulo del Articulo que quieres")
	description = models.CharField(max_length=140)
	model = models.CharField(max_length=25)

	def __unicode__(self):
		return self.title



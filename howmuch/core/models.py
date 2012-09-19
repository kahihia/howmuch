from django.db import models
from django.contrib.auth.models import User
from howmuch.Pictures.models import Picture

STATES_CHOICES = (
	('NEW' , 'NUEVO'),
	('USED' , 'USADO'),
)

class RequestItem(models.Model):
	owner = models.ForeignKey(User, related_name = "owner by RequestItem")
	price = models.IntegerField()
	title = models.CharField(max_length=100, help_text="Titulo del Articulo que quieres")
	description = models.CharField(max_length=140)
	brand = models.CharField(max_length=25)
	model = models.CharField(max_length=25)
	state = models.CharField(max_length=7, choices=STATES_CHOICES)
	duedate = models.DateTimeField()
	pictures = models.ManyToManyField(Picture, through='RequestItemPicture')

	def __unicode__(self):
		return self.title

class RequestItemPicture(models.Model):
	requestItem = models.ForeignKey(RequestItem)
	picture = models.ForeignKey(Picture)

	def __unicode__(self):
		return self.requestItem.title

class Proffer(models.Model):
	owner = models.ForeignKey(User, related_name = "owner by Proffer")
	date = models.DateTimeField()
	cprice = models.IntegerField()
	message = models.CharField(max_length=140)
	pictures = models.ManyToManyField(Picture, through='ProfferPicture')

	def __unicode__(self):
		return self.owner

class ProfferPicture(models.Model):
	proffer = models.ForeignKey(Proffer)
	picture = models.ForeignKey(Picture)

	def __unicode__(self):
		return self.proffer

class Assignment(models.Model):
	owner = models.ForeignKey(User)
	requestItem = models.ForeignKey(RequestItem)
	date = models.DateTimeField()







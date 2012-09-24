from django.db import models
from django.contrib.auth.models import User
from howmuch.Pictures.models import Picture

STATES_CHOICES = (

	('NEW' , 'NUEVO'),
	('USED' , 'USADO'),

)

STATUS_ASSIGNMENT = (

	('1', 'PAGADO'),
	('2', 'ENVIADO'),
	('3', 'COMPLETADO'),
	('4','CALIFICADO'),
	('5', 'CANCELADO')

)

class RequestItem(models.Model):
	owner = models.ForeignKey(User, related_name = "owner by RequestItem")
	price = models.IntegerField()
	title = models.CharField(max_length=100)
	description = models.CharField(max_length=140)
	brand = models.CharField(max_length=25)
	model = models.CharField(max_length=25)
	state = models.CharField(max_length=7, choices=STATES_CHOICES)
	date = models.DateTimeField(auto_now_add=True)
	duedate = models.DateTimeField()
	pictures = models.ManyToManyField(Picture, through='RequestItemPicture', blank=True)
	addressDelivery = models.CharField(max_length=177)

	def __unicode__(self):
		return self.title

class RequestItemPicture(models.Model):
	requestItem = models.ForeignKey(RequestItem)
	picture = models.ForeignKey(Picture)

	def __unicode__(self):
		return self.requestItem.title

class Proffer(models.Model):
	owner = models.ForeignKey(User, related_name = "owner by Proffer")
	requestItem = models.ForeignKey(RequestItem)
	date = models.DateTimeField(auto_now_add=True)
	cprice = models.IntegerField()
	message = models.CharField(max_length=140)
	pictures = models.ManyToManyField(Picture, through='ProfferPicture')

	def __unicode__(self):
		return u'owner: %s, item: %s' % (self.owner, self.requestItem.title)

class ProfferPicture(models.Model):
	proffer = models.ForeignKey(Proffer)
	picture = models.ForeignKey(Picture)

	def __unicode__(self):
		return self.proffer

class Assignment(models.Model):
	owner = models.ForeignKey(User)
	requestItem = models.ForeignKey(RequestItem)
	date = models.DateTimeField(auto_now_add=True)
	duedate = models.DateTimeField(null=True, blank=True)
	status = models.CharField(max_length=2, choices=STATUS_ASSIGNMENT)

	def __unicode__(self):
		return u'%s and %s' % (self.owner, self.requestItem)







# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from howmuch.backend.functions import get_timestamp

TYPE_CHOICES = (

	('proffer','Tienes un nuevo Candidato'),
	('assignment','Has sido seleccionado'),
	('confirm_pay','Te han confirmado el pago'),
	('confirm_delivery','Te han confirmado el envio'),
	('critique','Has sido criticado'),

	)

class Notification(models.Model):
	owner = models.ForeignKey(User)
	tipo = models.CharField(max_length=20)
	title = models.CharField(max_length=140)
	has_been_readed = models.BooleanField(default=False)
	redirect = models.CharField(max_length=140)
	date = models.DateTimeField(auto_now_add = True)
	idBack = models.IntegerField()

	def __unicode__(self):
		return u'%s' % (self.title)

	def get_timestamp(self):
		return get_timestamp(self.date)




# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from howmuch.core.models import Assignment

PRESTIGE_CHOICES = (
	('0','MALO'),
	('1','EXCELENTE'),
	)

STATUS_ASSIGNMENT = (

	('0', 'NOTIFICADO'), #Cuando la Asignacion es generada
	('1', 'PAGADO'), #Cuando el comprador notifica el pago
	('2', 'PRODUCTO ENVIADO'), #Cuando el vendedor notifica el Envio del producto, ya permite que los usuarios CRITIQUEN
	('3','EN ESPERA DE CRITICA'), #Se activa en el momento en que cualquiera de los involucrados CRITICA la transaccion
	('4', 'COMPLETADO'), #Cuando ya existe CRITICA tanto del comprador como del vendedor
	('5', 'CANCELADO') #Cuando se cancela la transaccion

)

class PayConfirm(models.Model):
	owner = models.ForeignKey(User, related_name = "owner by Confirm Pay")
	assignment = models.ForeignKey(Assignment)
	date = models.DateTimeField(auto_now_add = True)
	amount = models.IntegerField()
	message = models.CharField(max_length = 255)

	def __unicode__(self):
		return u'Assignment : %s message: %s ' % (self.assignment, self.message)

class DeliveryConfirm(models.Model):
	owner = models.ForeignKey(User, related_name = "owner by Confirm Delivery")
	assignment = models.ForeignKey(Assignment)
	date = models.DateTimeField(auto_now_add = True)
	message = models.CharField(max_length = 255)

	def __unicode__(self):
		return u'Assignment : %s message: %s ' % (self.assignment, self.message)

class Prestige(models.Model):
	de = models.ForeignKey(User, related_name = "prestige from")
	to = models.ForeignKey(User, related_name = "prestige to")
	assignment = models.ForeignKey(Assignment)
	date = models.DateTimeField(auto_now_add = True)
	prestige = models.CharField(max_length = 2, choices = PRESTIGE_CHOICES)
	message = models.CharField(max_length = 255)

	def __unicode__(self):
		return u'Assignment : %s Prestige: %s message: %s ' % (self.assignment, self.prestige, self.message)

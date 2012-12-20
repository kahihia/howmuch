# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from howmuch.core.models import Assignment
from howmuch.pictures.models import make_upload_path
from howmuch.pictures.thumbs import ImageWithThumbsField

PRESTIGE_CHOICES = (
    ('Malo','MALO'),
    ('Excelente','EXCELENTE'),
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
    picture = ImageWithThumbsField(upload_to=make_upload_path, sizes=((100,100),(250,250)), blank=True )

    def __unicode__(self):
        return u'Assignment : %s message: %s ' % (self.assignment, self.message)

    def get_picture_url_100x100(self):
        return str(self.picture.url_100x100.split("?")[0])

class DeliveryConfirm(models.Model):
    owner = models.ForeignKey(User, related_name = "owner by Confirm Delivery")
    assignment = models.ForeignKey(Assignment)
    date = models.DateTimeField(auto_now_add = True)
    message = models.CharField(max_length = 255)
    picture = ImageWithThumbsField(upload_to=make_upload_path, sizes=((100,100),(250,250)), blank=True )

    def __unicode__(self):
        return u'Assignment : %s message: %s ' % (self.assignment, self.message)

    def get_picture_url_100x100(self):
        return str(self.picture.url_100x100.split("?")[0])

class PrestigeLikeBuyer(models.Model):
    de = models.ForeignKey(User, related_name = "prestigeLikeBuyer from")
    to = models.ForeignKey(User, related_name = "prestigeLikeBuyer to")
    assignment = models.ForeignKey(Assignment)
    date = models.DateTimeField(auto_now_add = True)
    prestige = models.CharField(max_length = 10, choices = PRESTIGE_CHOICES)
    message = models.CharField(max_length = 255)

    def __unicode__(self):
        return u'Assignment : %s Prestige: %s message: %s ' % (self.assignment, self.prestige, self.message)


class PrestigeLikeSeller(models.Model):
    de = models.ForeignKey(User, related_name = "prestigeLikeSeller from")
    to = models.ForeignKey(User, related_name = "prestigeLikeSeller to")
    assignment = models.ForeignKey(Assignment)
    date = models.DateTimeField(auto_now_add = True)
    prestige = models.CharField(max_length = 10, choices = PRESTIGE_CHOICES)
    message = models.CharField(max_length = 255)

    def __unicode__(self):
        return u'Assignment : %s Prestige: %s message: %s ' % (self.assignment, self.prestige, self.message)



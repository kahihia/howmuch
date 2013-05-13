from django.contrib.auth.models import User
from django.db import models

from howmuch.article.models import Assignment
from howmuch.pictures.models import make_upload_path

CRITIQUE_CHOICES = (
    ('M','MALO'),
    ('E','EXCELENTE'),
    )

STATUS_ASSIGNMENT = (

    ('0', 'NOTIFICADO'), #Cuando la Asignacion es generada
    ('1', 'PAGADO'), #Cuando el comprador notifica el pago
    ('2', 'PRODUCTO ENVIADO'), #Cuando el vendedor notifica el Envio del producto, ya permite que los usuarios CRITIQUEN
    ('3','EN ESPERA DE CRITICA'), #Se activa en el momento en que cualquiera de los involucrados CRITICA la transaccion
    ('4', 'COMPLETADO'), #Cuando ya existe CRITICA tanto del comprador como del vendedor
    ('5', 'CANCELADO') #Cuando se cancela la transaccion

)

class ConfirmPay(models.Model):
    owner = models.ForeignKey(User, related_name = "owner by Confirm Pay")
    assignment = models.ForeignKey(Assignment)
    date = models.DateTimeField(auto_now_add = True)
    amount = models.IntegerField()
    message = models.CharField(max_length = 1024)
    picture = models.ImageField(upload_to=make_upload_path, blank=True)

    def __unicode__(self):
        return u'Assignment : %s message: %s ' % (self.assignment, self.message)


class ConfirmDelivery(models.Model):
    owner = models.ForeignKey(User, related_name = "owner by Confirm Delivery")
    assignment = models.ForeignKey(Assignment)
    date = models.DateTimeField(auto_now_add = True)
    message = models.CharField(max_length = 1024)
    picture = models.ImageField(upload_to=make_upload_path, blank=True )

    def __unicode__(self):
        return u'Assignment : %s message: %s ' % (self.assignment, self.message)


class Critique(models.Model):
    de = models.ForeignKey(User, related_name = "prestigeLikeBuyer from")
    to = models.ForeignKey(User, related_name = "prestigeLikeBuyer to")
    assignment = models.ForeignKey(Assignment)
    date = models.DateTimeField(auto_now_add = True)
    critique = models.CharField(max_length = 10, choices = CRITIQUE_CHOICES)
    message = models.CharField(max_length = 1024)

    def __unicode__(self):
        return u'Assignment : %s Critique: %s message: %s ' % (self.assignment, self.critique, self.message)



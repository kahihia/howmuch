import datetime

from django.db import models
from django.contrib.auth.models import User

from howmuch.pictures.models import Picture
from howmuch.profile.models import Address
from howmuch.utils import get_timestamp



STATES_CHOICES = (

    ('NUEVO' , 'NUEVO'),
    ('USADO' , 'USADO'),

)

STATUS_ASSIGNMENT = (
    ('0', 'NOTIFICADO'), #Cuando la Asignacion es generada
    ('1', 'PAGADO'), #Cuando el comprador notifica el pago
    ('2', 'PRODUCTO ENVIADO'), # Cuando el vendedor notifica el Envio del producto, ya permite que los usuarios CRITIQUEN
    ('3','EN ESPERA DE CRITICA'), #Se activa en el momento en que cualquiera de los involucrados CRITICA la transaccion
    ('4', 'COMPLETADO'), #Cuando ya existe CRITICA tanto del comprador como del vendedor
    ('5', 'CANCELADO') #Cuando se cancela la transaccion

)

DAYS_CHOICES = (
    (1, 'UN DIA'),
    (5, 'CINCO'),
    (10, 'DIEZ'),
    (30, 'TREINTA'),
    )

CATEGORY_CHOICES = (
    ('categoria1', 'categoria1'),
    ('categoria2', 'categoria2'),
    ('categoria3', 'categoria3'),
    ('categoria4', 'categoria4'),
    ('categoria5', 'categoria5'),
    )

class Article(models.Model):
    owner = models.ForeignKey(User, related_name = "owner by article")
    price = models.IntegerField()
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1024)
    quantity = models.IntegerField() 
    category = models.CharField(max_length=15, choices=CATEGORY_CHOICES)
    state = models.CharField(max_length=7, choices=STATES_CHOICES)
    date = models.DateTimeField(auto_now_add=True)
    addressDelivery = models.ForeignKey(Address)
    title_url = models.CharField(max_length=100, null=True, blank = True)

    def __unicode__(self):
        return u'Title: %s' % (self.title)

    #True si el item ya posee candidatos
    def has_candidates(self):
        if Offer.objects.filter(article = self).exists():
            return True
        else:
            return False

    def getNumber_candidates(self):
        return Offer.objects.filter(article = self).count()

    #True si el item ya posee asignacion
    def has_assignment(self):
        try:
            Assignment.objects.get(article = self)
        except Assignment.DoesNotExist:
            return False
        return True

    #True si el item ya ha finalizado
    def has_been_completed(self):
        try:
            assignment = Assignment.objects.get(article = self)
        except Assignment.DoesNotExist:
            return False
        if assignment.status == "4":
            return True
        return False

    def get_first_100_letters(self):
        return str(self.title)[:100]

    #Regresa el link de la primer imagen en miniatura 100x100 del item
    def get_first_picture_100x100(self):
        for p in self.pictures.all()[:1]:
            return p.get_url_100x100()

    #Regresa el link de la primer imagen en miniatura 250x250 del item
    def get_first_picture_250x250(self):
        for p in self.pictures.all()[:1]:
            return p.get_url_250x250()

    def get_url(self):
        return '/article/%s/%s' % (self.pk, self.title_url)

    def get_timestamp(self):
        return get_timestamp(self.date)


class Offer(models.Model):
    owner = models.ForeignKey(User, related_name = "owner by Offer")
    article = models.ForeignKey(Article)
    date = models.DateTimeField(auto_now_add=True)
    #Precio contra oferta
    cprice = models.IntegerField() 
    message = models.CharField(max_length=140)
    pictures = models.ManyToManyField(Picture)

    def __unicode__(self):
        return u'owner: %s, item: %s' % (self.owner, self.article.title)

    def is_open(self):
        try:
            Assignment.objects.get(article = self.article)
        except Assignment.DoesNotExist:
            return True
        return False

    def get_first_picture_100x100(self):
        for p in self.pictures.all()[:1]:
            return p.get_url_100x100()

    def get_first_picture_250x250(self):
        for p in self.pictures.all()[:1]:
            return p.get_url_250x250()

    def is_complete(self):
        if self.pictures.all().count() > 0:
            return True
        return False

    def has_pictures(self):
        if self.pictures.all().count() > 0:
            return True
        return False


class Assignment(models.Model):
    owner = models.ForeignKey(User)
    article = models.OneToOneField(Article)
    date = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=144)
    status = models.CharField(max_length=2, default = 0)

    def __unicode__(self):
        return u'Owner: %s and item: %s' % (self.owner, self.article)

    #True si el usuario dado es el vendedor del articulo
    def is_seller(self,user):
        if self.owner == user:
            return True
        else: 
            return False

    #True si el usuario dado es el comprador del articulo
    def is_buyer(self,user):
        if self.article.owner == user:
            return True
        else:
            return False

    #Regresa al comprador
    def get_buyer(self):
        return self.article.owner

    #Regresa al vendedor
    def get_seller(self):
        return self.owner

    #True si el usuario dado es comprador o vendedor
    def is_inside(self,user):
        if self.is_seller(user) or self.is_buyer(user):
            return True
        return False

    #True si en esta asignacion el comprador o vendedor ha criticado a su contraparte
    def has_been_critiqued_before(self):
        if self.status == "3":
            return True
        return False

    #True si la transaccion ha finalizado con exito
    def is_complete(self):
        if self.status == "4":
            return True
        return False














import datetime

from django.db import models
from django.contrib.auth.models import User


from howmuch.pictures.models import Picture
from howmuch.profile.models import Address
from howmuch.utils import get_timestamp
from howmuch.comments.models import Comment
from howmuch.tags.models import Tag
from howmuch.settings import URL_OFFICIAL_SITE



STATES_CHOICES = (

    ('Nuevo' , 'Nuevo'),
    ('Usado' , 'Usado'),
    ('Indistinto', 'Indistinto'),

)

QUANTITY_CHOICES = (
    (1,'1'),
    (2,'Entre 2 y 5'),
    (5,'Entre 5 y 10'),
    (10,'Mas de 10'),
    )

STATUS_ASSIGNMENT = (
    ('1', 'NOTIFICADO'), #Cuando la Asignacion es generada
    ('2', 'PAGADO'), #Cuando el comprador notifica el pago
    ('3', 'PRODUCTO ENVIADO'), # Cuando el vendedor notifica el Envio del producto, ya permite que los usuarios CRITIQUEN
    ('4','EN ESPERA DE CRITICA'), #Se activa en el momento en que cualquiera de los involucrados CRITICA la transaccion
    ('5', 'COMPLETADO'), #Cuando ya existe CRITICA tanto del comprador como del vendedor
    ('6', 'CANCELADO') #Cuando se cancela la transaccion
)

DAYS_CHOICES = (
    (1, 'UN DIA'),
    (5, 'CINCO'),
    (10, 'DIEZ'),
    (30, 'TREINTA'),
    )

CATEGORY_CHOICES = (
    ('1', 'categoria1'),
    ('2', 'categoria2'),
    ('3', 'categoria3'),
    ('4', 'categoria4'),
    ('5', 'categoria5'),
    )

class Article(models.Model):
    owner = models.ForeignKey(User, related_name = "owner by article")
    price = models.IntegerField()
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1024)
    quantity = models.IntegerField(choices=QUANTITY_CHOICES) 
    category = models.CharField(max_length=15, choices=CATEGORY_CHOICES)
    state = models.CharField(max_length=7, choices=STATES_CHOICES)
    tags = models.ManyToManyField(Tag)
    date = models.DateTimeField(auto_now_add=True)
    pictures = models.ManyToManyField(Picture)
    title_url = models.CharField(max_length=100, null=True, blank=True)
    comments = models.ManyToManyField(Comment, blank=True)
    followers = models.ManyToManyField(User, blank=True)
    is_active = models.BooleanField(default=True)


    def __unicode__(self):
        return u'Title: %s' % (self.title)

    #True si el item ya posee candidatos
    def has_candidates(self):
        if Offer.objects.filter(article = self).exists():
            return True
        return False


    #Regresa el numero de candidatos que han aplicado a este articulo
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


    #Regresa la URL de la primer imagen
    def get_first_picture_url(self):
        for p in self.pictures.all()[:1]:
            return p.get_url()


    #Regresa la URL del articulo
    def get_url(self):
        return '/article/%s/%s' % (self.pk, self.title_url)


    #Regresa una lista de Tags
    def get_list_tags(self):
        from howmuch.article.functions import tags_to_string
        return tags_to_string(self.tags.all())


    #Regresa hace que tiempo fue publicado el articulo        
    def get_timestamp(self):
        return get_timestamp(self.date)


class Offer(models.Model):
    owner = models.ForeignKey(User, related_name = "owner by Offer")
    article = models.ForeignKey(Article)
    date = models.DateTimeField(auto_now_add=True)
    #Precio contra oferta
    quantity = models.IntegerField(choices=QUANTITY_CHOICES) 
    cprice = models.IntegerField() 
    message = models.CharField(max_length=1024)
    pictures = models.ManyToManyField(Picture)

    def __unicode__(self):
        return u'owner: %s, item: %s' % (self.owner, self.article.title)

    #Regresa True si el articulo al que se hace referencia aun no tiene asignacion
    def is_open(self):
        try:
            Assignment.objects.get(article = self.article)
        except Assignment.DoesNotExist:
            return True
        return False

    def get_first_picture_url(self):
        for p in self.pictures.all()[:1]:
            return p.picture.url
            

    #Regresa hace que tiempo fue publicado el articulo        
    def get_timestamp(self):
        return get_timestamp(self.date)

    #Regresa la URL de la oferta, la podra ver unicamente el comprador del articulo
    def get_url(self):
        return URL_OFFICIAL_SITE + '/article/offer/view/%s' % (self.pk)


class Assignment(models.Model):
    owner = models.ForeignKey(User)
    article = models.OneToOneField(Article)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2, default = 1)

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














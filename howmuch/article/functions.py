from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.core.files import File

from howmuch.article.models import Article, Offer, Assignment
from howmuch.prestige.models import ConfirmPay, ConfirmDelivery, Critique
from howmuch.messages.models import Conversation
from howmuch.pictures.models import Picture


class AboutArticle(object):
    def __init__(self, user, articleID):
        self.user = user
        self.articleID = articleID

    #Regresa True si el Usuario es publico el Articulo dado su id
    def is_owner(self):
        try:
            Article.objects.get(owner = self.user, pk=self.articleID)
        except Article.DoesNotExist:
            return False
        return True 

    #Regresa True si el Usuario es Candidato de la publicacion del articulo dado su id, Es cuando el usuario da click en VENDER
    def is_candidate(self):
        try:
            Offer.objects.get(owner = self.user, article = self.articleID)
        except Offer.DoesNotExist:
            return False
        return True

    #Regresa True si el Usuario ha sido Asignado para completar el RequestItem (De los que dieron click en VENDER, es el que fue elegido)
    def is_assigned(self):
        try:
            Assignment.objects.get(article = self.articleID)
        except Assignment.DoesNotExist:
            return False
        return True

    #Regresa los Errores encontrados a la hora de realizar de intentar VENDER el articulo
    def errors(self):
        errors = []
        if self.is_owner():
            errors.append("Esta Solicitud fue publicada por ti y tu no puedes vendertela a ti mismo")
        elif self.is_assigned():
            errors.append("Este Articulo ya tiene Asignado un Vendedor, lo sentimos mucho")
        elif self.is_candidate():
            errors.append("Tu ya eres un Vendedor Candidaro, no puedes volver a serlo para este mismo articulo")
        
        return errors

    #Regresa False en caso de que Sea Propietario, Candidato o Asignado dado el id del RequestItem
    def is_valid(self):
        if self.is_owner() or self.is_candidate() or self.is_assigned():
            return False
        return True

class AboutAssignment(object):
    def __init__(self, assignment):
        self.assignment = assignment

    def has_been_paid(self):
        try:
            ConfirmPay.objects.get(assignment = self.assignment)
        except ConfirmPay.DoesNotExist:
            return False
        return True

    def has_been_delivered(self):
        try:
            ConfirmDelivery.objects.get(assignment = self.assignment)
        except ConfirmDelivery.DoesNotExist:
            return False
        return True

    def has_been_critiqued_by_buyer(self):
        try:
            Critique.objects.get(assignment = self.assignment, de = self.assignment.article.owner )
        except Critique.DoesNotExist:
            return False
        return True

    def has_been_critiqued_by_seller(self):
        try:
            Critique.objects.get(assignment = self.assignment, de = self.assignment.owner )
        except Critique.DoesNotExist:
            return False
        return True

    def user_has_critiqued(self, user):
        if self.assignment.is_buyer(user) and has_been_critiqued_by_buyer():
            return True
        elif self.assignment.is_seller(user) and has_been_critiqued_by_seller():
            return True
        return False

    def is_in_process(self):
        if self.assignment.status in ["0", "1", "2", "3"]:
            return True
        return False

#More Functions used in article views

def validate_assignment(articleID,request):
    #Validar que el item exista y que el owner de el sea el request.user
    try:
        article = Article.objects.get(pk= articleID, owner=request.user)
    except Article.DoesNotExist:
        return HttpResponse("No tienes permiso para Asignar este Solicutud")
    else:
        pass
    #Validar que no exista Asignacion
    try:
        Assignment.objects.get(article = article )
    except Assignment.DoesNotExist:
        pass
    else:
        return HttpResponse("Esta Asignacion ya Existe")

def validate_offer(articleID, user):
    #Se crea una instancia de AboutArticle, funcion que realiza algunas verificaciones
    aboutArticle = AboutArticle(user, articleID) 
    #Se valida la instancia: User is not candidate, is not owner, is not assigned
    if aboutArticle.is_valid():
        return aboutArticle.errors()
    else:
        return aboutArticle.errors()

def validate_quantity(quantity,article):
    if quantity < article.quantity:
        pass


def save_post_pictures(article,pictures):
    for picture in pictures:
        #Open File saved from google
        p = open(picture.name,'r+')
        #File Instance of p
        file_p = File(file=p)
        #New Picture
        n_p = Picture.objects.create(owner=article.owner,picture=file_p)
        #append picture in article
        article.pictures.add(n_p)
        #Close image
        picture.close()


def tags_to_string(tags):
    string_tags = ''
    for tag in tags:
        string_tags += (str(tag.name) + ',')
    return string_tags






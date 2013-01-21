from howmuch.article.models import Article, Offer, Assignment
from howmuch.prestige.models import ConfirmPay, ConfirmDelivery, PrestigeLikeBuyer, PrestigeLikeSeller
from howmuch.messages.models import Conversation

class AboutArticle(object):
    def __init__(self, user, itemid):
        self.user = user
        self.articleId = itemid

    #Regresa True si el Usuario es publico el Articulo dado su id
    def is_owner(self):
        try:
            Article.objects.get(owner = self.user, pk=self.articleId)
        except Article.DoesNotExist:
            return False
        return True 

    #Regresa True si el Usuario es Candidato de la publicacion del articulo dado su id, Es cuando el usuario da click en VENDER
    def is_candidate(self):
        try:
            Offer.objects.get(owner = self.user, article = self.articleId)
        except Offer.DoesNotExist:
            return False
        return True

    #Regresa True si el Usuario ha sido Asignado para completar el RequestItem (De los que dieron click en VENDER, es el que fue elegido)
    def is_assigned(self):
        try:
            Assignment.objects.get(article = self.articleId)
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
            PrestigeLikeSeller.objects.get(assignment = self.assignment, de = self.assignment.article.owner )
        except PrestigeLikeSeller.DoesNotExist:
            return False
        return True

    def has_been_critiqued_by_seller(self):
        try:
            PrestigeLikeBuyer.objects.get(assignment = self.assignment, de = self.assignment.owner )
        except PrestigeLikeBuyer.DoesNotExist:
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







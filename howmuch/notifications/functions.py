from howmuch.notifications.models import Notification
from howmuch.profile.models import Profile
from howmuch.backend.email import Email

class NotificationOptions(object):
    def __init__(self,instance, notif_type):
        self.instance = instance
        self.notif_type = notif_type

    def send(self):
        if self.notif_type == "assignment":
            title = 'Has sido seleccionado para vender el articulo %s' % (self.instance.article.title)
            context_render = {'assignment' : self.instance }
            template = 'emails/new_assignment.html'
            to = self.instance.owner
            Notification.objects.create(owner=to, article = self.instance.article ,notif_type='assignment', title = title)

        elif self.notif_type == "offer":            
            title = 'Hay un nuevo Vendedor para el articulo %s' % (self.instance.article.title)
            context_render = {'offer' : self.instance}
            template = 'emails/new_offer.html'
            to = self.instance.article.owner
            Notification.objects.create(owner = to, article = self.instance.article, notif_type = 'offer', title = title)

        elif self.notif_type == "confirm_pay":
            title = 'Confirmacion de PAGO del articulo %s' % (self.instance.assignment.article.title)
            context_render = {'confirm_pay' : self.instance}
            template = 'emails/confirm_pay.html'
            to = self.instance.assignment.owner
            Notification.objects.create(owner = to, article = self.instance.assignment.article ,notif_type = 'confirm_pay', title = title)

        elif self.notif_type == "confirm_delivery":
            title = 'Confirmacion de ENVIO del articulo %s' % (self.instance.assignment.article.title)
            context_render = {'confirm_delivery' : self.instance }
            template = 'emails/confirm_delivery.html'
            to = self.instance.assignment.article.owner
            Notification.objects.create(owner = to, article = self.instance.assignment.article, notif_type = 'confirm_delivery', title = title)
    
        elif self.notif_type == "critique":
            context_render = {'critique' : self.instance }
            title = 'Has sido Criticado por %s en el articulo %s' % (self.instance.de, self.instance.assignment.article.title)
            template = 'emails/critique.html'
            to = self.instance.to
            Notification.objects.create(owner = to, article = self.instance.assignment.article ,notif_type = 'critique', title = title)

        to.profile.add_unread_notification()
        Email(to,title,context_render,template).send()


    

    
 



    
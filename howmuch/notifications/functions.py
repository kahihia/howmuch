from howmuch.notifications.models import Notification
from howmuch.profile.models import Profile
from howmuch.backend.email import Email
from howmuch.settings import URL_OFFICIAL_SITE

class NotificationOptions(object):

    def __init__(self,instance, notif_type):
        self.instance = instance
        self.notif_type = notif_type


    def validate_emailing(self, 
                        instance, 
                        to, 
                        subject, 
                        context_render, 
                        template):
        if instance:
            Email(to,subject,context_render,template).send()

    def send(self):
        if self.notif_type == "assignment":
            to = self.instance.owner
            instance = to.notifications.new_sale
            title = 'Has sido seleccionado para vender este articulo'
            notification = Notification.objects.create(owner=to, article = self.instance.article ,
                notif_type='assignment', title = title)
            subject = 'Has sido seleccionado para vender el articulo %s' % (self.instance.article.title)
            context_render = {'assignment' : self.instance, 
                              'url' : URL_OFFICIAL_SITE + notification.get_url()}
            template = 'emails/new_assignment.html'


        elif self.notif_type == "offer":  
            to = self.instance.article.owner 
            instance = to.notifications.new_offer 
            title = 'Hay un nuevo Vendedor para este articulo'        
            notification = Notification.objects.create(owner = to, article = self.instance.article, 
                notif_type = 'offer', title = title)
            subject = 'Nuevo Vendedor para el articulo %s' % (self.instance.article.title)
            context_render = {'offer' : self.instance, 
                                'url' : URL_OFFICIAL_SITE + notification.get_url()}
            template = 'emails/new_offer.html'
        

        elif self.notif_type == "confirm_pay":
            to = self.instance.assignment.owner
            instance = to.notifications.confirm_pay
            title = 'Confirmacion de PAGO este articulo'
            notification = Notification.objects.create(owner = to, article = self.instance.assignment.article ,
                notif_type = 'confirm_pay', title = title)
            subject = 'Confirmacion de PAGO del articulo %s' % (self.instance.assignment.article.title)
            context_render = {'confirm_pay' : self.instance, 
                                'url' : URL_OFFICIAL_SITE + notification.get_url()}
            template = 'emails/confirm_pay.html'

        elif self.notif_type == "confirm_delivery":
            to = self.instance.assignment.article.owner
            instance = to.notifications.confirm_delivery
            title = 'Confirmacion de ENVIO de este articulo'
            notification = Notification.objects.create(owner = to, article = self.instance.assignment.article, 
                notif_type = 'confirm_delivery', title = title)
            subject = 'Confirmacion de ENVIO del articulo %s' % (self.instance.assignment.article.title)
            context_render = {'confirm_delivery' : self.instance, 
                                'url' : URL_OFFICIAL_SITE + notification.get_url()}
            template = 'emails/confirm_delivery.html'
    
        elif self.notif_type == "critique":
            to = self.instance.to
            instance = to.notifications.new_critique
            title = 'Has sido Criticado por %s' % (self.instance.de)
            notification = Notification.objects.create(owner = to, article = self.instance.assignment.article ,
                notif_type = 'critique', title = title)
            subject = 'Has sido Criticado por %s en el articulo %s' % (self.instance.de, self.instance.assignment.article.title)
            context_render = {'critique' : self.instance, 
                                'url' : URL_OFFICIAL_SITE + notification.get_url()}
            template = 'emails/critique.html'

        #Create unread notification 
        to.profile.add_unread_notification()
        #Send Email if instance of configuration is True
        self.validate_emailing(instance,to,subject,context_render,template)




    
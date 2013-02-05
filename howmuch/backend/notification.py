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
            to = self.instance.owner
            Notification.objects.create(owner=to, article = self.instance.article ,notif_type='assignment', title = subject)

        elif self.notif_type == "offer":            
            title = 'Hay un nuevo Vendedor para el articulo %s' % (self.instance.article.title)
            to = self.instance.article.owner
            Notification.objects.create(owner = to, article = self.instance.article, notif_type = 'offer', title = subject)

        elif self.notif_type == "confirm_pay":
            title = 'Confirmacion de PAGO del articulo %s' % (self.instance.assignment.article.title)
            to = self.instance.assignment.owner
            Notification.objects.create(owner = to, article = self.instance.assignment.article ,notif_type = 'confirm_pay', title = subject)

        
        elif self.notif_type == "confirm_delivery":
            title = 'Confirmacion de ENVIO del articulo %s' % (self.instance.assignment.article.title)
            to = self.instance.assignment.article.owner
            Notification.objects.create(owner = to, article = self.instance.assignment.article, notif_type = 'confirm_delivery', title = subject)
    
        elif self.notif_type == "critique":
            title = 'Has sido Criticado por %s en el articulo %s' % (self.instance.de, self.instance.assignment.article.title)
            to = self.instance.to
            Notification.objects.create(owner = to, article = self.instance.assignment.article ,notif_type = 'critique', title = subject)

        to.profile.add_unread_notification()



    

    
 



    
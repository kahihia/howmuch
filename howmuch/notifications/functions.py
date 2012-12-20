# -*- coding: utf8 -*- 
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.template.loader import get_template
from django.template import Context
from howmuch.notifications.models import Notification
from howmuch.perfil.models import Perfil

class SendNotification(object):
    def __init__(self,objeto, tipo):
        self.objeto = objeto
        self.tipo = tipo

    def create_unread_notification(self, owner):
        perfil = Perfil.objects.get(user = owner)
        perfil.unread_notifications += 1
        perfil.save()


    def sendNotification(self):
        if self.tipo == "assignment":
            subject = 'Has sido seleccionado para vender el articulo %s' % (self.objeto.requestItem.title)
            to = self.objeto.owner
            redirectNotification = '/messages/%s?notif_type=assignment&idBack=%s' % (self.objeto.conversation.pk, self.objeto.pk) 
            newNotification = Notification(owner=to, requestItem = self.objeto.requestItem ,tipo='assignment', title = subject, redirect = redirectNotification, idBack=self.objeto.pk)
            self.create_unread_notification(to)
            #Renderiza las variables para enviarlas por email
            dic_render = Context({'assignment' : self.objeto, 'redirect' : redirectNotification})
            html_content = get_template('emails/new_assignment.html').render(dic_render)
            text_content = strip_tags(html_content)
            #Se verifica si el usuario tiene configurado recibir un email para el caso de esta notificacion
            if to.notificationsconfig.new_sale:
                new_mail = EmailMultiAlternatives(subject, text_content, '', [to.email])
                new_mail.attach_alternative(html_content, "text/html")
                new_mail.send()

        elif self.tipo == "proffer":            
            subject = 'Hay un nuevo Vendedor para el articulo %s' % (self.objeto.requestItem.title)
            to = self.objeto.requestItem.owner
            redirectNotification = '/item/candidates/%s?notif_type=proffer&idBack=%s' % (self.objeto.requestItem.pk, self.objeto.pk)
            newNotification = Notification(owner = to, requestItem = self.objeto.requestItem, tipo = 'proffer', title = subject , redirect = redirectNotification, idBack = self.objeto.pk )
            self.create_unread_notification(to)
            #Renderiza las variables para enviarlas por email
            dic_render = Context({ 'proffer' : self.objeto ,'redirect' : redirectNotification})
            html_content = get_template('emails/new_proffer.html').render(dic_render)
            text_content = strip_tags(html_content) 
            #Se verifica si el usuario tiene configurado recibir un email para el caso de esta notificacion
            if to.notificationsconfig.new_offer:
                new_mail = EmailMultiAlternatives(subject, text_content,'', [to.email])
                new_mail.attach_alternative(html_content, "text/html")
                new_mail.send()

        elif self.tipo == "confirm_pay":
            subject = 'Confirmacion de PAGO del articulo %s' % (self.objeto.assignment.requestItem.title)
            to = self.objeto.assignment.owner
            redirectNotification = '/messages/%s?notif_type=confirm_pay&idBack=%s' % (self.objeto.assignment.conversation.pk, self.objeto.pk )
            newNotification = Notification(owner = to, requestItem = self.objeto.assignment.requestItem ,tipo = 'confirm_pay', title = subject , redirect = redirectNotification, idBack = self.objeto.pk )
            self.create_unread_notification(to)
            #Renderiza las variables para enviarlas por email
            dic_render = Context({'confirm_pay' : self.objeto, 'redirect' : redirectNotification})
            html_content = get_template('emails/confirm_pay.html').render(dic_render)
            text_content = strip_tags(html_content)
            #Se verifica si el usuario tiene configurado recibir un email para el caso de esta notificacion
            if to.notificationsconfig.confirm_pay:
                new_mail = EmailMultiAlternatives(subject, text_content,'', [to.email])
                new_mail.attach_alternative(html_content, "text/html")
                new_mail.send()
        
        elif self.tipo == "confirm_delivery":
            subject = 'Confirmacion de ENVIO del articulo %s' % (self.objeto.assignment.requestItem.title)
            to = self.objeto.assignment.requestItem.owner
            redirectNotification = '/messages/%s?notif_type=confirm_delivery&idBack=%s' % (self.objeto.assignment.conversation.pk, self.objeto.pk )
            newNotification = Notification(owner = to, requestItem = self.objeto.assignment.requestItem, tipo = 'confirm_delivery', title = subject , redirect = redirectNotification, idBack = self.objeto.pk )
            self.create_unread_notification(to)
            #Renderiza las variables para enviarlas por email
            dic_render = Context({'confirm_delivery' : self.objeto, 'redirect' : redirectNotification})
            html_content = get_template('emails/confirm_delivery.html').render(dic_render)
            text_content = strip_tags(html_content)
            #Se verifica si el usuario tiene configurado recibir un email para el caso de esta notificacion
            if to.notificationsconfig.confirm_delivery:
                new_mail = EmailMultiAlternatives(subject, text_content, '', [to.email])
                new_mail.attach_alternative(html_content, "text/html")
                new_mail.send()

        elif self.tipo == "critique":
            subject = 'Has sido Criticado por %s en el articulo %s' % (self.objeto.de, self.objeto.assignment.requestItem.title)
            to = self.objeto.to
            redirectNotification = '/messages/%s?notif_type=critique&idBack=%s' % (self.objeto.assignment.conversation.pk, self.objeto.pk )
            newNotification = Notification(owner = to, requestItem = self.objeto.assignment.requestItem ,tipo = 'critique', title = subject , redirect = redirectNotification, idBack = self.objeto.pk )
            self.create_unread_notification(to)
            #Renderiza las variables para enviarlas por email
            dic_render = Context({'critique' : self.objeto, 'redirect' : redirectNotification})
            html_content = get_template('emails/critique.html').render(dic_render)
            text_content = strip_tags(html_content)
            #Se verifica si el usuario tiene configurado recibir un email para el caso de esta notificacion
            if to.notificationsconfig.new_critique:
                new_mail = EmailMultiAlternatives(subject, text_content, '', [to.email])
                new_mail.attach_alternative(html_content, "text/html")
                new_mail.send()

    
        newNotification.save()



    

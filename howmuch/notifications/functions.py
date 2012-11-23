# -*- coding: utf8 -*- 
from django.core.mail import send_mail
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
			message = 'Esta es una confirmacion de que eres el Vendedor del articulo %s, enseguida recibiras un correo con la informacion de envio del articulo, el mensaje que el comprador te ha dejado es: %s ,puedes conversar con el comprador en el INBOX de howmuch' % (self.objeto.requestItem.title, self.objeto.comment)
			to = [self.objeto.owner.email]
			redirectNotification = '/messages/%s?notif_type=assignment&idBack=%s' % (self.objeto.conversation.pk, self.objeto.pk) 
			newNotification = Notification(owner=self.objeto.owner, requestItem = self.objeto.requestItem ,tipo='assignment', title = subject, redirect = redirectNotification, idBack=self.objeto.pk)
			self.create_unread_notification(self.objeto.owner)

		elif self.tipo == "proffer":			
			subject = 'Hay un nuevo Vendedor para el articulo %s' % (self.objeto.requestItem.title)
			message = '%s quiere venderte el articulo a $ %s, y para que lo elijas te dice lo siguiente: %s' % (self.objeto.owner, self.objeto.cprice, self.objeto.message)
			to = [self.objeto.requestItem.owner.email]
			redirectNotification = '/item/candidates/%s?notif_type=proffer&idBack=%s' % (self.objeto.requestItem.pk, self.objeto.pk)
			newNotification = Notification(owner = self.objeto.requestItem.owner, requestItem = self.objeto.requestItem, tipo = 'proffer', title = subject , redirect = redirectNotification, idBack = self.objeto.pk )
			self.create_unread_notification(self.objeto.requestItem.owner)

		elif self.tipo == "confirm_pay":
			subject = 'Confirmacion de PAGO del articulo %s' % (self.objeto.assignment.requestItem.title)
			message = '%s acaba de confirmarte el pago del articulo %s por una cantidad de %s y te ha dejado el siguiente mensaje: %s' % (self.objeto.owner, self.objeto.assignment.requestItem.title, self.objeto.amount, self.objeto.message)
			to = [self.objeto.assignment.owner.email]
			redirectNotification = '/messages/%s?notif_type=confirm_pay&idBack=%s' % (self.objeto.assignment.conversation.pk, self.objeto.pk )
			newNotification = Notification(owner = self.objeto.assignment.owner, requestItem = self.objeto.assignment.requestItem ,tipo = 'confirm_pay', title = subject , redirect = redirectNotification, idBack = self.objeto.pk )
			self.create_unread_notification(self.objeto.assignment.owner)
		
		elif self.tipo == "confirm_delivery":
			subject = 'Confirmacion de ENVIO del articulo %s' % (self.objeto.assignment.requestItem.title)
			message = '%s acaba de confirmarte el ENVIO del articulo %s y te ha dejado el siguiente mensaje: %s' % (self.objeto.owner, self.objeto.assignment.requestItem.title, self.objeto.message)
			to = [self.objeto.assignment.requestItem.owner.email]
			redirectNotification = '/messages/%s?notif_type=confirm_delivery&idBack=%s' % (self.objeto.assignment.conversation.pk, self.objeto.pk )
			newNotification = Notification(owner = self.objeto.assignment.requestItem.owner, requestItem = self.objeto.assignment.requestItem, tipo = 'confirm_delivery', title = subject , redirect = redirectNotification, idBack = self.objeto.pk )
			self.create_unread_notification(self.objeto.assignment.requestItem.owner)

		elif self.tipo == "critique":
			subject = 'Has sido Criticado por %s en el articulo %s' % (self.objeto.de, self.objeto.assignment.requestItem.title)
			message = '%s te ha criticado %s, y te ha dejado este mensaje %s' % (self.objeto.de, self.objeto.prestige, self.objeto.message)
			to = [self.objeto.to.email]
			redirectNotification = '/messages/%s?notif_type=critique&idBack=%s' % (self.objeto.assignment.conversation.pk, self.objeto.pk )
			newNotification = Notification(owner = self.objeto.to, requestItem = self.objeto.assignment.requestItem ,tipo = 'critique', title = subject , redirect = redirectNotification, idBack = self.objeto.pk )
			self.create_unread_notification(self.objeto.to)

		send_mail(subject,message,'',to)
		newNotification.save()



	

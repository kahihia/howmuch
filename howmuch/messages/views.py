# -*- coding: utf-8 -*-
from howmuch.messages.forms import MessageForm
from howmuch.messages.models import Conversation, Message
from howmuch.notifications.models import Notification
from howmuch.messages.functions import ConversationFeatures
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.db.models import Q
from django.core.mail import send_mail


def newMessage(request, conversationID):
	"""
	Verificar que la conversacion Exista
	"""
	conversation = get_object_or_404(Conversation, pk = conversationID)

	
	#Crea una instancia de conversationFeatures y verifica que quien publica el mensaje en la conversacion sea ya sea el buyer o el saller
	
	#conversationFeature = ConversationFeatures(conversation, request.user)

	"""
	Se verifica que quien publica el mensaje en la conversacion sea el buyer o seller
	"""
	if conversation.user_inside(request.user):
		pass
	else:
		return HttpResponse("No tienes permiso para publicar en esta conversacion")

	

	"""
	Si vienes de una notificacion, realizar las verificaciones y actualizar a True el status de la notificacion
	"""
	if request.GET.__contains__('notif_type') and request.GET.__contains__('idBack'):
		if request.GET['notif_type'] in ['assignment', 'confirm_pay', 'confirm_delivery'] and request.GET['idBack'] is not '' :
			notif_type = request.GET['notif_type']
			idBack = request.GET['idBack']
			try:
				#Me aseguro que el usuario sea el dueño de la notificacion, que la notificacion este en False y la paso a True
				notification = Notification.objects.get(owner=request.user, tipo = notif_type, has_been_readed = False ,idBack = idBack)
			except Notification.DoesNotExist:
				pass
			else:
				notification.has_been_readed = True
				notification.save()		

	"""
	Verifica si es comprador y tiene mensajes sin leer, en caso que si cambia el status de cada mensaje sin leer en la conversacion
	"""
	if conversation.is_buyer(request.user) and conversation.getNumber_unread_messages_buyer() > 0:
		messages = Message.objects.filter(conversation = conversation, has_been_readed=False)
		for message in messages:
			message.has_been_readed = True
			message.save()

	"""
	Verifica si es el vendedor y tiene mensajes sin leer, en caso que si cambia el status de cada mensaje sin leer en la conversacion
	"""

	if conversation.is_seller(request.user) and conversation.getNumber_unread_messages_seller() > 0:
		messages = Message.objects.filter(conversation = conversation, has_been_readed=False)
		for message in messages:
			message.has_been_readed = True
			message.save()


	if request.method == 'POST':
		form = MessageForm(request.POST)
		if form.is_valid():
			"""
			Crear el mensaje
			"""
			newMessage = form.save(commit = False)
			newMessage.owner = request.user
			newMessage.conversation = conversation
			newMessage.save()
			"""
			Envia el mensaje por mail al destinatario
			"""

			subject = 'Tienes un Nuevo mensaje sobre el articulo %s' % (conversation.assignment.requestItem.title)

			message = 'Has recibido el siguiente mensaje de: %s, %s' % (request.user, newMessage.message)

			"""
			Si el comprador envia el mensaje, el correo le llega al vendedor y viceversa
			"""
			if conversation.is_buyer(request.user):
				to = [conversation.assignment.owner.email]
			else:
				to = [conversation.assignment.requestItem.owner.email]

			send_mail(subject,message,'',to)

			return HttpResponseRedirect('/messages/' + conversationID)
	else:
		form = MessageForm()
	allmessages = Message.objects.filter(conversation = conversation).order_by('date')
	return render_to_response('messages/conversation.html', {'form' : form, 'messages' : allmessages, 'user' : request.user, 'conversation' : conversation }, context_instance = RequestContext(request))

def viewInbox(request):
	conversations = Conversation.objects.filter(Q(assignment__owner = request.user) | Q(assignment__requestItem__owner = request.user))
	return render_to_response('messages/inbox.html',{'conversations' : conversations}, context_instance = RequestContext(request))

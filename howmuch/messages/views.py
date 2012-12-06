# -*- coding: utf-8 -*-
from howmuch.core.functions import AssignmentFeatures
from howmuch.messages.forms import MessageForm
from howmuch.messages.models import Conversation, Message
from howmuch.notifications.models import Notification
from howmuch.perfil.models import Perfil
from howmuch.prestige.models import PayConfirm, DeliveryConfirm, PrestigeLikeBuyer, PrestigeLikeSeller
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.db.models import Q
from django.core.mail import send_mail
import json


def create_unread_conversation(owner):
	perfil = Perfil.objects.get(user = owner)
	perfil.unread_conversations += 1
	perfil.save()

def newMessage(request, conversationID):

	perfilUser = Perfil.objects.get(user = request.user)

	"""
	Verificar que la conversacion Exista
	"""
	conversation = get_object_or_404(Conversation, pk = conversationID)

	"""
	Se verifica que quien publica el mensaje en la conversacion sea el buyer o seller
	"""
	if conversation.assignment.is_inside(request.user):
		pass
	else:
		return HttpResponse("No tienes permiso para publicar en esta conversacion")

	"""
	Si vienes de una notificacion, realizar las verificaciones y actualizar a True el status de la notificacion
	"""
	if request.GET.__contains__('notif_type') and request.GET.__contains__('idBack'):
		if request.GET['notif_type'] in ['assignment', 'confirm_pay', 'confirm_delivery', 'critique'] and request.GET['idBack'] is not '' :
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
				Se le quita una notificacion al total de notificaciones del usuario
				"""
				perfilUser.unread_notifications -= 1
				perfilUser.save()

	"""
	Verifica si es comprador y tiene mensajes sin leer, en caso que si cambia el status de cada mensaje sin leer en la conversacion
	"""
	if conversation.assignment.is_buyer(request.user) and conversation.getNumber_unread_messages_buyer() > 0:
		messages = Message.objects.filter(conversation = conversation, has_been_readed=False)
		for message in messages:
			message.has_been_readed = True
			message.save()
		"""
		Se le quita una conversacion sin leer al total de conversaciones sin leer
		"""
		perfilUser.unread_conversations -= 1
		perfilUser.save()

	"""
	Verifica si es el vendedor y tiene mensajes sin leer, en caso que si cambia el status de cada mensaje sin leer en la conversacion
	"""

	if conversation.assignment.is_seller(request.user) and conversation.getNumber_unread_messages_seller() > 0:
		messages = Message.objects.filter(conversation = conversation, has_been_readed=False)
		for message in messages:
			message.has_been_readed = True
			message.save()
		"""
		Se le quita una conversacion sin leer al total de conversaciones sin leer
		"""
		perfilUser.unread_conversations -= 1
		perfilUser.save()

	"""
	Se crea una instancia de AssignmentFeatures para utilizar esa informacion en la conversacion
	"""

	assignmentFeatures = AssignmentFeatures(conversation.assignment)


	if request.method == 'POST':
		form = MessageForm(request.POST)
		if form.is_valid():
			
			"""
			Si es comprador y en esta conversacion el vendedor No tiene mensajes sin leer, se agrega un mensaje sin leer al vendedor y viceversa
			"""
			if conversation.assignment.is_buyer(request.user) and conversation.getNumber_unread_messages_seller() == 0:
				create_unread_conversation(conversation.assignment.owner)
			elif conversation.assignment.is_seller(request.user) and conversation.getNumber_unread_messages_buyer() == 0:
				create_unread_conversation(conversation.assignment.requestItem.owner)

			"""
			Crear el mensaje
			"""
			newMessage = form.save(commit = False)
			newMessage.owner = request.user
			newMessage.conversation = conversation
			newMessage.save()

			"""
			Se sobre escribe el valor de last_message en la conversacion
			"""
			conversation.last_message = newMessage.date
			conversation.save()

			"""
			Envia el mensaje por mail al destinatario
			"""

			subject = 'Tienes un Nuevo mensaje sobre el articulo %s' % (conversation.assignment.requestItem.title)

			message = 'Has recibido el siguiente mensaje de: %s, %s' % (request.user, newMessage.message)

			"""
			Si el comprador envia el mensaje, el correo le llega al vendedor y viceversa
			"""
			if conversation.assignment.is_buyer(request.user):
				to = conversation.assignment.owner
			else:
				to = conversation.assignment.requestItem.owner

			#Se envia un email solo si el receptor tiene activada la opcion
			if to.notificationsconfig.new_message:
				send_mail(subject,message,'',[to.email])

			return HttpResponseRedirect('/messages/' + conversationID)
	else:
		form = MessageForm()
	allmessages = Message.objects.filter(conversation = conversation).order_by('date')
	return render_to_response('messages/conversation.html', {'form' : form, 
			'messages' : allmessages, 'user' : request.user, 'conversation' : conversation, 'assignmentFeatures' : assignmentFeatures }, context_instance = RequestContext(request))

def viewInbox(request):
	conversations = Conversation.objects.filter(Q(assignment__owner = request.user) | Q(assignment__requestItem__owner = request.user)).order_by('-last_message')
	return render_to_response('messages/inbox.html',{'conversations' : conversations}, context_instance = RequestContext(request))

"""
Solicitudes de Información en la Conversacion
"""

@login_required(login_url = '/login/')
def getInfoBuyer(request,conversationID):
	conversation = get_object_or_404(Conversation, pk = conversationID)
	if conversation.assignment.is_inside(request.user):
		buyer = conversation.assignment.get_buyer()
		return render_to_response('messages/infoBuyer.html', {'conversation' : conversation, 'buyer' : buyer},
			context_instance = RequestContext(request))
	else:
		return render_to_response('messages/infoBuyer.html', {'errors' : True },
			context_instance = RequestContext(request))
	

@login_required(login_url = '/login/')
def getInfoSeller(request, conversationID):
	conversation = get_object_or_404(Conversation, pk = conversationID)
	if conversation.assignment.is_inside(request.user):
		seller = conversation.assignment.get_seller()
		return render_to_response('messages/infoSeller.html', {'conversation' : conversation, 'seller' : seller},
			context_instance = RequestContext(request))
	else:
		return render_to_response('messages/infoSeller.html', {'errors' : True },
			context_instance = RequestContext(request))

@login_required(login_url = '/login/')
def getInfoConfirmPay(request, conversationID):
	conversation = get_object_or_404(Conversation, pk = conversationID)
	confirmPay = get_object_or_404(PayConfirm, assignment = conversation.assignment )
	if conversation.assignment.is_inside(request.user):
		return render_to_response('messages/infoConfirmPay.html', {'confirmPay' : confirmPay},
			context_instance = RequestContext(request))
	else:
		return render_to_response('messages/infoConfirmPay.html', {'errors' : True },
			context_instance = RequestContext(request))
	
@login_required(login_url = '/login/')
def getInfoConfirmDelivery(request, conversationID):
	conversation = get_object_or_404(Conversation, pk = conversationID)
	confirmDelivery = get_object_or_404(DeliveryConfirm, assignment = conversation.assignment )
	if conversation.assignment.is_inside(request.user):
		return render_to_response('messages/infoConfirmDelivery.html', {'confirmDelivery' : confirmDelivery},
			context_instance = RequestContext(request))
	else:
		return render_to_response('messages/infoConfirmDelivery.html', {'errors' : True },
			context_instance = RequestContext(request))

@login_required(login_url='/login/')
def getInfoCritique(request, conversationID):
	conversation = get_object_or_404(Conversation, pk = conversationID)
	try:
		critique = PrestigeLikeBuyer.objects.get(to = request.user, assignment = conversation.assignment)
	except PrestigeLikeBuyer.DoesNotExist:
		try:
			critique = PrestigeLikeSeller.objects.get(to = request.user, assignment = conversation.assignment)
		except PrestigeLikeSeller.DoesNotExist:
			return render_to_response('messages/infoCritique.html', {'errors' : True },
				context_instance = RequestContext(request))
	return render_to_response('messages/infoCritique.html', {'critique' : critique }, 
			context_instance = RequestContext(request))


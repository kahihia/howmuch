from howmuch.messages.forms import MessageForm
from howmuch.messages.models import Conversation, Message
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

	"""
	Crea una instancia de conversationFeatures y verifica que quien publica el mensaje en la conversacion sea ya sea el buyer o el saller
	"""
	conversationFeature = ConversationFeatures(conversation, request.user)
	if conversationFeature.is_inside():
		pass
	else:
		return HttpResponse("No tienes permiso para publicar en esta conversacion")
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
			if conversationFeature.is_buyer():
				to = [conversation.assignment.owner.email]
			else:
				to = [conversation.assignment.requestItem.owner.email]

			send_mail(subject,message,'',to)

			return HttpResponseRedirect('/messages/' + conversationID)
	else:
		form = MessageForm()
	messages = Message.objects.filter(conversation = conversation).order_by('date')
	return render_to_response('messages/conversation.html', {'form' : form, 'messages' : messages, 'user' : request.user, 'conversation' : conversation }, context_instance = RequestContext(request))

def viewInbox(request):
	conversations = Conversation.objects.filter(Q(assignment__owner = request.user) | Q(assignment__requestItem__owner = request.user))
	return render_to_response('messages/inbox.html',{'conversations' : conversations}, context_instance = RequestContext(request))

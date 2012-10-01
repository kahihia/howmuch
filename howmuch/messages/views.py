from howmuch.messages.forms import MessageForm
from howmuch.messages.models import Conversation, Message
from howmuch.messages.functions import ConversationFeatures
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext


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
			newMessage = form.save(commit = False)
			newMessage.owner = request.user
			newMessage.conversation = conversation
			newMessage.save()
			return HttpResponseRedirect('/messages/' + conversationID)
	else:
		form = MessageForm()
	messages = Message.objects.filter(conversation = conversation).order_by('date')
	return render_to_response('messages/conversation.html', {'form' : form, 'messages' : messages }, context_instance = RequestContext(request))
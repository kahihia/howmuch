from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from howmuch.messages.models import Conversation
from django.db.models import Q
import json

@login_required(login_url="/login/")
def salesCount(request):
	return 0

@login_required(login_url="/login/")
def inboxCount(request):
	numConversations = 0

	conversations = Conversation.objects.filter( Q(assignment__owner = request.user, status = 1 ) | Q(assignment__requestItem__owner = request.user, status = 1) )
	for conversation in conversations:
		if conversation.is_buyer(request.user) and conversation.getNumber_unread_messages_buyer() > 0:
			numConversations += 1
		elif conversation.is_seller(request.user) and conversation.getNumber_unread_messages_seller() > 0:
			numConversations += 1
			
	return HttpResponse(json.dumps({ 'numConversations' : numConversations }))

@login_required(login_url="/login")
def purchasesCount(request):
	return 0


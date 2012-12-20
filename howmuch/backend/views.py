# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from howmuch.messages.models import Conversation
from howmuch.notifications.models import Notification
from django.db.models import Q
import json

@login_required(login_url="/login/")
def inboxCount(request):
    #en lugar de que te calcule el numero de notificaciones, ahora ese resultado esta en la base de datos y se va actualizando automaticamente
    """
    numConversations = 0
    conversations = Conversation.objects.filter( Q(assignment__owner = request.user, status = 1 ) | Q(assignment__requestItem__owner = request.user, status = 1) )
    for conversation in conversations:
        if conversation.is_buyer(request.user) and conversation.getNumber_unread_messages_buyer() > 0:
            numConversations += 1
        elif conversation.is_seller(request.user) and conversation.getNumber_unread_messages_seller() > 0:
            numConversations += 1
    return HttpResponse(json.dumps({ 'numConversations' : numConversations }))
    """
    return 0

    

@login_required(login_url="/login/")
def notificationsCount(request):
    #en lugar de que te calcule el numero de notificaciones, ahora ese resultado esta en la base de datos y se va actualizando automaticamente
    """
    numNotifications = Notification.objects.filter(owner=request.user, has_been_readed = False).count()
    return HttpResponse(json.dumps({'numNotifications' : numNotifications }))
    """
    return 0

    


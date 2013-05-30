from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from howmuch.messages.forms import MessageForm
from howmuch.messages.functions import *
from howmuch.messages.models import Conversation, Message
from howmuch.prestige.models import ConfirmPay, ConfirmDelivery, Critique


#Envia un mensaje a la conversation via ajax
@login_required(login_url = '/login/')
def send(request, conversationID):
    conversation = get_object_or_404(Conversation, pk=conversationID)
    #Verificacion de usuario
    verify_user(request.user, conversation)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            update_status_conversation(request.user, conversation)
            newMessage = form.save(commit=False)
            newMessage.owner = request.user
            newMessage.conversation = conversation
            newMessage.save()
            #Send mail to other user
            send_mail(newMessage, request.user)
            #html_response to append conversation
            html_response =  "<div class='message group border dashed margin-top-1em'>" +\
            "<div class='width-15 float-left'>" +\
            "<div class='padding-1em text-align-center'>" +\
            "<img class='padding-0_5em border width-90' src='%s'/>" % (newMessage.owner.profile.get_profile_picture()) +\
            "</div>" +\
            "</div>" +\
            "<div class='width-85 float-right group'>" +\
            "<div class='padding-1em'>" +\
            "<div class='width-60 float-left'>" +\
            "<div>" +\
            "%s" % (newMessage.message) +\
            "</div>" +\
            "</div>" +\
            "<div class='width-30 float-right text-align-right'>" +\
            "hace %s" % (newMessage.get_timestamp()) +\
            "</div>" +\
            "</div>" +\
            "</div>" +\
            "</div>"

            return HttpResponse(html_response)

@login_required(login_url = '/login/')
def view_conversation(request, conversationID):
    conversation = get_object_or_404(Conversation, pk = conversationID)
    #Se verifica que quien publica el mensaje en la conversation sea el buyer o seller
    verify_user(request.user, conversation)
    #Si vienes de una notificacion, realizar las verificaciones y actualizar a True el status de la notificacion
    update_status_notification(request)
    #Verifica si es comprador y tiene mensajes sin leer, en caso que si cambia el status de cada mensaje sin leer en la conversation
    if conversation.assignment.is_buyer(request.user):
        update_status_messages_buyer(conversation)
    #Verifica si es vendedor y tiene mensajes sin leer, en caso que si cambia el status de cada mensaje sin leer en la conversation
    if conversation.assignment.is_seller(request.user):
        update_status_messages_seller(conversation)
    allmessages = Message.objects.filter(conversation = conversation).order_by('date')
    return render_to_response('messages/conversation.html', {'messages' : allmessages, 
        'conversation' : conversation, 'status' : int(conversation.assignment.status) * 20 }, 
        context_instance = RequestContext(request))

@login_required(login_url = '/login/')
def inbox(request):
    conversations = Conversation.objects.filter(Q(assignment__owner = request.user) | 
        Q(assignment__article__owner = request.user)).order_by('-last_message')
    return render_to_response('messages/inbox.html',
        {'conversations' : conversations}, 
        context_instance = RequestContext(request))

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
    try:
        pay = ConfirmPay.objects.get(assignment = conversation.assignment)
    except ConfirmPay.DoesNotExist:
        return render_to_response('messages/infoConfirmPay.html', {
            'errors' : True,
            'url':conversation.get_url()},
            context_instance=RequestContext(request))
    else:
        return render_to_response('messages/infoConfirmPay.html', {'pay' : pay},
            context_instance=RequestContext(request))


@login_required(login_url = '/login/')
def getInfoConfirmDelivery(request, conversationID):
    conversation = get_object_or_404(Conversation, pk = conversationID)
    try:
        delivery = ConfirmDelivery.objects.get(assignment = conversation.assignment)
    except ConfirmDelivery.DoesNotExist:
        return render_to_response('messages/infoConfirmDelivery.html',{
            'errors':True, 
            'url' : conversation.get_url()},
            context_instance=RequestContext(request))
    else:
        return render_to_response('messages/infoConfirmDelivery.html',{'delivery' : delivery},
            context_instance=RequestContext(request))


@login_required(login_url='/login/')
def getInfoCritique(request, conversationID):
    conversation = get_object_or_404(Conversation, pk = conversationID)
    try:
        critique = Critique.objects.get(to = request.user, assignment = conversation.assignment)
    except Critique.DoesNotExist:
        return render_to_response('messages/infoCritique.html', {
                'errors' : True,
                'url' : conversation.get_url()},
                context_instance = RequestContext(request))
    return render_to_response('messages/infoCritique.html', {'critique' : critique }, 
            context_instance = RequestContext(request))


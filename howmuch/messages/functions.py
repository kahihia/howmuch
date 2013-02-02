from django.http import HttpResponse

from howmuch.messages.models import Message
from howmuch.notifications.models import Notification

#Verifica que un usuario en determinada conversation sea comprador o vendedor de la misma
def verify_user(user, conversation):
    if conversation.assignment.is_inside(user):
        pass
    else:
        return HttpResponse('Error')

#Si tiene mensajes sin leer cambia el status de cada mensaje sin leer en la conversation
def update_status_messages_buyer(conversation):
    if conversation.getNumber_unread_messages_buyer() > 0:
        messages = Message.objects.filter(conversation = conversation, has_been_readed=False)
        for message in messages:
            message.has_been_readed = True
            message.save()
        #Se le quita una conversation sin leer al total de conversationes sin leer
        conversation.assignment.article.owner.profile.remove_unread_conversation()


#Si tiene mensajes sin leer cambia el status de cada mensaje sin leer en la conversation
def update_status_messages_seller(conversation):
    if conversation.getNumber_unread_messages_seller() > 0:
        messages = Message.objects.filter(conversation = conversation, has_been_readed=False)
        for message in messages:
            message.has_been_readed = True
            message.save()
        #Se le quita una conversation sin leer al total de conversationes sin leer
        conversation.assignment.owner.profile.remove_unread_conversation()

def update_status_notification(request):
    if request.GET.__contains__('notif_id'):
        try:
            notificacion = Notification.objects.get(owner=request.user, pk = request.GET['notif_id'], has_been_readed=False)
        except Notification.DoesNotExist:
            pass
        else:
            notificacion.has_been_readed = True
            notificacion.save()
            request.user.profile.remove_unread_notification()

def update_status_conversation(user, conversation):
    #Si es comprador y en esta conversacion el vendedor No tiene mensajes sin leer, se agrega un mensaje sin leer al vendedor y viceversa
    if conversation.assignment.is_buyer(user) and conversation.getNumber_unread_messages_seller() == 0:
        conversation.assignment.owner.profile.add_unread_conversation()
    #Si es vendedor y en esta conversacion el comprador No tiene mensajes sin leer, se agrega un mensaje sin leer al comprador y viceversa
    elif conversation.assignment.is_seller(user) and conversation.getNumber_unread_messages_buyer() == 0:
        conversation.assignment.article.owner.profile.add_unread_conversation()







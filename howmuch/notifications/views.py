from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from howmuch.notifications.models import Notification

@login_required(login_url='/login/')
def viewNotifications(request):
    """
    Envia una Lista con las notificaciones agrupadas por article
    """
    notifications_result = []
    notifications = Notification.objects.filter(owner=request.user).order_by('article')

    if notifications.exists():  
        index = int(notifications[0].article.pk)
        notification_list = []
        notification_list_group = []

        for notification in notifications:
            if int(notification.article.pk) == index:
                notification_list_group.append(notification)
            else:
                notification_list.append(notification_list_group)
                notification_list_group = []
                index = int(notification.article.pk)
                notification_list_group.append(notification)
        notification_list.append(notification_list_group)

        for group in notification_list:
            notifications_result.append(dict([('title', group[0].article.title), ('notifications', group) ]))

    return render_to_response('notifications/notificationsView.html', {'notifications_result' : notifications_result }, context_instance = RequestContext(request))







from howmuch.notifications.models import Notification
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def viewNotifications(request):
	notifications = Notification.objects.filter(owner=request.user)
	return render_to_response('notifications/notificationsView.html', {'notifications' : notifications }, context_instance = RequestContext(request))